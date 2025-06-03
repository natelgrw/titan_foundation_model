import torch
import re

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