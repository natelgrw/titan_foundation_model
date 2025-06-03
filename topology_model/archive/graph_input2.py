import torch
from optimizer_parser import combine_netlist_optimizer, parse_optimizer_output
from netlist_parser import parse_netlist


# def build_node_features(components):
#     node_features = []
#     node_names = []

#     type_map = {'nfet': 0, 'pfet': 1, 'resistor': 2, 'capacitor': 3, 'isource': 4}
#     region_map = {'sub-threshold': 0, 'triode': 1, 'saturation': 2, 'unknown': -1}

#     for name, comp in components.items():
#         if comp["type"] == "vsource":
#             continue

#         comp_type = comp["type"]
#         region = comp.get("region", "unknown")
#         params = comp["params"]

#         L = params.get("L", 0.0)
#         W = params.get("W", 0.0)
    #    val_str = params.get("value", "0.0")
#         try:
#             val = float(val_str)
#         except ValueError:
#             val = 0.0

#         t_idx = type_map.get(comp_type, -1)
#         r_idx = region_map.get(region, -1)

#         node_feat = [t_idx, r_idx, float(L), float(W), val]
#         node_features.append(node_feat)
#         node_names.append(name)

#     return torch.tensor(node_features, dtype=torch.float), node_names

def build_node_features(components, bias_voltages=None):
    # print("Components keys:", components.keys())

    node_features = []
    node_names = []
    
    # Update for bias voltages
    if bias_voltages is None:
        bias_voltages = {}

    type_map = {'nfet': 0, 'pfet': 1, 'vbias': 2, 'v_input': 3}  # Added vsource for bias nodes
    region_map = {'sub-threshold': 0, 'triode': 1, 'saturation': 2}
    
    # Add bias voltages as nodes
    # for name, value in bias_voltages.items():
    #     node_features.append([2, 0, 0.0, 0.0, value])  # Example: vsource as type 2
    #     node_names.append(name)
    
    for name, comp in components.items():
        comp_type = comp["type"]
        region = comp.get("region", "unknown")
        params = comp["params"]
        L = params.get("L", 0.0)
        W = params.get("W", 0.0)
        val_str = params.get("value", "0.0")
        try:
            val = float(val_str)
        except ValueError:
            val = 0.0
        t_idx = type_map.get(comp_type, -1)
        r_idx = region_map.get(region, -1)
        node_feat = [t_idx, r_idx, float(L), float(W), val]
        node_features.append(node_feat)
        node_names.append(name)
    return torch.tensor(node_features, dtype=torch.float), node_names




def get_edge_label(net):
    net = net.lower()
    if "vdd" in net:
        return 1
    elif "gnd" in net:
        return 2
    elif "vbias" in net:
        return 3
    elif "vin" in net:
        return 4
    elif "vout" in net:
        return 5
    else:
        return 0  # generic


# def build_edge_index(net_to_components, node_names):
#     name_to_idx = {name: i for i, name in enumerate(node_names)}
#     edge_index = []
#     edge_attr = []

#     for net, comp_set in net_to_components.items():
#         comps = list(comp_set)
#         label = get_edge_label(net)

#         for i in range(len(comps)):
#             for j in range(i + 1, len(comps)):
#                 if comps[i] not in name_to_idx or comps[j] not in name_to_idx:
#                     continue

#                 src = name_to_idx[comps[i]]
#                 tgt = name_to_idx[comps[j]]

#                 edge_index.append([src, tgt])
#                 edge_index.append([tgt, src])
#                 edge_attr.append(label)
#                 edge_attr.append(label)

#     edge_index = torch.tensor(edge_index, dtype=torch.long).t()
#     edge_attr = torch.tensor(edge_attr, dtype=torch.long)
#     return edge_index, edge_attr

def build_edge_index(net_to_components, node_names, bias_voltages=None):
    name_to_idx = {name: i for i, name in enumerate(node_names)}
    edges = set()

    if bias_voltages is None:
        bias_voltages = {}

    # Add bias voltage edges
    for bias_name, bias_value in bias_voltages.items():
        bias_idx = name_to_idx[bias_name]
        for comp_set in net_to_components.values():
            comps = list(comp_set)
            for comp_name in comps:
                comp_idx = name_to_idx[comp_name]
                edges.add((comp_idx, bias_idx))
                edges.add((bias_idx, comp_idx))  # Undirected edge for bias voltage

    # Add regular component-to-component edges
    for comp_set in net_to_components.values():
        comps = list(comp_set)
        for i in range(len(comps)):
            for j in range(i + 1, len(comps)):
                src = name_to_idx[comps[i]]
                tgt = name_to_idx[comps[j]]
                edges.add((src, tgt))
                edges.add((tgt, src))  # Undirected edge

    edge_index = list(edges)
    return edge_index


# Load and parse
netlist_path = "/homes/hhussein/Desktop/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/netlist_templates/7nm/single_ended_cascode_current_mirror.scs"
optimizer_output_path = "new_folder_7nmsingle_ended_cascode_current_mirror/out1.txt"
netlist_data = parse_netlist(netlist_path)
optimizer_data = parse_optimizer_output(optimizer_output_path)

# Combine them
combined = combine_netlist_optimizer(netlist_data, optimizer_data[0], netlist_path)

# Build graph components
# node_feats, node_names = build_node_features(combined["graph"]["components"])
flat_components = {}
for group in combined["graph"]["components"].values():
    if group != "v_sources":
        flat_components.update(group)

node_feats, node_names = build_node_features(flat_components)
edge_index = build_edge_index(combined["graph"]["net_to_components"], node_names)

# Print shapes
# print(f"Number of nodes: {len(node_names)}")
# print(f"Node feature shape: {len(node_feats)} x {len(node_feats[0])}")
# print(f"Number of edges: {edge_index.shape[1]}")
# print(f"Edge attr shape: {edge_attr.shape}")

# # Example nodes and edges
# print("\nExample node names and features:")
# for name, feat in zip(node_names[:3], node_feats[:3]):
#     print(f"{name}: {feat}")

# print("\nExample edges:")
# for idx in range(5):
#     src, tgt = edge_index[:, idx]
#     label = edge_attr[idx]
#     print(f"{node_names[src]} <-> {node_names[tgt]} (label: {label})")


# Visualization
# import networkx as nx
# import matplotlib.pyplot as plt

# def visualize_graph(edge_index, node_names):
#     G = nx.Graph()

#     if isinstance(edge_index, torch.Tensor):
#         if edge_index.dim() == 2 and edge_index.shape[0] == 2:
#             edges = edge_index.t().tolist()
#         else:
#             raise ValueError("edge_index tensor must have shape [2, num_edges].")
#     elif isinstance(edge_index, list) and isinstance(edge_index[0], (list, tuple)):
#         edges = edge_index
#     else:
#         raise ValueError("edge_index must be a [2, N] tensor or list of edge pairs.")

#     G.add_edges_from(edges)

#     mapping = {i: name for i, name in enumerate(node_names)}
#     G = nx.relabel_nodes(G, mapping)

#     plt.figure(figsize=(10, 8))
#     pos = nx.spring_layout(G, seed=42)
#     nx.draw(G, pos, with_labels=True, node_size=700, font_size=8)
#     plt.title("Circuit Graph Visualization")
#     plt.show()

def visualize_graph(edge_index, node_names):
    """
    Visualizes the graph using networkx and matplotlib.
    - Bias voltage nodes (e.g., VP2, VN) shown in orange.
    - All edges shown in light gray.

    Args:
        edge_index: torch.Tensor of shape [2, num_edges] or list of (src, dst) pairs
        node_names: list of node names, index-aligned with nodes
    """
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()

    # Handle edge_index shape
    if isinstance(edge_index, torch.Tensor):
        if edge_index.dim() == 2 and edge_index.shape[0] == 2:
            edges = edge_index.t().tolist()
        else:
            raise ValueError("edge_index tensor must have shape [2, num_edges].")
    elif isinstance(edge_index, list) and isinstance(edge_index[0], (list, tuple)):
        edges = edge_index
    else:
        raise ValueError("edge_index must be a [2, N] tensor or list of edge pairs.")

    G.add_edges_from(edges)

    # Rename nodes to original names
    mapping = {i: name for i, name in enumerate(node_names)}
    G = nx.relabel_nodes(G, mapping)

    # Define node colors
    bias_keywords = []
    #TODO: need to ensure that this is actually representative of all bias voltages
    node_colors = []
    for node in G.nodes():
        if any(bias in node for bias in bias_keywords):
            node_colors.append('orange')
        else:
            node_colors.append('skyblue')

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    #TODO: Need the bias voltages to be grouped together to make graph input more readable, and to be a different color than other connections
    nx.draw_networkx_edges(G, pos, edge_color='lightgray')
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title("Circuit Graph Visualization")
    plt.axis('off')
    plt.show()


visualize_graph(edge_index, node_names)
