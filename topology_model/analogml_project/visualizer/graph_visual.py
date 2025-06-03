import networkx as nx
import matplotlib.pyplot as plt
import torch
def visualize_graph(edge_index, node_names, node_features, edge_attr_tensor, edge_type_vocab):
    G = nx.DiGraph()
    # invert vocab to decode edge type IDs
    inv_edge_vocab = {v: k for k, v in edge_type_vocab.items()}

    # Add nodes
    for i, name in enumerate(node_names):
        node_type = int(node_features[i][0])
        G.add_node(i, label=name, type=node_type)

    # add edge labels (making them str instead of id)
    for i in range(edge_index.shape[1]):
        src = edge_index[0, i].item()
        tgt = edge_index[1, i].item()
        edge_type_str = inv_edge_vocab.get(edge_attr_tensor[i].item(), "UNK->UNK")
        G.add_edge(src, tgt, label=edge_type_str)

    pos = nx.spring_layout(G, seed=42)
    # Color by node type
    node_colors = [G.nodes[n]['type'] for n in G.nodes]
    cmap = plt.cm.get_cmap('tab10')
    plt.figure()
    nx.draw(
        G, pos,
        with_labels=True,
        labels={i: node_names[i] for i in G.nodes},
        node_color=node_colors,
        node_size=800,
        font_size=8,
        cmap=cmap,
        edgecolors='black'
    )
    # Edge labels
    edge_labels = {(u, v): G.edges[u, v]['label'] for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    plt.axis('off')
    plt.tight_layout()
    plt.show()


from graph.graph_input import build_nodes, build_edges

data_dict = {'netlist_name': 'single_ended_cascode_current_mirror', 'graph': {'components': {'transistors': {'MM12': {'type': 'pfet', 'pins': ['net12', 'Vbiasp2', 'net37', 'vdd!'], 'params': {'L': 5.29e-07, 'W': 5.0}, 'region': 'sub-threshold'}, 'MM11': {'type': 'pfet', 'pins': ['net23', 'Vbiasp2', 'net36', 'vdd!'], 'params': {'L': 5.29e-07, 'W': 5.0}, 'region': 'sub-threshold'}, 'MM10': {'type': 'pfet', 'pins': ['net10', 'Vbiasp2', 'net35', 'vdd!'], 'params': {'L': 2.08e-07, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM9': {'type': 'pfet', 'pins': ['Voutp', 'Vbiasp2', 'net34', 'vdd!'], 'params': {'L': 2.08e-07, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM2': {'type': 'pfet', 'pins': ['net37', 'net12', 'vdd!', 'vdd!'], 'params': {'L': 6.78e-07, 'W': 3.0}, 'region': 'sub-threshold'}, 'MM1': {'type': 'pfet', 'pins': ['net36', 'net23', 'vdd!', 'vdd!'], 'params': {'L': 6.78e-07, 'W': 3.0}, 'region': 'sub-threshold'}, 'MM6': {'type': 'pfet', 'pins': ['net35', 'net12', 'vdd!', 'vdd!'], 'params': {'L': 5.41e-08, 'W': 3.0}, 'region': 'sub-threshold'}, 'MM5': {'type': 'pfet', 'pins': ['net34', 'net23', 'vdd!', 'vdd!'], 'params': {'L': 5.41e-08, 'W': 3.0}, 'region': 'sub-threshold'}, 'MM14': {'type': 'nfet', 'pins': ['net10', 'Vbiasn2', 'net33', 'gnd!'], 'params': {'L': 7.1e-08, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM13': {'type': 'nfet', 'pins': ['Voutp', 'Vbiasn2', 'net31', 'gnd!'], 'params': {'L': 7.1e-08, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM3': {'type': 'nfet', 'pins': ['net23', 'Vinp', 'net17', 'gnd!'], 'params': {'L': 6.51e-07, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM0': {'type': 'nfet', 'pins': ['net12', 'Vinn', 'net17', 'gnd!'], 'params': {'L': 6.51e-07, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM4': {'type': 'nfet', 'pins': ['net17', 'Vbiasn0', 'gnd!', 'gnd!'], 'params': {'L': 4.22e-08, 'W': 5.0}, 'region': 'triode'}, 'MM8': {'type': 'nfet', 'pins': ['net33', 'net10', 'gnd!', 'gnd!'], 'params': {'L': 6.66e-08, 'W': 5.0}, 'region': 'sub-threshold'}, 'MM7': {'type': 'nfet', 'pins': ['net31', 'net10', 'gnd!', 'gnd!'], 'params': {'L': 6.66e-08, 'W': 5.0}, 'region': 'sub-threshold'}}, 'vsources': {'VS': {'type': 'vsource', 'pins': ['gnd!', '0'], 'params': {'value': '0'}, 'subtype': 'global'}, 'V0': {'type': 'vsource', 'pins': ['vdd!', 'gnd!'], 'params': {'value': 0.8}, 'subtype': 'global'}, 'V2': {'type': 'vsource', 'pins': ['in', 'gnd!'], 'params': {'value': 'type=dc'}, 'subtype': 'input'}, 'V1': {'type': 'vsource', 'pins': ['cm', 'gnd!'], 'params': {'value': 0.4}, 'subtype': 'input'}, 'VP2': {'type': 'vsource', 'pins': ['Vbiasp2', 'gnd!'], 'params': {'value': 0.216}, 'subtype': 'bias'}, 'VN': {'type': 'vsource', 'pins': ['Vbiasn0', 'gnd!'], 'params': {'value': 0.642}, 'subtype': 'bias'}, 'VN2': {'type': 'vsource', 'pins': ['Vbiasn2', 'gnd!'], 'params': {'value': 0.692}, 'subtype': 'bias'}}, 'isources': {}, 'resistors': {}, 'capacitors': {}}, 'net_to_components': {'net12': {'MM6', 'MM0', 'MM12', 'MM2'}, 'Vbiasp2': {'MM11', 'MM12', 'MM9', 'VP2', 'MM10'}, 'net37': {'MM12', 'MM2'}, 'vdd!': {'MM6', 'MM5', 'MM1', 'MM11', 'MM12', 'MM9', 'V0', 'MM2', 'MM10'}, 'net23': {'MM5', 'MM3', 'MM1', 'MM11'}, 'net36': {'MM1', 'MM11'}, 'net10': {'MM14', 'MM7', 'MM8', 'MM10'}, 'net35': {'MM6', 'MM10'}, 'Voutp': {'MM9', 'MM13'}, 'net34': {'MM5', 'MM9'}, 'Vbiasn2': {'MM13', 'MM14', 'VN2'}, 'net33': {'MM14', 'MM8'}, 'gnd!': {'MM4', 'MM14', 'MM7', 'VS', 'MM13', 'V2', 'MM8', 'MM3', 'V1', 'VP2', 'VN', 'V0', 'MM0', 'VN2'}, 'net31': {'MM13', 'MM7'}, 'Vinp': {'MM3'}, 'net17': {'MM4', 'MM0', 'MM3'}, 'Vinn': {'MM0'}, 'Vbiasn0': {'MM4', 'VN'}, '0': {'VS'}, 'in': {'V2'}, 'cm': {'V1'}}}, 'sim_outputs': {'specs': {'gain': 1680.0, 'UGBW': 3490000000.0, 'PM': -117.0, 'power': 5.85e-07, 'reward': -1.0}, 'sizing': {'nA1': 6.66e-08, 'nB1': 5.0, 'nA2': 7.1e-08, 'nB2': 6.0, 'nA3': 2.08e-07, 'nB3': 6.0, 'nA4': 5.41e-08, 'nB4': 3.0, 'nA5': 6.78e-07, 'nB5': 3.0, 'nA6': 5.29e-07, 'nB6': 5.0, 'nA7': 6.51e-07, 'nB7': 6.0, 'nA8': 4.22e-08, 'nB8': 5.0, 'vbiasp2': 0.216, 'vbiasn0': 0.642, 'vbiasn2': 0.692, 'vcm': 0.4, 'vdd': 0.8, 'tempc': 27.0}}}

EDGE_TYPE_VOCAB = {
                "G->D": 0, "D->G": 1,
                "G->S": 2, "S->G": 3,
                "G->bias": 4, "bias->G": 5,
                "D->S": 6, "S->D": 7,
                "D->VDD": 8, "S->VDD": 9, "B->VDD": 10,
                "D->GND": 11, "S->GND": 12, "B->GND": 13,
                "G->vout": 14, "D->vout": 15,"S->vout": 16,
                "UNK->UNK": 99}

# step 1: build nodes and edges
x, _, node_names, name_to_idx = build_nodes(data_dict)
edge_index, edge_attr_tensor = build_edges(data_dict, node_names, name_to_idx, EDGE_TYPE_VOCAB)

# Step 2: visualize
visualize_graph(
    edge_index=edge_index,
    node_names=node_names,
    node_features=x.tolist(),  # list of lists
    edge_attr_tensor=edge_attr_tensor,
    edge_type_vocab=EDGE_TYPE_VOCAB,
    title="Circuit Graph"
)