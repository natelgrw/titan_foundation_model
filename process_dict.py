import re

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


# Example usage:
data = {}
parse_ocean_csv("outputvoutp.csv", "tran_voutp", data)
parse_ocean_csv("outputvinn.csv", "tran_vinn", data)

print(data)