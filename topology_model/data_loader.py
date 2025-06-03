import os
import pickle
from netlist_parser import parse_netlist
from optimizer_parser import parse_optimizer_output, combine_netlist_optimizer
from tranformer2_input import dict_to_graph_data  # the function that builds x, edge_index, edge_attr, etc.

EDGE_TYPE_VOCAB = {
    "G->D": 0, "D->G": 1, "G->S": 2, "S->G": 3,
    "G->bias": 4, "bias->G": 5,
    "D->S": 6, "S->D": 7,
    "G->vout": 8, "D->vout": 9, "S->vout": 10,
    "D->VDD": 11, "S->VDD": 12, "B->VDD": 13,
    "D->GND": 14, "S->GND": 15, "B->GND": 16,
    "UNK->UNK": 99
}

# data_dir = "/homes/hhussein/Desktop/model/data_dir/"
# netlist_dir = os.path.join(data_dir, "netlists")
# optimizer_dir = os.path.join(data_dir, "optimizer_outputs")

graph_data = []

optimizer_folder = "/homes/hhussein/Desktop/model/data_dir/optimizer_outputs"
netlist_path = "/homes/hhussein/Desktop/model/data_dir/netlists/single_ended_cascode_current_mirror.scs"
netlist = parse_netlist(netlist_path)

graph_data = []

for fname in os.listdir(optimizer_folder):
    if not fname.endswith(".txt"):
        continue

    optimizer_path = os.path.join(optimizer_folder, fname)
    optimizer_blocks = parse_optimizer_output(optimizer_path)

    for block in optimizer_blocks:
        combined = combine_netlist_optimizer(netlist, block, netlist_path)
        graph_dict = dict_to_graph_data(combined, EDGE_TYPE_VOCAB)
        graph_data.append(graph_dict)

print(f"Total samples: {len(graph_data)}")
with open("compiled_graphs.pkl", "wb") as f:
    pickle.dump(graph_data, f)