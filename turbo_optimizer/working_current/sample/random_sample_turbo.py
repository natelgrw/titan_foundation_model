import numpy as np
from collections import OrderedDict
from turbo.turbo.turbo_1 import Turbo1
from turbo.turbo.turbo_m import TurboM
import numpy as np
import torch
import math
import matplotlib
import matplotlib.pyplot as plt
from working_current.eval_engines.spectre.script_test.single_ended_meas_man import *
from working_current.eval_engines.spectre.specs_test.config_env import *
import globalsy
import re

SCS_FILE_PATH = f"/homes/natelgrw/Documents/titan_foundation_model/demo_netlists/single_ended_low_voltage_cascode_current_mirror.scs"

np.random.seed(2000)

# constant parameter values
vcm = 0.5
vdd = 1.0
tempc = 27.0

# transistor power states
region_mapping = {
    0: "cut-off",
    1: "triode",
    2: "saturation",
    3: "sub-threshold",
    4: "breakdown"
}

# netlist target specifications
specs_dict = {
    "gain": 1.0e5,
    "UGBW": 1.0e9,
    "PM": 60.0,
    "power": 1.0e-6,
}

# parameter bounds
shared_ranges = {
    'nA': (10e-9, 30e-9),
    'nB': (1, 20),
    'vbiasp': (0, 0.80),
    'vbiasn': (0, 0.80),
    'rr': (5e3, 1e7),
    'cc': (0.1e-12, 2.5e-12)
}

# reformatted specs for optimizer input
specs_id = list(specs_dict.keys())
specs_ideal = list(specs_dict.values())

def extract_parameter_names(scs_file):
    """
    Extracts all parameter names from a given Spectre netlist file.
    """
    with open(scs_file, "r") as file:
        for line in file:
            if line.strip().startswith("parameters"):
                matches = re.findall(r'(\w+)=', line)
                matches.remove("tempc")
                matches.remove("vcm")
                matches.remove("vdd")
                matches.remove("dc_offset")
                matches.remove("gain_n")
                matches.remove("use_tran")
                matches.remove("rfeedback_val")
                return matches
    return []

def build_bounds(params_id, shared_ranges):
    """
    Builds lower and upper bounds for netlist parameters based on parameter bounds in shared_ranges.
    """
    lb, ub = [], []
    for pname in params_id:
        if pname.startswith("nA"):
            low, high = shared_ranges['nA']
        elif pname.startswith("nB"):
            low, high = shared_ranges['nB']
        elif "biasp" in pname:
            low, high = shared_ranges['vbiasp']
        elif "biasn" in pname:
            low, high = shared_ranges['vbiasn']
        elif pname.startswith("nC"):
            low, high = shared_ranges['cc']
        elif pname.startswith("nR"):
            low, high = shared_ranges['rr']
        else:
            raise ValueError(f"Unknown parameter: {pname}")
        lb.append(low)
        ub.append(high)
    return np.array(lb), np.array(ub)

def classify_opamp_type(file_path):
    """
    Classifies the operational amplifier type based on the netlist file name.
    """
    with open(file_path, "r") as file:
        for line in file:
            if "Voutn" in line:
                return "differential"
        else:
            return "single_ended"

class Levy:
    """
    A representation class of netlist parameeters and bounds for the optimization function.
    Implements important lookup, reward, and __call__ functions for evaluating netlist performance.

    Args:
    - dim (int): Dimension of the parameter space, or the number of parameters involved.
    - params_id (list): List of parameter names as strings.
    - specs_id (list): List of target specification names as strings.
    - specs_ideal (list): List of ideal target specification values, as floats.
    - vcm (float): Set common mode voltage.
    - vdd (float): Set supply voltage.
    - empc (float): Set temperature in Celsius.
    - ub (np.ndarray): Upper bounds for the parameters.
    - lb (np.ndarray): Lower bounds for the parameters.
    """
    def __init__(self, dim, params_id, specs_id, specs_ideal, vcm, vdd, tempc, ub, lb, yaml_path):
        self.dim = dim
        self.params_id = params_id
        self.specs_id = specs_id
        self.specs_ideal = specs_ideal
        self.vcm = vcm
        self.vdd = vdd
        self.tempc = tempc
        self.ub = ub
        self.lb = lb
        self.yaml_path = yaml_path

    def lookup(self, spec, goal_spec):
        """
        Calulcates the normalized difference, or error, between the current specs and
        the ideal specs. Outputs a numpy array of normalized deviations.
        """
        goal_spec = [float(e) for e in goal_spec]
        spec = [float(e) for e in spec]
        spec = np.array(spec)
        goal_spec = np.array(goal_spec)

        # normalized deviation calculation: (spec-goal_spec)/(goal_spec+spec)

        norm_spec = (spec-goal_spec)/(np.abs(goal_spec)+np.abs(spec))

        return norm_spec

    def reward(self, spec, goal_spec, specs_id):
        """
        Calculates a penalty-based reward value based on the normalized deviations
        of current measured specs from the established target specs.

        Penalty Weights:
        - Gain: 3.0 (critical): crucial for signal amplification.
        - UGBW: 4.0 (very critical): directly impacts speed and frequency performance.
        - PM: 2.0 (moderately critical): affects circuit stability.
        - Power: 1.0 (less critical): important for efficiency, but trade-offs are allowed.
        """
        rel_specs = self.lookup(spec, goal_spec)
        reward = 0
        for i, rel_spec in enumerate(rel_specs):
            if specs_id[i] == "power" and rel_spec > 0:
                reward += np.abs(rel_spec)
            elif specs_id[i] == "gain" and rel_spec < 0:
                reward += 50.0 * np.abs(rel_spec)
            elif specs_id[i] == "UGBW" and rel_spec < 0:
                reward += 30.0 * np.abs(rel_spec)
            elif specs_id[i] == "PM" and rel_spec < 0:
                reward += 30.0 * np.abs(rel_spec)

        return reward

    def __call__(self, x):

        # assertions and bounds checks
        assert len(x) == self.dim
        assert x.ndim == 1
        print(np.all(x <= self.ub) and np.all(x >= self.lb))

        # creation of cadence simulation environment
        sim_env = OpampMeasMan(self.yaml_path)

        # establishing a parameter vector with current values
        sample = x.copy()

        for i, param in enumerate(self.params_id):
            if param.startswith('nB'): 
                sample[i] = round(sample[i])

        sample = np.append(sample, self.vcm)
        sample = np.append(sample, self.vdd)
        sample = np.append(sample, self.tempc)
    
        param_val = [OrderedDict(list(zip(self.params_id,sample)))]

        # IMPORTANT: calls evaluate() to obtain simulation specs and sort them
        cur_specs = OrderedDict(sorted(sim_env.evaluate(param_val)[0][1].items(), key=lambda k:k[0]))
        
        dict1 = OrderedDict(list(cur_specs.items())[:-5])   # original specs
        dict3 = OrderedDict(list(cur_specs.items())[-5:-4]) # regional information
        dict2 = OrderedDict(list(cur_specs.items())[-4:])   # all remaining parameters

        # flattening OrderedDicts to numpy arrays for data processing
        dict2_values = list(dict2.values())
        flattened_dict2 = [item for sublist in dict2_values for item in sublist]
        dict2_nparray = np.array(flattened_dict2)

        dict3_values = list(dict3.values())
        flattened_dict3 = [item for sublist in dict3_values for item in sublist]
        dict3_nparray = np.array(flattened_dict3) #extra_ob
                
        cur_specs = np.array(list(dict1.values()))[:-1]
        dummy = cur_specs[0]
        cur_specs[0] = cur_specs[1]
        cur_specs[1] = dummy

        # calculating reward based on reward() function
        reward1 = self.reward(cur_specs, self.specs_ideal, self.specs_id)

        # logging tested parameter values to text files
        if globalsy.counterrrr < 200:
                f = open("/homes/natelgrw/Documents/titan_foundation_model/results/out1.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()
        elif globalsy.counterrrr < 1200:
                f = open("/homes/natelgrw/Documents/titan_foundation_model/results/out11.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()
        elif globalsy.counterrrr < 2000:
                f = open("/homes/natelgrw/Documents/titan_foundation_model/results/out12.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()

        # dynamically determine number of transistors
        num_transistors = len(dict3_nparray)

        # determine output file based on counter
        if globalsy.counterrrr < 200:
            filename = "/homes/natelgrw/Documents/titan_foundation_model/results/out1.txt"
        elif globalsy.counterrrr < 1200:
            filename = "/homes/natelgrw/Documents/titan_foundation_model/results/out11.txt"
        elif globalsy.counterrrr < 2000:
            filename = "/homes/natelgrw/Documents/titan_foundation_model/results/out12.txt"
        else:
            filename = None

        if filename:
            with open(filename, 'a') as f:
                # log transistor regions dynamically
                for i in range(num_transistors):
                    region = region_mapping.get(int(dict3_nparray[i]), 'unknown')
                    end_char = ', ' if i < num_transistors - 1 else '\n'
                    print(f"MM{i} is in {region}", end=end_char, file=f)

                # log reward
                print("reward", format(-reward1, '.3g'), file=f)

            globalsy.counterrrr += 1

        return reward1

params_id = extract_parameter_names(SCS_FILE_PATH)
lb, ub = build_bounds(params_id, shared_ranges)
opamp_type = classify_opamp_type(SCS_FILE_PATH)
config_env = EnvironmentConfig(SCS_FILE_PATH, opamp_type, specs_dict, params_id, lb, ub)
yaml_path = config_env.write_yaml_configs()
f = Levy(len(lb), params_id, specs_id, specs_ideal, vcm, vdd, tempc, ub, lb, yaml_path)

turbo1 = Turbo1(
    f=f,  # handle to objective function
    lb=lb,  # numpy array specifying lower bounds
    ub=ub,  # numpy array specifying upper bounds
    n_init=20,  # number of initial bounds from an Latin hypercube design
    max_evals = 2000,  # maximum number of evaluations
    batch_size=5,  # how large batch size TuRBO uses
    verbose=True,  # print information from each batch
    use_ard=True,  # set to true if you want to use ARD for the GP kernel
    max_cholesky_size=2000,  # when we switch from Cholesky to Lanczos
    n_training_steps=30,  # number of steps of ADAM to learn the hypers
    min_cuda=10.40,  # run on CPU for small datasets
    device="cpu",  # "cpu" or "cuda"
    dtype="float32",  # float64 or float32
)

turbo1.optimize()

X = turbo1.X  # evaluated points
fX = turbo1.fX  # observed values
ind_best = np.argmin(fX)
f_best, x_best = fX[ind_best], X[ind_best, :]

print("Best value found:\n\tf(x) = %.3f\nObserved at:\n\tx = %s" % (f_best, np.around(x_best, 3)))

config_env.del_yaml()

# turbo_m = TurboM(
#     f=f,  # Handle to objective function
#     lb=lb,  # Numpy array specifying lower bounds
#     ub=ub,  # Numpy array specifying upper bounds
#     n_init=10,  # Number of initial bounds from an Symmetric Latin hypercube design
#     max_evals=300,  # Maximum number of evaluations
#     n_trust_regions=5,  # Number of trust regions
#     batch_size=10,  # How large batch size TuRBO uses
#     verbose=True,  # Print information from each batch
#     use_ard=True,  # Set to true if you want to use ARD for the GP kernel
#     max_cholesky_size=200,  # When we switch from Cholesky to Lanczos
#     n_training_steps=50,  # Number of steps of ADAM to learn the hypers
#     min_cuda=10.40,  # Run on the CPU for small datasets
#     device="cpu",  # "cpu" or "cuda"
#     dtype="float32",  # float64 or float32
# )

# turbo_m.optimize()

# X = turbo_m.X  # Evaluated points
# fX = turbo_m.fX  # Observed values
# ind_best = np.argmin(fX)
# f_best, x_best = fX[ind_best], X[ind_best, :]

# print("Best value found:\n\tf(x) = %.3f\nObserved at:\n\tx = %s" % (f_best, np.around(x_best, 3)))
