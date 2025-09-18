import networkx as nx
import matplotlib.pyplot as plt
import torch
from graph_utils import build_nodes, build_edges

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

data_dict = {'netlist_name': 'single_ended1', 
             'graph': {
                 'components': {
                     'transistors': {
                         'MM12': {'type': 'pfet', 
                                  'pins': ['net12', 'Vbiasp2', 'net37', 'vdd!'], 
                                  'params': {'L': 2.52e-08, 'nfin': 5.0}, 
                                  'region': 'sub-threshold'}, 
                         'MM11': {'type': 'pfet', 
                                  'pins': ['net23', 'Vbiasp2', 'net36', 'vdd!'], 
                                  'params': {'L': 2.40e-08, 'nfin': 3.0}, 
                                  'region': 'sub-threshold'}, 
                         'MM10': {'type': 'pfet', 
                                  'pins': ['net10', 'Vbiasp2', 'net35', 'vdd!'], 
                                  'params': {'L': 2.52e-08, 'nfin': 5.0}, 
                                  'region': 'sub-threshold'}, 
                         'MM9': {'type': 'pfet', 
                                 'pins': ['Voutp', 'Vbiasp2', 'net34', 'vdd!'], 
                                 'params': {'L': 2.40e-08, 'nfin': 3.0}, 
                                 'region': 'sub-threshold'}, 
                         'MM2': {'type': 'pfet', 
                                 'pins': ['net37', 'net12', 'vdd!', 'vdd!'], 
                                 'params': {'L': 1.54e-08, 'nfin': 17.0}, 
                                 'region': 'sub-threshold'}, 
                         'MM1': {'type': 'pfet', 
                                 'pins': ['net36', 'net23', 'vdd!', 'vdd!'], 
                                 'params': {'L': 1.76e-08, 'nfin': 7.0}, 
                                 'region': 'sub-threshold'}, 
                         'MM6': {'type': 'pfet', 
                                 'pins': ['net35', 'net12', 'vdd!', 'vdd!'], 
                                 'params': {'L': 1.54e-08, 'nfin': 17.0}, 
                                 'region': 'sub-threshold'}, 
                         'MM5': {'type': 'pfet', 
                                 'pins': ['net34', 'net23', 'vdd!', 'vdd!'], 
                                 'params': {'L': 1.76e-08, 'nfin': 7.0}, 
                                 'region': 'sub-threshold'}, 
                         'MM14': {'type': 'nfet', 
                                  'pins': ['net10', 'Vbiasn2', 'net33', 'gnd!'], 
                                  'params': {'L': 1.23e-08, 'nfin': 13.0}, 
                                  'region': 'sub-threshold'}, 
                         'MM13': {'type': 'nfet', 
                                  'pins': ['Voutp', 'Vbiasn2', 'net31', 'gnd!'], 
                                  'params': {'L': 1.23e-08, 'nfin': 13.0}, 
                                  'region': 'sub-threshold'}, 
                         'MM3': {'type': 'nfet', 
                                 'pins': ['net23', 'Vinp', 'net17', 'gnd!'], 
                                 'params': {'L': 1.13e-08, 'nfin': 15.0}, 
                                 'region': 'sub-threshold'}, 
                         'MM0': {'type': 'nfet', 
                                 'pins': ['net12', 'Vinn', 'net17', 'gnd!'], 
                                 'params': {'L': 1.13e-08, 'nfin': 15.0}, 
                                 'region': 'sub-threshold'}, 
                         'MM4': {'type': 'nfet', 
                                 'pins': ['net17', 'Vbiasn0', 'gnd!', 'gnd!'], 
                                 'params': {'L': 2.04e-08, 'nfin': 9.0}, 
                                 'region': 'triode'}, 
                         'MM8': {'type': 'nfet', 
                                 'pins': ['net33', 'net10', 'gnd!', 'gnd!'], 
                                 'params': {'L': 1.18e-08, 'nfin': 7.0}, 
                                 'region': 'sub-threshold'}, 
                         'MM7': {'type': 'nfet', 
                                 'pins': ['net31', 'net10', 'gnd!', 'gnd!'], 
                                 'params': {'L': 1.18e-08, 'nfin': 7.0}, 
                                 'region': 'sub-threshold'}}, 
                     'vsources': {
                         'VS': {'type': 'vsource', 
                                'pins': ['gnd!', '0'], 
                                'params': {'value': 0}, 
                                'subtype': 'global'}, 
                         'V0': {'type': 'vsource', 
                                'pins': ['vdd!', 'gnd!'], 
                                'params': {'value': 1.0}, 
                                'subtype': 'global'}, 
                         'V2': {'type': 'vsource', 
                                'pins': ['in', 'gnd!'], 
                                'params': {'value': 0}, 
                                'subtype': 'input'}, 
                         'V1': {'type': 'vsource', 
                                'pins': ['cm', 'gnd!'], 
                                'params': {'value': 0.5},
                                'subtype': 'input'}, 
                         'Vstep': {'type': 'vsource', 
                                  'pins': ['in_tran', 'gnd!'], 
                                  'params': {'value': 0.5},
                                  'subtype': 'pulse'}, 
                         'VP2': {'type': 'vsource', 
                                 'pins': ['Vbiasp2', 'gnd!'], 
                                 'params': {'value': 0.397}, 
                                 'subtype': 'bias'}, 
                         'VN': {'type': 'vsource', 
                                'pins': ['Vbiasn0', 'gnd!'], 
                                'params': {'value': 0.395}, 
                                'subtype': 'bias'}, 
                         'VN2': {'type': 'vsource', 
                                 'pins': ['Vbiasn2', 'gnd!'], 
                                 'params': {'value': 0.390}, 
                                 'subtype': 'bias'}}, 
                     'esources': {
                        'E1': {'type': 'vcvs',
                               'pins': ['Vinp_norm', 'cm', 'in', 'gnd!'],
                               'params': {'gain': 0.5}},
                        'E0': {'type': 'vcvs',
                               'pins': ['Vinn_norm', 'cm', 'in', 'gnd!'],
                               'params': {'gain': -0.5}},
                        'E3': {'type': 'vcvs',
                               'pins': ['Vinp_tran', 'cm', 'in_tran', 'gnd!'],
                               'params': {'gain': 0.5}},
                        'E2': {'type': 'vcvs',
                               'pins': ['Vinn_tran', 'cm', 'in_tran', 'gnd!'],
                               'params': {'gain': -0.5}}},
                     'isources': {}, 
                     'resistors': {
                                'Rin1': {'type': 'resistor', 
                                        'pins': ['Vinp', 'Vinp_norm'], 
                                        'params': {'r': 1.0}}, 
                                'Rin2': {'type': 'resistor', 
                                        'pins': ['Vinp', 'Vinp_tran'], 
                                        'params': {'r': 1.0e12}},
                                'Rin3': {'type': 'resistor',
                                         'pins': ['Vinn', 'Vinn_norm'], 
                                         'params': {'r': 1.0}},
                                'Rin4': {'type': 'resistor',
                                         'pins': ['Vinn', 'Vinn_tran'], 
                                         'params': {'r': 1.0e12}},
                                'Rfeedback_p': {'type': 'resistor',
                                                'pins': ['Vinn', 'Voutp'],
                                                'params': {'r': 1.0e12}}}, 
                     'capacitors': {
                                'Ctran_p': {'type': 'capacitor',
                                            'pins': ['Vinp_tran', 'gnd!'],
                                            'params': {'c': 0}}}}, 
                 'net_to_components': {
                     'net12': {'MM6', 'MM0', 'MM12', 'MM2'}, 
                     'Vbiasp2': {'MM11', 'MM12', 'MM9', 'VP2', 'MM10'}, 
                     'net37': {'MM12', 'MM2'}, 
                     'vdd!': {'MM6', 'MM5', 'MM1', 'MM11', 'MM12', 'MM9', 'V0', 'MM2', 'MM10'}, 
                     'net23': {'MM5', 'MM3', 'MM1', 'MM11'}, 
                     'net36': {'MM1', 'MM11'}, 
                     'net10': {'MM14', 'MM7', 'MM8', 'MM10'}, 
                     'net35': {'MM6', 'MM10'}, 
                     'Voutp': {'MM9', 'MM13', 'Rfeedback_p', 'Ctran_p'}, 
                     'net34': {'MM5', 'MM9'}, 
                     'Vbiasn2': {'MM13', 'MM14', 'VN2'}, 
                     'net33': {'MM14', 'MM8'}, 
                     'gnd!': {'MM4', 'MM14', 'MM7', 'VS', 'MM13', 'V2', 'MM8', 'MM3', 'V1', 'VP2', 'VN', 'V0', 'MM0', 'VN2', 'E1', 'E0', 'Vstep', 'E3', 'E2', 'Ctran_p'}, 
                     'net31': {'MM13', 'MM7'}, 
                     'Vinp': {'MM3', 'Rin1', 'Rin2'}, 
                     'net17': {'MM4', 'MM0', 'MM3'}, 
                     'Vinn': {'MM0', 'Rfeedback_p', 'Rin3', 'Rin4'}, 
                     'Vbiasn0': {'MM4', 'VN'}, 
                     '0': {'VS'}, 
                     'in': {'V2', 'E1', 'E0'}, 
                     'in_tran': {'E3', 'E2'},
                     'cm': {'V1', 'E1', 'E0', 'E3', 'E2'},
                     'Vinp_norm': {'E1', 'Rin1'},
                     'Vinn_norm': {'E0', 'Rin3'},
                     'Vinp_tran': {'E3', 'Rin2'},
                     'Vinn_tran': {'E2', 'Rin4'}}}, 
             'sim_outputs': {
                 'specs': {'gain': 1680.0, 'ugbw': 3490000000.0, 'pm': -117.0, 'power': 5.85e-07, 'cmrr': 1000.37, 'vos': 0.02456, 'linearity': (-0.0245, 0.01456), 'out_vswing': (0.1556, 0.8678), 'i_noise': 1.34e-6, 'slew_rate': 1.24e2, 'settle_time': 0.678}, 
                 'sizing': {'nA1': 1.18e-08, 'nB1': 7.0, 'nA2': 1.23e-08, 'nB2': 13.0, 'nA3': 2.40e-08, 'nB3': 3.0, 'nA4': 1.76e-08, 'nB4': 7.0, 'nA5': 1.54e-08, 'nB5': 17.0, 'nA6': 2.52e-08, 'nB6': 5.0, 'nA7': 1.13e-08, 'nB7': 15.0, 'nA8': 2.04e-08, 'nB8': 9.0, 'vbiasp2': 0.397, 'vbiasn0': 0.395, 'vbiasn2': 0.397, 'vcm': 0.5, 'vdd': 1.0, 'tempc': 27.0}}}

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
)