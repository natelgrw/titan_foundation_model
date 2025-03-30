import numpy as np
import pandas as pd
import re
from collections import OrderedDict
from turbo.turbo import Turbo1
from eval_engines.spectre.script_test.single_ended_cascode_current_mirror_meas_man import *
import globalsy
import os


def params_from_netlist(scs_file):
    """
    parameter definitions from a netlist files (.scs)
    """
    params = {}

    with open(scs_file, "r") as file:
        lines = file.readlines()
    for line in lines:
        # extracting parameters section (tempc={{tempc}} nA1={{nA1}} nB1={{nB1}} ...)
        if line.strip().startswith("parameters"):
            matches = re.findall(r'(\w+)=\{\{(\w+)\}\}', line)
            for match in matches:
                param_name = match[0]
                param_val = match[1]
                params[param_name] = param_val
    return params

# params = params_from_netlist("/Users/heba/Desktop/chandrakasan_lab/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror_pmos.scs")
# print(params)

def transistor_params_netlist(scs_file):
    """
    extracting nfin, W, L from netlist
    """
    with open(scs_file, "r") as file:
        lines = file.readlines()

    transistors = {}
    for line in lines:
        # Match transistor definitions: MM<number> <nodes> <device_type> l=<L_value> nfin=<W_value>
        match = re.search(r'(MM\d+)\s+[\w!]+\s+[\w!]+\s+[\w!]+\s+[\w!]+\s+(pfet|nfet)\s+l=(\S+)\s+nfin=(\S+)', line)
        if match:
            name = match.group(1)  # e.g., MM14
            type_ = match.group(2)  # pfet or nfet
            length = match.group(3)  # e.g., nA1
            width = match.group(4)   # e.g., nB1
            transistors[name] = {"type": type_, "L": length, "W": width}
    return transistors

# transistors = transistor_params_netlist("/Users/heba/Desktop/chandrakasan_lab/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror_pmos.scs")
# print(transistors)
scs_file = "/Users/heba/Desktop/chandrakasan_lab/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror_pmos.scs"

netlist_params = params_from_netlist(scs_file)
transistor_params = transistor_params_netlist(scs_file)

lb = []
ub = []


for name, values in transistor_params.items():
    if values["L"] in netlist_params and values["W"] in netlist_params: # plus/minus 50% range right now
        lb.append(float(netlist_params[values["L"]]) * 0.5)
        ub.append(float(netlist_params[values["L"]]) * 1.5)
        lb.append(float(netlist_params[values["W"]]) * 0.5)
        ub.append(float(netlist_params[values["W"]]) * 1.5)

class Levy:
    def __init__(self, dim, params_id, specs_id, specs_ideal, ub, lb):
        self.dim = dim
        self.params_id = params_id
        self.specs_id = specs_id
        self.specs_ideal = specs_ideal
        self.ub = ub
        self.lb = lb

    def reward(self, spec, goal_spec, specs_id):
        """
        Computes the reward of the circuit based on its gain and power.
        """
        rel_specs = (np.array(spec) - np.array(goal_spec)) / (np.abs(goal_spec) + np.abs(spec))
        reward = sum(
            (3 * abs(val) if specs_id[i] == "gain" and val < 0 else abs(val))
            for i, val in enumerate(rel_specs)
        )
        return reward

    def __call__(self, x):
        """
        Runs the circuit simulation and evaluates the reward.
        """
        assert len(x) == self.dim
        assert np.all(x <= self.ub) and np.all(x >= self.lb)

        # Assign extracted parameters to netlist variables
        param_values = np.append(x, [0.4, 0.8, 27])  # Adding vcm, vdd, tempc
        param_dict = OrderedDict(zip(self.params_id, param_values))

        # Run simulation
        sim_env = OpampMeasMan(scs_file)
        cur_specs = OrderedDict(sorted(sim_env.evaluate([param_dict])[0][1].items(), key=lambda k: k[0]))

        # Compute reward
        reward1 = self.reward(list(cur_specs.values())[:-1], self.specs_ideal, self.specs_id)

        # Save results
        save_results(param_dict, -reward1)
        return reward1
    
output_file = "optimizer_results.csv"

f = Levy(19, params_id, specs_id, specs_ideal, vcm, vdd, tempc, ub, lb)

#store in a graph transformer
# how to respresent the data https://dspace.mit.edu/bitstream/handle/1721.1/132297/2005.00406.pdf?sequence=2&isAllowed=y
# baysian optimizer base - look into how it works 
# encoder & decoder code base, another paper to look at

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