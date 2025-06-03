import torch
from torch_geometric.data import Data

PIN_ROLES = {
    # Identifying which pin of the component
    "nfet": ["D", "G", "S", "B"],
    "pfet": ["D", "G", "S", "B"],
    "vsource": ["+", "-"],
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

def build_nodes(data_dict):
    """
    Node features and sizing targets from a parsed netlist/optimizer data.
    Returns:
        - x (Tensor): node features [num_nodes, 6] row is [component_type, region_type, voltage_type, L, W, value] (2D tensor)
        - sizing_targets (Tensor): [L, W] sizing targets for each node (needed to train model, so that it learns correlation)
        - node_names (List[str]): list of component names (used for edges)
        - name_to_idx (Dict[str, int]): maps component name to node index 
    """
    components = data_dict["graph"]["components"]
    sizing = data_dict["sim_outputs"]["sizing"]
    all_comps = {}
    for group in components.values():
        all_comps.update(group)
    # define encoding maps for component, region, and voltage type
    type_map = {
        'nfet': 0, 'pfet': 1, 'vsource': 2, 'vcvs': 3,
        'isource': 4, 'resistor': 5, 'capacitor': 6
    }
    region_map = {'sub-threshold': 0, 'triode': 1, 'saturation': 2, None: -1}
    voltage_map = {'bias': 0, 'input': 1, 'supply': 2, None: -1}
    node_names = []
    node_feats = []
    sizing_targets = []
    # including only components for model (transistors, input/bias sources, vcvs)
    for name, comp in all_comps.items():
        ctype = comp.get("type", "")
        subtype = comp.get("subtype", "")
        #TODO: check to see if it is ok to omit the input voltages as vcvs, because that's what is connected?
        if ctype in {"nfet", "pfet"} or (ctype == "vsource" and subtype in {"bias", "input"}) or ctype == "vcvs":
            node_names.append(name)
    # global sources as nodes
    node_names += ["VDD", "GND"]
    name_to_idx = {name: i for i, name in enumerate(node_names)}
    for name in node_names:
        if name in {"VDD", "GND"}:
            # special dummy features for global nodes
            node_feats.append([99, -1, 2, 0.0, 0.0, 0.0])
            sizing_targets.append([0.0, 0.0])
            continue
        comp = all_comps[name]
        ctype = comp["type"]
        subtype = comp.get("subtype", None)
        region = comp.get("region", None)
        params = comp.get("params", {})
        t_idx = type_map.get(ctype, -1)
        r_idx = region_map.get(region, -1)
        v_idx = voltage_map.get(subtype, -1)
        # L/W can be direct or string references to sizing dict
        L = float(sizing.get(params.get("L"), 0.0)) if isinstance(params.get("L"), str) else float(params.get("L", 0.0))
        W = float(sizing.get(params.get("W"), 0.0)) if isinstance(params.get("W"), str) else float(params.get("W", 0.0))
        # value used for vsources, gain for vcvs
        val = float(params.get("gain", params.get("value", 0.0)))
        node_feats.append([t_idx, r_idx, v_idx, L, W, val])
        if ctype in {"nfet", "pfet"}:
            sizing_targets.append([L, W])
        else:
            sizing_targets.append([0.0, 0.0])  # no sizing for other node types
    x = torch.tensor(node_feats, dtype=torch.float)
    sizing_target_tensor = torch.tensor(sizing_targets, dtype=torch.float)
    return x, sizing_target_tensor, node_names, name_to_idx

def build_edges(data_dict, node_names, name_to_idx, edge_type_vocab):
    """
    Edge indices and edge attribute tensor type from net_to_component map
    Returns:
        - edge_index (Tensor): shape [2, num_edges], indicating connections between nodes
        - edge_attr_tensor (Tensor): encoded edge types as tensor
    """
    components = data_dict["graph"]["components"]
    net_map = data_dict["graph"]["net_to_components"]
    all_comps = {}
    for group in components.values():
        all_comps.update(group)
    output_nets = {"Vout", "Voutp"}
    global_nets = {"gnd!", "vdd!", "0"}
    edge_names = []
    edge_attr = []
    # Build inter-component edges through shared nets
    for net, comps in net_map.items():
        if net in global_nets:
            continue  # handled separately later
        comp_list = list(comps)
        for i in range(len(comp_list)):
            for j in range(i + 1, len(comp_list)):
                src, tgt = comp_list[i], comp_list[j]
                if src not in name_to_idx or tgt not in name_to_idx:
                    continue
                role1 = get_pin_role(all_comps[src], net)
                role2 = get_pin_role(all_comps[tgt], net)
                edge_type = f"{role1}->vout" if net in output_nets else f"{role1}->{role2}"
                edge_names.append([name_to_idx[src], name_to_idx[tgt]])
                edge_attr.append(edge_type)
    # Add edges from components to supply nodes (VDD, GND)
    for name, comp in all_comps.items():
        if name not in name_to_idx:
            continue
        pins = comp.get("pins", [])
        for pin in pins:
            if pin == "vdd!":
                role = get_pin_role(comp, pin)
                edge_names.append([name_to_idx[name], name_to_idx["VDD"]])
                edge_attr.append(f"{role}->VDD")
            elif pin in {"gnd!", "0"}:
                role = get_pin_role(comp, pin)
                edge_names.append([name_to_idx[name], name_to_idx["GND"]])
                edge_attr.append(f"{role}->GND")
    # Convert edge names and types to PyTorch tensors
    edge_index = torch.tensor(edge_names, dtype=torch.long).t()
    edge_attr_ids = [edge_type_vocab.get(e, edge_type_vocab["UNK->UNK"]) for e in edge_attr]
    edge_attr_tensor = torch.tensor(edge_attr_ids, dtype=torch.long)
    return edge_index, edge_attr_tensor
