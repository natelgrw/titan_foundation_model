import torch
from torch_geometric.data import Data

'''

'''

# Data(
#     x=node_features,         # shape [num_nodes, node_feat_dim]
#     edge_index=edge_index,   # shape [2, num_edges]
#     edge_attr=edge_attr,     # shape [num_edges] or [num_edges, edge_feat_dim]
#     y=target_sizing,         # shape [num_targets]
#     spec=spec_vector         # shape [spec_dim]
# )

# def voltage_as_node(name, pins):
#     '''
#     Returns true if voltage is either input or bias voltage 
#     '''
#     for pin in pins:
#         if any(keyword in pin.lower() for keyword in ["vdd", "gnd", "0", "vout"]):
#             return False
#     if any(keyword in name.lower() for keyword in ["bias", "in", "vinp", "vinn", "cm"]):
#         return True
#     return False

PIN_ROLES = {
    "nfet": ["D", "G", "S", "B"],
    "pfet": ["D", "G", "S", "B"],
    "vsource": ["+", "-"]
}
def get_pin_role(component, net):
    ctype = component["type"]
    pins = component["pins"]
    roles = PIN_ROLES.get(ctype, [])
    for i, pin in enumerate(pins):
        if pin == net and i < len(roles):
            return roles[i]
    return "UNK"

def dict_to_graph_data(data_dict, target_spec='gain'):
    components = data_dict["graph"]["components"]
    net_map = data_dict["graph"]["net_to_components"]
    specs = data_dict["sim_outputs"]["specs"]

    all_comps = {}
    for group in components.values():
        all_comps.update(group)
    node_names = node_names = []
    for name, comp in all_comps.items():
        ctype = comp.get("type", "")
        subtype = comp.get("subtype", "")
        if ctype in {"nfet", "pfet"}:
            node_names.append(name)
        elif ctype == "vsource" and subtype in {"bias", "input"}:
            node_names.append(name)
    name_to_idx = {name: i for i, name in enumerate(node_names)}
    
    type_map = {
        'nfet': 0, 'pfet': 1, 'vsource': 2, 'isource': 3, 'resistor': 4, 'capacitor': 5
    } # types of components
    region_map = {
        'sub-threshold': 0, 'triode': 1, 'saturation': 2, None: -1
    } # for each transistor components, states RoOp
    voltage_map = {
        'bias': 0, 'input': 1, 'supply': 2, None: -1
    }

    node_feats = []
    for name in node_names:
        comp = all_comps[name]
        ctype = comp["type"]
        subtype = comp.get("subtype", None)
        if ctype == "vsource" and subtype not in {"bias", "input"}:
            continue
        region = comp.get("region", None)
        params = comp.get("params", {})
        t_idx = type_map.get(ctype, -1) # putting type as a number
        r_idx = region_map.get(region, -1) # putting region as a number
        v_idx = voltage_map.get(subtype, -1) # putting voltage type as a numver
        L = float(params.get("L", 0.0)) # length if transistor
        W = float(params.get("W", 0.0)) # width if transistor
        val = float(params.get("value", 0.0)) if isinstance(params.get("value", 0.0), (float, int)) else 0.0 # value is resistance/capacitance/value associated with source
        comp["type"] == "vsource" and comp["subtype"] in {"bias", "input"}
        node_feats.append([t_idx, r_idx, v_idx, L, W, val])
        #TODO, LIKELY WANT TO APPEND TO NODE FEATURES FOR SUPPLY VOLTAGES
        # print(name)
        # print(node_feats[-1])
    x = torch.tensor(node_feats, dtype=torch.float) # crears a tensor type (32 floating point number)

    # edges = set()
    edge_attr = []
    edge_names= []
    edge_nets = []
    global_nets = {"gnd!", "vdd!", "0"}
    node_names.append("VDD")
    node_names.append("GND")
    name_to_idx["VDD"] = len(name_to_idx)
    name_to_idx["GND"] = len(name_to_idx)

    output_nets = {"Vout", "Voutp"}
    for net, comps in net_map.items(): # getting nets and the components they're connected to
        if net in global_nets: # skipping global voltages
            continue
        comp_list = list(comps)
        for i in range(len(comp_list)): # checking all the components against the rest of the components in the list
            for j in range(i + 1, len(comp_list)):
                src = name_to_idx.get(comp_list[i]) # the start of the connection (src)
                tgt = name_to_idx.get(comp_list[j]) # end of the connection (trgt)
                if src is None or tgt is None:
                    continue
                name1 = comp_list[i]
                name2 = comp_list[j]
                comp1 = all_comps[name1]
                comp2 = all_comps[name2]
                role1 = get_pin_role(comp1, net)
                role2 = get_pin_role(comp2, net)
                if net in output_nets:
                    edge_type = f"{role1}->vout"
                else:
                    edge_type = f"{role1}->{role2}"
                edge_names.append([src, tgt])
                edge_attr.append(edge_type)

                #FOR TESTING PURPOSES (TESTING EDGE ATTRIBUTE IDS)
                EDGE_TYPE_VOCAB = {
                "G->D": 0, "D->G": 1,
                "G->S": 2, "S->G": 3,
                "G->bias": 4, "bias->G": 5,
                "D->S": 6, "S->D": 7,
                "D->VDD": 8, "S->VDD": 9, "B->VDD": 10,
                "D->GND": 11, "S->GND": 12, "B->GND": 13,
                "G->vout": 14, "D->vout": 15,"S->vout": 16,
                "UNK->UNK": 99}
                #TODO NEED TO SOMEHOW IDENTIFY VOLTAGE -> TRANSISTOR PART CONNECTIONS
                edge_attr_ids = []
                edge_attr_ids.append(EDGE_TYPE_VOCAB.get(edge_attr[-1], EDGE_TYPE_VOCAB["UNK->UNK"]))
                print(name1, name2)
                print(edge_attr[-1])
                print(edge_attr_ids[-1])

                edge_nets.append(net)

    for name, comp in all_comps.items():
        ctype = comp.get("type", "")
        subtype = comp.get("subtype", None)
        pins = comp.get("pins", [])
        # ONLY FOR CONNECTING GND AND VDD CONNECTIONS
        if ctype == "vsource" and voltage_map.get(subtype, -1) == 2:
            continue  # already excluded
        if name not in name_to_idx:
            continue  # not in your graph
        for i, pin in enumerate(pins):
            if pin == "vdd!":
                role = get_pin_role(comp, pin)
                edge_type = f"{role}->VDD"
                edge_names.append([name_to_idx[name], name_to_idx["VDD"]])
                edge_attr.append(edge_type)
                edge_nets.append("vdd!")
            elif pin in {"gnd!", "0"}:
                role = get_pin_role(comp, pin)
                edge_type = f"{role}->GND"
                edge_names.append([name_to_idx[name], name_to_idx["GND"]])
                edge_attr.append(edge_type)
                edge_nets.append(pin)
                

    EDGE_TYPE_VOCAB = {
    "G->D": 0, "D->G": 1,
    "G->S": 2, "S->G": 3,
    "G->bias": 4, "bias->G": 5,
    "D->S": 6, "S->D": 7,
    "D->VDD": 8, "S->VDD": 9, "B->VDD": 10,
    "D->GND": 11, "S->GND": 12, "B->GND": 13,
    "G->vout": 14, "D->vout": 15,"S->vout": 16,
    "UNK->UNK": 99}
    #TODO NEED TO SOMEHOW IDENTIFY VOLTAGE -> TRANSISTOR PART CONNECTIONS
    edge_attr_ids = [EDGE_TYPE_VOCAB.get(e, EDGE_TYPE_VOCAB["UNK->UNK"]) for e in edge_attr]

    edge_index = torch.tensor(list(edge_names), dtype=torch.long).t()

    y = torch.tensor(edge_attr_ids, dtype=torch.float)


    node_types = []
    for name in node_names:
        if name in {"VDD", "GND"}:
            continue
        comp = all_comps[name]
        ctype = comp["type"]
        subtype = comp.get("subtype", "")
        if ctype == "nfet":
            node_types.append("nfet")
        elif ctype == "pfet":
            node_types.append("pfet")
        elif ctype == "vsource" and subtype == "bias":
            node_types.append("vsource-bias")
        elif ctype == "vsource" and subtype == "input":
            node_types.append("vsource-input")
        else:
            node_types.append("other")
    node_types.append("global")  # or "supply"
    node_types.append("global")

    # return [x, edge_index, y, node_names, node_types, edge_attr, edge_nets]
    
    # return [node_feats, edge_attr, y, node_names, node_types]


from torch_geometric.data import DataLoader

list_of_circuits = [{'netlist_name': 'single_ended_cascode_current_mirror', 'graph': {'components': {'transistors': {'MM12': {'type': 'pfet', 'pins': ['net12', 'Vbiasp2', 'net37', 'vdd!'], 'params': {'L': 5.29e-07, 'W': 5.0}, 'region': 'sub-threshold'}, 'MM11': {'type': 'pfet', 'pins': ['net23', 'Vbiasp2', 'net36', 'vdd!'], 'params': {'L': 5.29e-07, 'W': 5.0}, 'region': 'sub-threshold'}, 'MM10': {'type': 'pfet', 'pins': ['net10', 'Vbiasp2', 'net35', 'vdd!'], 'params': {'L': 2.08e-07, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM9': {'type': 'pfet', 'pins': ['Voutp', 'Vbiasp2', 'net34', 'vdd!'], 'params': {'L': 2.08e-07, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM2': {'type': 'pfet', 'pins': ['net37', 'net12', 'vdd!', 'vdd!'], 'params': {'L': 6.78e-07, 'W': 3.0}, 'region': 'sub-threshold'}, 'MM1': {'type': 'pfet', 'pins': ['net36', 'net23', 'vdd!', 'vdd!'], 'params': {'L': 6.78e-07, 'W': 3.0}, 'region': 'sub-threshold'}, 'MM6': {'type': 'pfet', 'pins': ['net35', 'net12', 'vdd!', 'vdd!'], 'params': {'L': 5.41e-08, 'W': 3.0}, 'region': 'sub-threshold'}, 'MM5': {'type': 'pfet', 'pins': ['net34', 'net23', 'vdd!', 'vdd!'], 'params': {'L': 5.41e-08, 'W': 3.0}, 'region': 'sub-threshold'}, 'MM14': {'type': 'nfet', 'pins': ['net10', 'Vbiasn2', 'net33', 'gnd!'], 'params': {'L': 7.1e-08, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM13': {'type': 'nfet', 'pins': ['Voutp', 'Vbiasn2', 'net31', 'gnd!'], 'params': {'L': 7.1e-08, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM3': {'type': 'nfet', 'pins': ['net23', 'Vinp', 'net17', 'gnd!'], 'params': {'L': 6.51e-07, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM0': {'type': 'nfet', 'pins': ['net12', 'Vinn', 'net17', 'gnd!'], 'params': {'L': 6.51e-07, 'W': 6.0}, 'region': 'sub-threshold'}, 'MM4': {'type': 'nfet', 'pins': ['net17', 'Vbiasn0', 'gnd!', 'gnd!'], 'params': {'L': 4.22e-08, 'W': 5.0}, 'region': 'triode'}, 'MM8': {'type': 'nfet', 'pins': ['net33', 'net10', 'gnd!', 'gnd!'], 'params': {'L': 6.66e-08, 'W': 5.0}, 'region': 'sub-threshold'}, 'MM7': {'type': 'nfet', 'pins': ['net31', 'net10', 'gnd!', 'gnd!'], 'params': {'L': 6.66e-08, 'W': 5.0}, 'region': 'sub-threshold'}}, 'vsources': {'VS': {'type': 'vsource', 'pins': ['gnd!', '0'], 'params': {'value': '0'}, 'subtype': 'global'}, 'V0': {'type': 'vsource', 'pins': ['vdd!', 'gnd!'], 'params': {'value': 0.8}, 'subtype': 'global'}, 'V2': {'type': 'vsource', 'pins': ['in', 'gnd!'], 'params': {'value': 'type=dc'}, 'subtype': 'input'}, 'V1': {'type': 'vsource', 'pins': ['cm', 'gnd!'], 'params': {'value': 0.4}, 'subtype': 'input'}, 'VP2': {'type': 'vsource', 'pins': ['Vbiasp2', 'gnd!'], 'params': {'value': 0.216}, 'subtype': 'bias'}, 'VN': {'type': 'vsource', 'pins': ['Vbiasn0', 'gnd!'], 'params': {'value': 0.642}, 'subtype': 'bias'}, 'VN2': {'type': 'vsource', 'pins': ['Vbiasn2', 'gnd!'], 'params': {'value': 0.692}, 'subtype': 'bias'}}, 'isources': {}, 'resistors': {}, 'capacitors': {}}, 'net_to_components': {'net12': {'MM6', 'MM0', 'MM12', 'MM2'}, 'Vbiasp2': {'MM11', 'MM12', 'MM9', 'VP2', 'MM10'}, 'net37': {'MM12', 'MM2'}, 'vdd!': {'MM6', 'MM5', 'MM1', 'MM11', 'MM12', 'MM9', 'V0', 'MM2', 'MM10'}, 'net23': {'MM5', 'MM3', 'MM1', 'MM11'}, 'net36': {'MM1', 'MM11'}, 'net10': {'MM14', 'MM7', 'MM8', 'MM10'}, 'net35': {'MM6', 'MM10'}, 'Voutp': {'MM9', 'MM13'}, 'net34': {'MM5', 'MM9'}, 'Vbiasn2': {'MM13', 'MM14', 'VN2'}, 'net33': {'MM14', 'MM8'}, 'gnd!': {'MM4', 'MM14', 'MM7', 'VS', 'MM13', 'V2', 'MM8', 'MM3', 'V1', 'VP2', 'VN', 'V0', 'MM0', 'VN2'}, 'net31': {'MM13', 'MM7'}, 'Vinp': {'MM3'}, 'net17': {'MM4', 'MM0', 'MM3'}, 'Vinn': {'MM0'}, 'Vbiasn0': {'MM4', 'VN'}, '0': {'VS'}, 'in': {'V2'}, 'cm': {'V1'}}}, 'sim_outputs': {'specs': {'gain': 1680.0, 'UGBW': 3490000000.0, 'PM': -117.0, 'power': 5.85e-07, 'reward': -1.0}, 'sizing': {'nA1': 6.66e-08, 'nB1': 5.0, 'nA2': 7.1e-08, 'nB2': 6.0, 'nA3': 2.08e-07, 'nB3': 6.0, 'nA4': 5.41e-08, 'nB4': 3.0, 'nA5': 6.78e-07, 'nB5': 3.0, 'nA6': 5.29e-07, 'nB6': 5.0, 'nA7': 6.51e-07, 'nB7': 6.0, 'nA8': 4.22e-08, 'nB8': 5.0, 'vbiasp2': 0.216, 'vbiasn0': 0.642, 'vbiasn2': 0.692, 'vcm': 0.4, 'vdd': 0.8, 'tempc': 27.0}}}]


dataset = [dict_to_graph_data(example_dict) for example_dict in list_of_circuits]


# loader = DataLoader(dataset, batch_size=8, shuffle=True)

# Data(x=x, edge_index=edge_index, y=y, node_names=node_names)

"""
import networkx as nx
import matplotlib.pyplot as plt
def visualize_graph(node_names, edge_index, edge_attr, node_feats=None, node_types=None, edge_attr_str = None, edge_nets = None):
    G = nx.DiGraph()
    EDGE_TYPE_VOCAB = {
    "G->D": 0,
    "D->G": 1,
    "G->S": 2,
    "S->G": 3,
    "G->bias": 4,
    "bias->G": 5,
    "S->D": 6,
    "D->S": 7,
    "UNK->UNK": 99
    }
    ID_TO_EDGE_TYPE = {v: k for k, v in EDGE_TYPE_VOCAB.items()}
    # Add nodes with labels
    for i, name in enumerate(node_names):
        label = name
        # if node_feats:
        #     label += f"\n{node_feats[i]}"
        G.add_node(i, label=label)
    # # Add edges with labels
    # for i, (src, tgt) in enumerate(zip(edge_index[0], edge_index[1])):
    #     label = edge_attr[i] if i < len(edge_attr) else ""
    #     G.add_edge(src, tgt, label=label)

    # for i, (src, tgt) in enumerate(zip(edge_index[0], edge_index[1])):
    #     edge_type_id = edge_attr[i]
    #     label = ID_TO_EDGE_TYPE.get(edge_type_id, "UNK->UNK")
    #     G.add_edge(src, tgt, label=label)
    for i, (src, tgt) in enumerate(zip(edge_index[0], edge_index[1])):
    #     label = edge_attr_str[i] if i < len(edge_attr_str) else ""
    #     G.add_edge(src, tgt, label=label)
        edge_type = edge_attr_str[i] if i < len(edge_attr_str) else ""
        net_name = edge_nets[i] if i < len(edge_nets) else ""
        label = f"{edge_type}\n[{net_name}]"
        G.add_edge(src, tgt, label=label)
    # Choose layout
    # pos = nx.spring_layout(G, seed=42)
    pos = nx.kamada_kawai_layout(G)
    # Set colors by type
    type_to_color = {
        "nfet": "skyblue",
        "pfet": "salmon",
        "vsource-bias": "lightgreen",
        "vsource-input": "gold",
        "global": "gray",
        "other": "lightgray"
    }
    node_colors = []
    for i in range(len(node_names)):
        t = node_types[i] if node_types else "other"
        node_colors.append(type_to_color.get(t, "lightgray"))
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600)
    # Draw labels
    node_labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=7)
    # Draw edges and edge labels
    nx.draw_networkx_edges(G, pos, arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

visualize_graph(dataset[0][3], dataset[0][1].tolist(), dataset[0][2].tolist(), dataset[0][0].tolist(), dataset[0][4], dataset[0][5], dataset[0][6])
"""