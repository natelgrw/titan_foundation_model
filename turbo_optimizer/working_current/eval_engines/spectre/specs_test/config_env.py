import yaml
import os

class EnvironmentConfig(object):
    def __init__(self, netlist_path, type, specs, params, param_lbs, param_ubs):
        self.netlist_path = netlist_path
        self.type = type
        self.specs = specs
        self.params = params
        self.param_lbs = param_lbs
        self.param_ubs = param_ubs
        self.configs = {
            "database_dir": "/homes/natelgrw/Documents/titan_foundation_model/results",
            "measurement": {
                "meas_params": {},
                "testbenches": {
                    "ac_dc": {
                        "netlist_template": self.netlist_path,
                        "tb_module": f"eval_engines.spectre.script_test.{self.type}_meas_man",
                        "tb_class": "ACTB",
                        "post_process_function": "process_ac",
                        "tb_params": {}
                    }
                }
            },
            "params": {},
            "spec_range": {},
            "normalize": {},
            "target_specs": {}
        }
        self.spec_ranges = []
        self.normalized_list = []
        self.param_dict = {}
        self.yaml_path = ""

    def build_specs(self):
        for spec, val in self.specs.items():
            val = float(val)
            self.configs["target_specs"][spec] = (val,)
    
            if spec == "PM":
                self.spec_ranges.append((val - 30, val + 30, 1))
                self.normalized_list.append(1)
            else:
                self.spec_ranges.append((val / 10, val * 10, val / 100))
                self.normalized_list.append(val / 100)

    def build_params(self):
        for i in range(len(self.params)):
            param = self.params[i]
            lb = float(self.param_lbs[i])
            ub = float(self.param_ubs[i])
            if self.params[i] in ["vdd", "vcm", "tempc"] or self.params[i].startswith("nB"):
                self.param_dict[param] = (lb, ub, 1)
            elif self.params[i].startswith("nA"):
                self.param_dict[param] = (lb, ub, lb / 10)
            elif self.params[i].startswith("vbias"):
                self.param_dict[param] = (lb, ub, 0.01)
            elif self.params[i].startswith(("nR", "nC")):
                self.param_dict[param] = (lb, ub, lb / 100)

    def build_configs(self):
        self.build_specs()
        self.build_params()

        self.configs["params"] = self.param_dict
        self.configs["spec_range"] = self.spec_ranges
        self.configs["normalize"] = self.normalized_list

    def write_yaml_configs(self):
        self.build_configs()

        # Create YAML filename based on netlist name
        netlist_name = os.path.splitext(os.path.basename(self.netlist_path))[0]
        yaml_filename = f"{netlist_name}.yaml"

        # Absolute path in the same directory as the Python file
        self.yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), yaml_filename)

        # Write configs to YAML
        with open(self.yaml_path, "w") as f:
            yaml.dump(self.configs, f, default_flow_style=False, sort_keys=False)

        print(f"YAML configuration written to {self.yaml_path}")
        return self.yaml_path
    
    def del_yaml(self):
        if os.path.exists(self.yaml_path):
            os.remove(self.yaml_path)
            print(f"Deleted YAML file: {self.yaml_path}")
        else:
            print(f"YAML file does not exist: {self.yaml_path}")
    
