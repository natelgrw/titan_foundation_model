'''
# netlist_parser.py
import re
from collections import defaultdict

def parse_netlist(netlist_path):
    with open(netlist_path, 'r') as f:
        lines = f.readlines()

    components = {}
    net_to_components = defaultdict(set)

    transistor_pattern = re.compile(r'(MM\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(nfet|pfet).*l=(\S+)\s+nfin=(\S+)')
    vsource_pattern = re.compile(r'(V\w+)\s+\(([^)]+)\)\s+vsource\s+(?:dc=)?(\S+)')
    isource_pattern = re.compile(r'(I\w+)\s+\(([^)]+)\)\s+isource\s+(?:dc=)?(\S+)')
    resistor_pattern = re.compile(r'(RR?\d*)\s+(\S+)\s+(\S+)\s+resistor\s+r=(\S+)')
    capacitor_pattern = re.compile(r'(CC\d+)\s+(\S+)\s+(\S+)\s+capacitor\s+c=(\S+)')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('//'):
            continue

        t_match = transistor_pattern.match(line)
        if t_match:
            name, d, g, s, b, ttype, L, W = t_match.groups()
            components[name] = {
                "type": ttype,
                "pins": [d, g, s, b],
                "params": {"L": L, "W": W},
                "region": None  # Placeholder, can be filled from optimizer later
            }
            for net in [d, g, s, b]:
                net_to_components[net].add(name)

        v_match = vsource_pattern.match(line)
        if v_match:
            name, pin_str, val = v_match.groups()
            pins = pin_str.split()
            components[name] = {
                "type": "vsource",
                "pins": pins,
                "params": {"value": val}
            }
            for net in pins:
                net_to_components[net].add(name)

        i_match = isource_pattern.match(line)
        if i_match:
            name, pin_str, val = i_match.groups()
            pins = pin_str.split()
            components[name] = {
                "type": "isource",
                "pins": pins,
                "params": {"value": val}
            }
            for net in pins:
                net_to_components[net].add(name)

        r_match = resistor_pattern.match(line)
        if r_match:
            name, n1, n2, val = r_match.groups()
            components[name] = {
                "type": "resistor",
                "pins": [n1, n2],
                "params": {"R": val}
            }
            for net in [n1, n2]:
                net_to_components[net].add(name)

        c_match = capacitor_pattern.match(line)
        if c_match:
            name, n1, n2, val = c_match.groups()
            components[name] = {
                "type": "capacitor",
                "pins": [n1, n2],
                "params": {"C": val}
            }
            for net in [n1, n2]:
                net_to_components[net].add(name)

    return {
        "components": components,
        "net_to_components": dict(net_to_components)
    }

# optimizer_parser.py
import re

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



# TESTING NEW PARSER


netlist_path = "/homes/hhussein/Desktop/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror.scs"  # e.g., /Users/heba/Desktop/single_ended.scs

result = parse_netlist(netlist_path)

components = result["components"]
net_map = result["net_to_components"]

print("==== COMPONENTS ====")
for comp, info in components.items():
    print(f"{comp}: {info}")

print("\n==== NET TO COMPONENTS MAP ====")
for net, comps in net_map.items():
    print(f"{net}: {sorted(comps)}")

'''

# import re
# from collections import defaultdict

import re
from collections import defaultdict
import os

def parse_netlist(netlist_path):
    with open(netlist_path, 'r') as f:
        lines = f.readlines()

    grouped_components = {
        "transistors": {},
        "vsources": {},
        "isources": {},
        "resistors": {},
        "capacitors": {}
    }
    net_to_components = defaultdict(set)

    # Patterns
    transistor_pattern = re.compile(r'(MM\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(nfet|pfet).*l=(\S+)\s+nfin=(\S+)')
    vsource_pattern = re.compile(r'(V\w+)\s+\(([^)]+)\)\s+vsource\s+(?:dc=)?(\S+)')
    isource_pattern = re.compile(r'(I\w+)\s+\(([^)]+)\)\s+isource\s+(?:dc=)?(\S+)')
    resistor_pattern = re.compile(r'(RR?\d*)\s+(\S+)\s+(\S+)\s+resistor\s+r=(\S+)')
    capacitor_pattern = re.compile(r'(CC\d+)\s+(\S+)\s+(\S+)\s+capacitor\s+c=(\S+)')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('//'):
            continue

        # Transistors
        t_match = transistor_pattern.match(line)
        if t_match:
            name, d, g, s, b, ttype, L, W = t_match.groups()
            grouped_components["transistors"][name] = {
                "type": ttype,
                "pins": [d, g, s, b],
                "params": {"L": L, "W": W},
                "region": None
            }
            for net in [d, g, s, b]:
                net_to_components[net].add(name)
            continue

        # Voltage sources
        v_match = vsource_pattern.match(line)
        if v_match:
            name, pin_str, val = v_match.groups()
            pins = pin_str.split()
            # CLASSIFYING SUBTYPES
            bias_nets = {"bias"} # has word bias in voltages
            input_nets = {"in", "cm", "Vinp", "Vinn"} # special type of node w/ floating edge, need attrivutes for differntt parts, gds
            output_nets = {"Vout", "Voutp"} # special edge attribute
            global_nets = {"vdd!", "gnd!", "0"} # supply voltages
            subtype = "other"
            pins_lower = [p.lower() for p in pins]

            if any(any(bias in pin for bias in bias_nets) for pin in pins_lower):
               subtype = "bias"
            elif any(pin in input_nets for pin in pins):
                subtype = "input"
            elif any(pin in output_nets for pin in pins):
                subtype = "output"
            elif all(pin in global_nets for pin in pins):
                subtype = "global"

            grouped_components['vsources'][name] = {
                "type": "vsource",
                "subtype": subtype,
                "pins": pins,
                "params": {"value": val}
            }
            
            for net in pins:
                net_to_components[net].add(name)
            continue

        # Current sources
        i_match = isource_pattern.match(line)
        if i_match:
            name, pin_str, val = i_match.groups()
            pins = pin_str.split()
            grouped_components["isources"][name] = {
                "type": "isource",
                "pins": pins,
                "params": {"value": val}
            }
            for net in pins:
                net_to_components[net].add(name)
            continue

        # Resistors
        r_match = resistor_pattern.match(line)
        if r_match:
            name, n1, n2, val = r_match.groups()
            grouped_components["resistors"][name] = {
                "type": "resistor",
                "pins": [n1, n2],
                "params": {"R": val}
            }
            for net in [n1, n2]:
                net_to_components[net].add(name)
            continue

        # Capacitors
        c_match = capacitor_pattern.match(line)
        if c_match:
            name, n1, n2, val = c_match.groups()
            grouped_components["capacitors"][name] = {
                "type": "capacitor",
                "pins": [n1, n2],
                "params": {"C": val}
            }
            for net in [n1, n2]:
                net_to_components[net].add(name)
            continue

    return {
    "netlist_name": os.path.splitext(os.path.basename(netlist_path))[0],
    "components": grouped_components,
    "net_to_components": dict(net_to_components)
}


if __name__ == "__main__":
    test_netlist_path = "/homes/hhussein/Desktop/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror.scs"  # Update this to your actual file
    parsed = parse_netlist(test_netlist_path)

    # components = parsed["components"]
    # print("\n==== COMPONENT GROUPS ====")
    # for group, group_data in components.items():
    #     if group_data:
    #         print(f"\n{group.upper()}:")
    #         for name, info in group_data.items():
    #             print(f"  {name}: {info}")


    # # Print net connections
    # print("\n==== NET CONNECTIONS ====")
    # for net, comps in parsed["net_to_components"].items():
    #     print(f"{net}: {comps}")

    print(parsed)




def generate_node_features(node_names, components):
    """
    Generate node features for each component node.

    Returns:
        x: FloatTensor [num_nodes, feature_dim]
    """
    type_to_id = {"nfet": 0, "pfet": 1, "capacitor": 2, "resistor": 3, "vsource": 4, "isource": 5}
    features = []

    for name in node_names:
        # Find component
        for group, comp_dict in components.items():
            if name in comp_dict:
                comp = comp_dict[name]
                ctype = comp["type"]
                type_id = type_to_id.get(ctype, -1)

                if ctype in {"nfet", "pfet"}:
                    L = comp.get("L", 0.0)
                    W = comp.get("W", 0.0)
                    features.append([type_id, L, W])
                elif ctype == "capacitor":
                    features.append([type_id, comp["C"], 0.0])
                elif ctype == "resistor":
                    features.append([type_id, comp["R"], 0.0])
                elif ctype in {"vsource", "isource"}:
                    val = comp["value"]
                    val = float(val) if isinstance(val, str) and val.replace(".", "", 1).isdigit() else 0.0
                    features.append([type_id, val, 0.0])
                break
        else:
            # Unknown component, pad with zeros
            features.append([-1, 0.0, 0.0])

    return torch.tensor(features, dtype=torch.float)
