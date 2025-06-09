import numpy as np
from collections import OrderedDict
from turbo.turbo.turbo_1 import Turbo1
from turbo.turbo.turbo_m import TurboM
import numpy as np
import torch
import math
import matplotlib
import matplotlib.pyplot as plt
from eval_engines.spectre.script_test.single_ended_cascode_current_mirror_meas_man import *
import globalsy
import re

#import psutil

MINI_PATH = "/cleaned_gana_netlists/single_ended_cascode_current_mirror_LG_load_biasn_LV.scs_cr2_2.scs"
SCS_FILE_PATH = f"/homes/natelgrw/Documents/turbo_circuit_optimizer/netlist_data{MINI_PATH}"

np.random.seed(1299)

# constant values
vcm = 0.40
vdd = 0.8
tempc = 27

# TODO: clarify target specs/purpose of code!
region_mapping = {
    0: "cut-off",
    1: "triode",
    2: "saturation",
    3: "sub-threshold",
    4: "breakdown"
}

# TODO: clarify target specs/purpose of code, this can change!
specs_dict = {
    "gain": 1680.0,        # ~64.5 dB
    "UGBW": 3e6,           # 3 MHz
    "PM": 60.0,            # Phase Margin
    "power": 10e-6         # 10 µW
}

specs_id = list(specs_dict.keys())
specs_ideal = list(specs_dict.values())

#shared ranges to make new bound list
shared_ranges = {
    'nA': (40e-9, 100e-9),
    'nB': (5, 100),
    'vbiasp': (0.4, 0.8),
    'vbiasn': (0.2, 0.8),
    'rr': (1e4, 1e8),
    'cc': (0.3e-12, 3e-12)
}

def extract_parameter_names(scs_file):
    with open(scs_file, "r") as file:
        for line in file:
            if line.strip().startswith("parameters"):
                # extracting all names before '='
                matches = re.findall(r'(\w+)=', line)
                matches.remove("vcm")
                matches.remove("vdd")
                matches.remove("tempc")
                return matches
    return []
    
# return np.array(lb), np.array(ub), param_names

# param_values = {}
# i.e. {'nA1': 6.66e-08, 'nB1': 5.0, 'nA2': 7.1e-08, 'nB2': 6.0}

# CIR_YAML = "/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/specs_test/single_ended_cascode_current_mirror.yaml"
# with open(CIR_YAML, 'r') as f:
#             yaml_data = yaml.load(f, OrderedDictYAMLLoader)
# f.close()
# params = yaml_data['params']
# specs = yaml_data['target_spec']
# specs_ideal = []
# for spec in list(specs.values()):
#              specs_ideal.append(spec)
# specs_ideal = np.array(specs_ideal)
# params_id = list(params.keys())
# specs_id = list(specs.keys())

def build_bounds(params_id, shared_ranges):
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

#import ipdb; ipdb.set_trace()

class Levy:
    def __init__(self, dim, params_id, specs_id, specs_ideal, vcm, vdd, tempc, ub, lb):
        self.dim = dim
        self.params_id = params_id
        self.specs_id = specs_id
        self.specs_ideal = specs_ideal
        self.vcm = vcm
        self.vdd = vdd
        self.tempc = tempc
        self.ub = ub
        self.lb = lb

    def lookup(self,spec, goal_spec):
        goal_spec = [float(e) for e in goal_spec]
        spec = [float(e) for e in spec]
        spec = np.array(spec)
        goal_spec =np.array(goal_spec)

        norm_spec = (spec-goal_spec)/(np.abs(goal_spec)+np.abs(spec)) #(spec-goal_spec)/(goal_spec+spec)
        return norm_spec

    def reward(self,spec, goal_spec, specs_id):
        rel_specs = self.lookup(spec, goal_spec)
        pos_val = [] 
        reward = 0
        for i,rel_spec in enumerate(rel_specs):
            if(specs_id[i] == 'power' and rel_spec > 0):
                reward += np.abs(rel_spec) #/10
            elif(specs_id[i] == 'gain' and rel_spec < 0):
                reward += 3*np.abs(rel_spec) #/10
            elif (specs_id[i] != 'power' and rel_spec < 0):
                reward += np.abs(rel_spec)
        return reward ###updated

    def __call__(self, x):
        assert len(x) == self.dim
        assert x.ndim == 1
        print(np.all(x <= self.ub) and np.all(x >= self.lb))# assert np.all(x <= self.ub) and np.all(x >= self.lb) #ASSERTION FAILED
	    # w = 1 + (x - 1.0) / 4.0
        # val = np.sin(np.pi * w[0]) ** 2 + \
        #     np.sum((w[1:self.dim - 1] - 1) ** 2 * (1 + 10 * np.sin(np.pi * w[1:self.dim - 1] + 1) ** 2)) + \
        #     (w[self.dim - 1] - 1) ** 2 * (1 + np.sin(2 * np.pi * w[self.dim - 1])**2)
        sim_env = OpampMeasMan(SCS_FILE_PATH)
        sample = x.copy()
        for i, param in enumerate(self.params_id): #TODO: check with dimple is there should just be nBs in list or also nA
            if param.startswith('nB'):  # Discrete values
                sample[i] = round(sample[i])
        sample = np.append(sample,self.vcm)
        sample = np.append(sample,self.vdd)
        sample = np.append(sample,self.tempc)
        param_val = [OrderedDict(list(zip(self.params_id,sample)))]

        cur_specs = OrderedDict(sorted(sim_env.evaluate(param_val)[0][1].items(), key=lambda k:k[0]))
        
        dict1 = OrderedDict(list(cur_specs.items())[:-5]) #all the original
        dict3 = OrderedDict(list(cur_specs.items())[-5:-4]) #region
        dict2 = OrderedDict(list(cur_specs.items())[-4:]) #remaining 

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
        # f = open("/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/out1.txt",'a')
        # print("cur_specs", cur_specs, file=f)
        reward1 = self.reward(cur_specs,self.specs_ideal,self.specs_id)

        if globalsy.counterrrr < 200:
                f = open("/homes/natelgrw/Documents/out1.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()
        elif globalsy.counterrrr < 1200:
                f = open("/homes/natelgrw/Documents/out11.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()
        elif globalsy.counterrrr < 2000:
                f = open("/homes/natelgrw/Documents/out12.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()

        if globalsy.counterrrr < 200:
                f = open("/homes/natelgrw/Documents/out1.txt",'a')
                for i, j in zip(range(15),[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]):
                   region = region_mapping.get(int(dict3_nparray[i]), 'unknown')
                   print(f"MM{j} is in {region}", end=', ' if i < 14 else '\n', file=f)
                print("reward", format(-reward1, '.3g'), file=f)
                f.close()
                globalsy.counterrrr=globalsy.counterrrr+1
        elif globalsy.counterrrr < 1200:
                f = open("/homes/natelgrw/Documents/out11.txt",'a')
                for i, j in zip(range(15),[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]):
                   region = region_mapping.get(int(dict3_nparray[i]), 'unknown')
                   print(f"MM{j} is in {region}", end=', ' if i < 14 else '\n', file=f)
                print("reward", format(-reward1, '.3g'), file=f)
                f.close()
                globalsy.counterrrr=globalsy.counterrrr+1
        elif globalsy.counterrrr < 2000:
                f = open("/homes/natelgrw/Documents/out12.txt",'a')
                for i, j in zip(range(15),[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]):
                   region = region_mapping.get(int(dict3_nparray[i]), 'unknown')
                   print(f"MM{j} is in {region}", end=', ' if i < 14 else '\n', file=f)
                print("reward", format(-reward1, '.3g'), file=f)
                f.close()
                globalsy.counterrrr=globalsy.counterrrr+1
        val = reward1
       # proc=psutil.Process()
       # print(proc.open_files())
        return val

params_id = extract_parameter_names(SCS_FILE_PATH)
print(params_id)
lb, ub = build_bounds(params_id, shared_ranges)
print(params_id)
f = Levy(len(lb), params_id, specs_id, specs_ideal, vcm, vdd, tempc, ub, lb)

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
