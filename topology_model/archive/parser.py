import re
from collections import defaultdict
import torch

def parse_netlist_general(netlist_text):
    lines = netlist_text.splitlines()
    net_to_components = defaultdict(set)
    component_nets = {}

    # Regex for basic SPICE/Spectre elements
    patterns = {
        "transistor": re.compile(r'^(MM\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(nfet|pfet)'),
        # "vsource": re.compile(r'^(V\w+)\s+\((\S+)\s+(\S+)\)\s+vsource.*'),
        # "vcvs": re.compile(r'^(E\w+)\s+\((\S+)\s+(\S+)\s+(\S+)\s+(\S+)\)\s+vcvs.*'),
        "resistor": re.compile(r'^(R\w+)\s+(\S+)\s+(\S+)\s+'),
        "capacitor": re.compile(r'^(C\w+)\s+(\S+)\s+(\S+)\s+'),
    }

    for line in lines:
        line = line.strip()
        matched = False

        for name, pattern in patterns.items():
            match = pattern.match(line)
            if match:
                comp_id = match.group(1)
                nets = match.groups()[1:]

                # flatten nets (remove None, handle parenthesis)
                nets = [n.strip('()') for n in nets if n]
                component_nets[comp_id] = nets

                for net in nets:
                    net_to_components[net].add(comp_id)
                matched = True
                break

        # optionally handle other line types

    # Build edges from shared nets
    edges = set()
    for net, comps in net_to_components.items():
        comps = list(comps)
        for i in range(len(comps)):
            for j in range(i + 1, len(comps)):
                edges.add((comps[i], comps[j]))
                edges.add((comps[j], comps[i]))  # undirected

    # Assign integer indices
    component_list = list(component_nets.keys())
    name_to_idx = {name: idx for idx, name in enumerate(component_list)}

    edge_index = torch.tensor(
        [[name_to_idx[u], name_to_idx[v]] for u, v in edges],
        dtype=torch.long
    ).t()

    return edge_index, component_list, component_nets

with open("example_netlist.scs", "r") as f:
    netlist_text = f.read()

edge_index, node_names, node_to_nets = parse_netlist_general(netlist_text)

print("Graph edges:", edge_index.shape)
print("Nodes:", node_names)

def generate_node_features(component_dict):
    """
    Args:
        component_dict: dict of {name: {'type': ..., 'L': ..., 'W': ..., etc.}}
    Returns:
        features: tensor [num_nodes, feature_dim]
        feature_names: list of node names (order matches rows)
    """
    node_names = list(component_dict.keys())
    types = sorted(set(comp['type'] for comp in component_dict.values()))

    type_to_idx = {t: i for i, t in enumerate(types)}
    feature_dim = len(types) + 4  # one-hot + up to 4 params

    features = []

    for name in node_names:
        comp = component_dict[name]
        t_idx = type_to_idx[comp["type"]]
        one_hot = [1 if i == t_idx else 0 for i in range(len(types))]

        params = [
            float(comp.get("L", 0.0)),
            float(comp.get("W", 0.0)),
            float(comp.get("value", 0.0)),
            float(comp.get("gain", 0.0)),  # for VC(V)S etc
        ]

        feat_vec = one_hot + params
        features.append(feat_vec)

    return torch.tensor(features, dtype=torch.float), node_names

