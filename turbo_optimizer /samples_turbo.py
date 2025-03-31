import numpy as np
import pandas as pd
import re
from collections import OrderedDict
from turbo.turbo.turbo_1 import Turbo1
from eval_engines.spectre.script_test.single_ended_cascode_current_mirror_meas_man import *
import globalsy
import os

# Netlist
def params_from_netlist(scs_file):
    params = {}
    with open(scs_file, "r") as file:
        for line in file:
            if line.strip().startswith("parameters"):
                matches = re.findall(r'(\w+)=\{\{(\w+)\}\}', line)
                for match in matches:
                    param_name, param_val = match
                    params[param_name] = param_val
    return params

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

# Netlist file
scs_file = "/Users/heba/Desktop/chandrakasan_lab/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror_pmos.scs"
netlist_params = params_from_netlist(scs_file)
transistor_params = transistor_params_netlist(scs_file)

# Bounds
lb = []
ub = []
for name, values in transistor_params.items():
    if values["L"] in netlist_params and values["W"] in netlist_params:
        lb.append(float(netlist_params[values["L"]]) * 0.5)
        ub.append(float(netlist_params[values["L"]]) * 1.5)
        lb.append(float(netlist_params[values["W"]]) * 0.5)
        ub.append(float(netlist_params[values["W"]]) * 1.5)

lb = np.array(lb)
ub = np.array(ub)

# Simulating
vcm = 0.4
vdd = 0.8
tempc = 27

params_id = list(netlist_params.keys()) + ["vcm", "vdd", "tempc"]
specs_id = ["gain", "power"]
specs_ideal = np.array([60, 0.5])  # Example targets

# Saving (to csv)
import csv
output_file = "optimizer_results.csv"
if not os.path.exists(output_file):
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["netlist"] + params_id + specs_id + ["reward"])

def save_results(netlist_name, param_vals, specs, reward):
    row = [netlist_name] + [param_vals.get(p, "") for p in params_id] + [specs.get(s, "") for s in specs_id] + [reward]
    with open(output_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

# 
class Levy:
    def __init__(self, dim, params_id, specs_id, specs_ideal, ub, lb):
        self.dim = dim
        self.params_id = params_id
        self.specs_id = specs_id
        self.specs_ideal = specs_ideal
        self.ub = ub
        self.lb = lb

    def reward(self, spec, goal_spec, specs_id):
        rel_specs = (np.array(spec) - np.array(goal_spec)) / (np.abs(goal_spec) + np.abs(spec))
        return sum((3 * abs(val) if specs_id[i] == "gain" and val < 0 else abs(val)) for i, val in enumerate(rel_specs))

    def __call__(self, x):
        assert len(x) == self.dim
        assert np.all(x <= self.ub) and np.all(x >= self.lb)

        param_values = np.append(x, [vcm, vdd, tempc])
        param_dict = OrderedDict(zip(self.params_id, param_values))

        sim_env = OpampMeasMan(scs_file)
        try:
            cur_specs = OrderedDict(sorted(sim_env.evaluate([param_dict])[0][1].items(), key=lambda k: k[0]))
        except Exception as e:
            print(f"Simulation failed: {e}")
            return 1e6

        gain = cur_specs.get("gain", 0)
        if gain <= 0:
            print("Non-functional (gain <= 0)")
            return 1e6

        reward1 = self.reward(list(cur_specs.values())[:-1], self.specs_ideal, self.specs_id)
        save_results(scs_file, param_dict, cur_specs, -reward1)
        return reward1

# Optimizer
f = Levy(len(lb), params_id, specs_id, specs_ideal, ub, lb)

turbo1 = Turbo1(
    f=f,
    lb=lb,
    ub=ub,
    n_init=20,
    max_evals=200,
    batch_size=5,
    verbose=True,
    device="cpu",
    dtype="float32",
)

turbo1.optimize()
