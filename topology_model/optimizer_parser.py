# optimizer_parser.py
import re
from netlist_parser import parse_netlist

def parse_optimizer_output(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    blocks = []
    current = []

    for line in lines:
        if line.startswith("metrics") and current:
            blocks.append(current)
            current = []
        current.append(line.strip())
    if current:
        blocks.append(current)

    parsed = []
    for block in blocks:
        specs = {}
        sizing = {}
        regions = {}
        reward = None
        for line in block:
            if line.startswith("metrics"):
                matches = re.findall(r'(\w+):\s*(-?\d*\.?\d+(?:e[+-]?\d+)?)', line)
                for k, v in matches:
                    specs[k] = float(v)
            elif any("nA" in part or "vbias" in part for part in line.split(",")):
                matches = re.findall(r'(\w+):\s*(-?\d*\.?\d+(?:e[+-]?\d+)?)', line)
                for k, v in matches:
                    sizing[k] = float(v)
            elif line.startswith("MM"):
                matches = re.findall(r'(MM\d+)\s+is\s+in\s+([\w\-]+)', line)
                for mm, region in matches:
                    regions[mm] = region
            elif line.startswith("reward"):
                reward = float(line.split()[-1])
                specs["reward"] = reward
        parsed.append({
            "specs": specs,
            "sizing": sizing,
            "regions": regions
        })

    return parsed

# #TESTING OPTIMIZER CODE
# # 
# test_path = "new_folder_7nmsingle_ended_cascode_current_mirror/out1.txt"

# # Parse it
# parsed_results = parse_optimizer_output(test_path)

# # Print the result to inspect
# for idx, result in enumerate(parsed_results):
#     print(f"\n==== BLOCK {idx} ====")
#     print("Specs:", result["specs"])
#     print("Sizing:", result["sizing"])
#     print("Regions:", result["regions"]) 


import os

def combine_netlist_optimizer(netlist_data, optimizer_entry, netlist_path):
    netlist_name = os.path.splitext(os.path.basename(netlist_path))[0]
    grouped_components = netlist_data["components"]  # transistors, vsources, etc.
    net_to_components = netlist_data["net_to_components"]
    regions = optimizer_entry["regions"]
    sizing = optimizer_entry["sizing"]

    updated_components = {}

    for group_name, group_dict in grouped_components.items():
        updated_group = {}
        for name, comp in group_dict.items():
            region = regions.get(name)
            sized_params = {}

            for param_key, param_val in comp["params"].items():
                if isinstance(param_val, str) and param_val in sizing:
                    sized_params[param_key] = sizing[param_val]
                else:
                    sized_params[param_key] = param_val

            updated_comp = {
                "type": comp["type"],
                "pins": comp["pins"],
                "params": sized_params
            }

            if "subtype" in comp:
                updated_comp["subtype"] = comp["subtype"]

            if region:
                updated_comp["region"] = region

            updated_group[name] = updated_comp

        updated_components[group_name] = updated_group

    return {
        "netlist_name": netlist_name,
        "graph": {
            "components": updated_components,
            "net_to_components": net_to_components
        },
        "sim_outputs": {
            "specs": optimizer_entry["specs"],
            "sizing": sizing
        }
    }


# TESTING COMBINER

netlist_path = "/homes/hhussein/Desktop/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror.scs"
optimizer_output_path = "new_folder_7nmsingle_ended_cascode_current_mirror/out1.txt"
netlist_data = parse_netlist(netlist_path)
optimizer_data = parse_optimizer_output(optimizer_output_path)

# Combine
combined_data = combine_netlist_optimizer(netlist_data, optimizer_data[0], netlist_path)

# print(combined_data)

