import torch

PIN_ROLES = {
    "nfet": ["D", "G", "S", "B"],
    "pfet": ["D", "G", "S", "B"],
    "vsource": ["+", "-"],
    "vcvs": ["+", "-", "inp", "inn"],  # VCVS has control + output
    "isource": ["+", "-"],
    "resistor": ["+", "-"],
    "capacitor": ["+", "-"],
}

def get_pin_role(component, net):
    ctype = component.get("type", "")
    pins = component.get("pins", [])
    roles = PIN_ROLES.get(ctype, [])
    for i, pin in enumerate(pins):
        if pin == net and i < len(roles):
            return roles[i]
    return "UNK"


def build_nodes(data_dict):
    """
    Build node features and sizing targets for all components in the netlist.
    Returns:
        - x (Tensor): node features [num_nodes, 6]
            row format: [component_type, region_type, voltage_type, L, W, value]
        - sizing_targets (Tensor): [L, W] sizing targets (only for FETs, else zeros)
        - node_names (List[str]): component names
        - name_to_idx (Dict[str, int]): map from component name to index
    """
    components = data_dict["graph"]["components"]
    sizing = data_dict["sim_outputs"]["sizing"]

    # flatten all component groups into a single dict
    all_comps = {}
    for group in components.values():
        all_comps.update(group)

    # encoding maps
    type_map = {
        'nfet': 0, 'pfet': 1, 'vsource': 2, 'vcvs': 3,
        'isource': 4, 'resistor': 5, 'capacitor': 6
    }
    region_map = {'sub-threshold': 0, 'triode': 1, 'saturation': 2, None: -1}
    voltage_map = {'bias': 0, 'input': 1, 'supply': 2, 'global': 3, None: -1}

    node_names = list(all_comps.keys())
    # add special global supply nodes
    node_names += ["VDD", "GND"]

    name_to_idx = {name: i for i, name in enumerate(node_names)}
    node_feats, sizing_targets = [], []

    for name in node_names:
        if name in {"VDD", "GND"}:
            node_feats.append([99, -1, 2, 0.0, 0.0, 0.0])
            sizing_targets.append([0.0, 0.0])
            continue

        comp = all_comps[name]
        ctype = comp.get("type", "")
        subtype = comp.get("subtype", None)
        region = comp.get("region", None)
        params = comp.get("params", {})

        t_idx = type_map.get(ctype, -1)
        r_idx = region_map.get(region, -1)
        v_idx = voltage_map.get(subtype, -1)

        # transistor sizing (L, W/NFIN), others get 0
        L = float(params.get("L", 0.0)) if "L" in params else 0.0
        NFIN = float(params.get("nfin", 0.0)) if "nfin" in params else 0.0

        # general "value" for passives/sources or "gain" for vcvs
        val = float(params.get("gain", params.get("value", 0.0)))

        node_feats.append([t_idx, r_idx, v_idx, L, NFIN, val])

        if ctype in {"nfet", "pfet"}:
            sizing_targets.append([L, NFIN])
        else:
            sizing_targets.append([0.0, 0.0])

    x = torch.tensor(node_feats, dtype=torch.float)
    sizing_target_tensor = torch.tensor(sizing_targets, dtype=torch.float)

    return x, sizing_target_tensor, node_names, name_to_idx


def build_edges(data_dict, node_names, name_to_idx, edge_type_vocab):
    """
    Build graph edges based on net connectivity.
    Returns:
        - edge_index (Tensor): shape [2, num_edges]
        - edge_attr_tensor (Tensor): edge type IDs
    """
    components = data_dict["graph"]["components"]
    net_map = data_dict["graph"]["net_to_components"]

    # flatten component dict
    all_comps = {}
    for group in components.values():
        all_comps.update(group)

    output_nets = {"Vout", "Voutp"}
    global_nets = {"gnd!", "vdd!", "0"}

    edge_names, edge_attr = [], []

    # connect components through shared nets
    for net, comps in net_map.items():
        if net in global_nets:
            continue
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

    # connect components to global supply nodes
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

    edge_index = torch.tensor(edge_names, dtype=torch.long).t()
    edge_attr_ids = [edge_type_vocab.get(e, edge_type_vocab["UNK->UNK"]) for e in edge_attr]
    edge_attr_tensor = torch.tensor(edge_attr_ids, dtype=torch.long)

    return edge_index, edge_attr_tensor