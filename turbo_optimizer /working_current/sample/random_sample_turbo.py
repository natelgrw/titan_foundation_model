import numpy as np
from collections import OrderedDict
import yaml
import yaml.constructor

from turbo.turbo import Turbo1
from turbo.turbo import TurboM
import numpy as np
import torch
import math
import matplotlib
import matplotlib.pyplot as plt
from eval_engines.spectre.script_test.single_ended_cascode_current_mirror_meas_man import *
import globalsy
import re

#import psutil

np.random.seed(1299)
region_mapping = {
        0: 'cut-off',
        1: 'triode',
        2: 'saturation',
        3: 'sub-threshold',
        4: 'breakdown'
        }


# Define the ranges
# nA1_range = (7e-9, 40e-9)
# nB1_range = (1, 200)
# nA2_range = (10e-9, 40e-9)
# nB2_range = (1, 200)
# nA3_range = (10e-9, 40e-9)
# nB3_range = (1, 200)
# nA4_range = (10e-9, 40e-9)
# nB4_range = (1, 200)
# nA5_range = (10e-9, 40e-9)
# nB5_range = (1, 200)
# nA6_range = (10e-9, 40e-9)
# nB6_range = (1, 200)
# nA7_range = (10e-9, 40e-9)
# nB7_range = (1, 200)
# nA8_range = (10e-9, 40e-9)
# nB8_range = (1, 200)
# nA9_range = (10e-9, 40e-9)
# nB9_range = (1, 200)
# vbiasp0_range = (0, 0.8)
# vbiasp1_range = (0, 0.8)
# vbiasp2_range = (0, 0.8)
# vbiasn0_range = (0, 0.8)
# vbiasn1_range = (0, 0.8)
# vbiasn2_range = (0, 0.8)
# cc_range = (1e-15, 1e-11)
# vcm = 0.40
# vdd = 0.8
# tempc = 27

scs_file = "/Users/heba/Desktop/chandrakasan_lab/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror_pmos.scs"

def transistor_params_netlist(scs_file):
    with open(scs_file, "r") as file:
        lines = file.readlines()
    transistors = {}
    for line in lines:
        match = re.search(r'(MM\d+)\s+[\w!]+\s+[\w!]+\s+[\w!]+\s+[\w!]+\s+(pfet|nfet)\s+l=(\S+)\s+nfin=(\S+)', line)
        if match:
            name, type_, length, width = match.groups()[0], match.groups()[1], match.groups()[2], match.groups()[3]
            transistors[name] = {"type": type_, "L": length, "W": width}
    return transistors

transistor_params = transistor_params_netlist(scs_file) #TODO change this to current netlist

vcm = 0.4       # Common-mode input voltage
vdd = 0.8       # Supply voltage
tempc = 27      # Temperature in °C

def generate_bounds(transistor_params, param_values):
    lb = []
    ub = []
    param_names = []

    for name, comp in transistor_params.items():
        for param_type in ['L', 'W']:
            param_name = comp[param_type]
            if param_name not in param_names:  # Avoid duplicates
                param_names.append(param_name)
                if param_name in param_values:
                    val = float(param_values[param_name])
                    low, high = val * 0.5, val * 1.5
                else:
                    # Default hard-coded fallback if param not in values
                    low, high = 1e-9, 1e-7
                lb.append(low)
                ub.append(high)
    
    return np.array(lb), np.array(ub), param_names

param_values = {}
# i.e. {'nA1': 6.66e-08, 'nB1': 5.0, 'nA2': 7.1e-08, 'nB2': 6.0}

lb, ub, param_order = generate_bounds(transistor_params, param_values) #TODO: determine param values with nathan

# Get a random sample

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
# 


#CAN CHANGE

specs_dict = {
    "gain": 1680.0,
    "UGBW": 3.49e9,
    "PM": -117.0,
    "power": 5.85e-7
}

specs_id = list(specs_dict.keys())
specs_ideal = list(specs_dict.values())
params_id = param_order + ["vcm", "vdd", "tempc"]


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
        assert np.all(x <= self.ub) and np.all(x >= self.lb)
        # w = 1 + (x - 1.0) / 4.0
        # val = np.sin(np.pi * w[0]) ** 2 + \
        #     np.sum((w[1:self.dim - 1] - 1) ** 2 * (1 + 10 * np.sin(np.pi * w[1:self.dim - 1] + 1) ** 2)) + \
        #     (w[self.dim - 1] - 1) ** 2 * (1 + np.sin(2 * np.pi * w[self.dim - 1])**2)
        sim_env = OpampMeasMan(scs_file)
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
                f = open("/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/out1.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()
        elif globalsy.counterrrr < 1200:
                f = open("/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/out11.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()
        elif globalsy.counterrrr < 2000:
                f = open("/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/out12.txt",'a')
                for ordered_dict in param_val:
                    formatted_items = [f"{k}: {format(v, '.3g')}" for k, v in ordered_dict.items()]
                    print(", ".join(formatted_items), file=f)
                f.close()


        if globalsy.counterrrr < 200:
                f = open("/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/out1.txt",'a')
                for i, j in zip(range(15),[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]):
                   region = region_mapping.get(int(dict3_nparray[i]), 'unknown')
                   print(f"MM{j} is in {region}", end=', ' if i < 14 else '\n', file=f)
                print("reward", format(-reward1, '.3g'), file=f)
                f.close()
                globalsy.counterrrr=globalsy.counterrrr+1
        elif globalsy.counterrrr < 1200:
                f = open("/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/out11.txt",'a')
                for i, j in zip(range(15),[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]):
                   region = region_mapping.get(int(dict3_nparray[i]), 'unknown')
                   print(f"MM{j} is in {region}", end=', ' if i < 14 else '\n', file=f)
                print("reward", format(-reward1, '.3g'), file=f)
                f.close()
                globalsy.counterrrr=globalsy.counterrrr+1
        elif globalsy.counterrrr < 2000:
                f = open("/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/out12.txt",'a')
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

f = Levy(len(lb), params_id, specs_id, specs_ideal, vcm, vdd, tempc, ub, lb)

turbo1 = Turbo1(
    f=f,  # Handle to objective function
    lb=lb,  # Numpy array specifying lower bounds
    ub=ub,  # Numpy array specifying upper bounds
    n_init=20,  # Number of initial bounds from an Latin hypercube design
    max_evals = 2000,  # Maximum number of evaluations
    batch_size=5,  # How large batch size TuRBO uses
    verbose=True,  # Print information from each batch
    use_ard=True,  # Set to true if you want to use ARD for the GP kernel
    max_cholesky_size=2000,  # When we switch from Cholesky to Lanczos
    n_training_steps=30,  # Number of steps of ADAM to learn the hypers
    min_cuda=10.40,  # Run on the CPU for small datasets
    device="cpu",  # "cpu" or "cuda"
    dtype="float32",  # float64 or float32
)

turbo1.optimize()

X = turbo1.X  # Evaluated points
fX = turbo1.fX  # Observed values
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



