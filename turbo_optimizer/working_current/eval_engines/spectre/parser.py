import sys
import os
import scipy.interpolate as interp
import scipy.optimize as sciopt
import libpsf
import fnmatch
import pdb
import IPython
import subprocess
import tempfile
import re

IGNORE_LIST = ['*.info', '*.primitives', '*.subckts', 'logFile']

OCEAN_TEMPLATE_BOTH = """
resultsDir = \"%(dir_file_path)s\"
openResults(resultsDir)
selectResult('tran)
wave_1 = v("Voutp")
wave_2 = v("Voutn")
ocnPrint(?output \"%(csv_output_path_voutp)s\" wave_1 ?precision 15)
ocnPrint(?output \"%(csv_output_path_voutn)s\" wave_2 ?precision 15)
exit
"""

OCEAN_TEMPLATE_SINGLE = """
resultsDir = \"%(dir_file_path)s\"
openResults(resultsDir)
selectResult('tran)
wave_1 = v("Voutp")
ocnPrint(?output \"%(csv_output_path_voutp)s\" wave_1 ?precision 15)
exit
"""

class FileNotCompatible(Exception):
    """
    raise when file is not compatible with libpsf
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,  args, kwargs)

def is_ignored(string):
    return any([fnmatch.fnmatch(string, pattern) for pattern in IGNORE_LIST])

def ocean_export_csv(dir_file_path, csv_output_path_voutp, csv_output_path_voutn, include_voutn=True):
    """Run OCEAN script to export signals to CSV."""
    template = OCEAN_TEMPLATE_BOTH if include_voutn else OCEAN_TEMPLATE_SINGLE
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ocn', delete=False) as tmp_script:
        script_path = tmp_script.name
        tmp_script.write(template % {
            "dir_file_path": dir_file_path,
            "csv_output_path_voutp": csv_output_path_voutp,
            "csv_output_path_voutn": csv_output_path_voutn
        })

    try:
        result = subprocess.run(
            ["ocean", "-nograph", "-restore", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=100
        )
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            raise RuntimeError(f"OCEAN error:\n{result.stderr}")
    finally:
        os.remove(script_path)

def parse_ocean_csv(file_path, key_name, data_dict):
    """
    Parse an OCEAN CSV-like file and append data to the given dictionary.
    Converts:
        - time to nanoseconds
        - voltage to millivolts
    """
    unit_to_multiplier_time = {
        "s": 1e9,      # seconds → nanoseconds
        "n": 1,        # nanoseconds → nanoseconds
        "p": 1e-3,     # picoseconds → nanoseconds
        "f": 1e-6,     # femtoseconds → nanoseconds
    }
    unit_to_multiplier_voltage = {
        "V": 1000,     # volts → millivolts
        "m": 1,        # millivolts → millivolts
        "u": 1e-3,     # microvolts → millivolts
    }

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.lower().startswith("time"):
                continue  # skip header or empty lines

            parts = re.split(r"\s+", line)
            if len(parts) < 2:
                continue

            # Parse time
            match_time = re.match(r"([\d\.\-Ee+]+)([a-z]*)", parts[0])
            if match_time:
                time_val = float(match_time.group(1))
                time_unit = match_time.group(2)
                time_ns = round(time_val * unit_to_multiplier_time.get(time_unit, 1), 8)

            # Parse voltage
            match_volt = re.match(r"([\d\.\-Ee+]+)([a-z]*)", parts[1])
            if match_volt:
                volt_val = float(match_volt.group(1))
                volt_unit = match_volt.group(2)
                volt_mV = round(volt_val * unit_to_multiplier_voltage.get(volt_unit, 1), 8)

            # Append to dictionary
            data_dict.setdefault(key_name, []).append((time_ns, volt_mV))

class SpectreParser(object):

    @classmethod
    def parse(cls, raw_folder):
        folder_path = os.path.abspath(raw_folder)
        data = dict()
        files =  os.listdir(folder_path)
        for file in files:
            if is_ignored(file):
                continue

            file_path = os.path.join(raw_folder, file)

            if file.endswith(".tran.tran"):
                base_name = file.replace(".tran.tran", "")
                output_csv_voutp = os.path.join(folder_path, f"{base_name}_Voutp.csv")
                output_csv_voutn = os.path.join(folder_path, f"{base_name}_Voutn.csv")

                if not os.path.exists(output_csv_voutp):
                    try:
                        print(f"Exporting {file_path} ...")
                        # Try with Voutn first
                        try:
                            ocean_export_csv(file_path, output_csv_voutp, output_csv_voutn, include_voutn=True)
                            has_voutn = True
                        except RuntimeError as e:
                            if "Voutn" in str(e):  # OCEAN complained
                                print("⚠️ Voutn not found, retrying without it...")
                                ocean_export_csv(file_path, output_csv_voutp, output_csv_voutn, include_voutn=False)
                                has_voutn = False
                            else:
                                raise
                    except Exception as e:
                        print(f"Failed to export {file}: {e}")
                        continue
                else:
                    has_voutn = os.path.exists(output_csv_voutn)

                # Parse voutp always
                parse_ocean_csv(output_csv_voutp, "tran_voutp", data)

                # Parse voutn only if available
                if has_voutn and os.path.exists(output_csv_voutn):
                    parse_ocean_csv(output_csv_voutn, "tran_voutn", data)

                continue

            try:
                datum = cls.process_file(file_path)
            except FileNotCompatible:
                continue

            _, kwrd = os.path.split(file)
            kwrd = os.path.splitext(kwrd)[0]
            data[kwrd] = datum

        return data

    @classmethod
    def process_file(cls, file):
        fpath = os.path.abspath(file)
        try:
            psfobj = libpsf.PSFDataSet(fpath)
        except:
            raise FileNotCompatible('file {} was not compatible with libpsf'.format(file))

        is_swept = psfobj.is_swept()
        datum = dict()
        for signal in psfobj.get_signal_names():
            datum[signal] = psfobj.get_signal(signal)

        if is_swept:
            datum['sweep_vars'] = psfobj.get_sweep_param_names()
            datum['sweep_values'] = psfobj.get_sweep_values()

        psfobj.close()
        return datum

if __name__ == '__main__':

   res = SpectreParser.parse(sys.argv[1])
   pdb.set_trace()
   print(res)
