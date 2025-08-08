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

IGNORE_LIST = ['*.info', '*.primitives', '*.subckts', 'logFile']

OCEAN_TEMPLATE = """
resultsDir = \"%(dir_file_path)s\"
selectResult(resultsDir)
wave = v(\"%(signal_name)s\" ?result \"tran\")
ocnPrint(wave ?output \"%(csv_output_path)s\" ?precision 15 ?header t)
"""

class FileNotCompatible(Exception):
    """
    raise when file is not compatible with libpsf
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self,  args, kwargs)

def is_ignored(string):
    return any([fnmatch.fnmatch(string, pattern) for pattern in IGNORE_LIST])

def ocean_export_csv(dir_file_path, csv_output_path, signal_name="/Voutp"):
    """Run OCEAN script to export a signal to CSV."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ocn', delete=False) as tmp_script:
        script_path = tmp_script.name
        tmp_script.write(OCEAN_TEMPLATE % {
            "dir_file_path": dir_file_path,
            "csv_output_path": csv_output_path,
            "signal_name": signal_name
        })

    try:
        result = subprocess.run(
            ["ocean", "-nograph", "-restore", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30  # prevent hanging forever
        )
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            raise RuntimeError(f"OCEAN error:\n{result.stderr}")
    finally:
        os.remove(script_path)

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
                output_csv = os.path.join(folder_path, f"{base_name}_Voutp.csv")

                if not os.path.exists(output_csv):  # don’t overwrite existing CSVs
                    try:
                        print(f"file_path = {file_path}")
                        print(f"is file? {os.path.isfile(file_path)}")
                        print(f"is dir? {os.path.isdir(file_path)}")
                        print(f"parent dir = {os.path.dirname(file_path)}")
                        ocean_export_csv(os.path.dirname(file_path), output_csv, signal_name="/Voutp")
                        print(f"Exported CSV to {output_csv}")
                    except Exception as e:
                        print(f"Failed to export {file}: {e}")
                else:
                    print(f"CSV already exists: {output_csv}")
                continue

            try:
                datum = cls.process_file(file_path)
            except FileNotCompatible:
                with open("/homes/natelgrw/Documents/titan_foundation_model/badfiles.txt", "a") as f:
                    f.write('failed on {}'.format(file))
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
            with open("/homes/natelgrw/Documents/titan_foundation_model/badfiles.txt", "a") as f:
                f.write("File not compatible: {}\n".format(file))
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
