from your_netlist_parser import parse_netlist_general
from your_feature_gen import generate_node_features
from train_poc import train_graph
import json

# Load files
with open("example_netlist.scs") as f:
    netlist_str = f.read()

with open("data.json") as f:
    metadata = json.load(f)

component_info = metadata["graph"]["components"]
target_gain = torch.tensor([metadata["specs"]["gain"]], dtype=torch.float)

# Parse netlist → graph
edge_index, node_names, _ = parse_netlist_general(netlist_str)

# Generate node features
x, ordered_names = generate_node_features(component_info)

# Match feature order
assert node_names == ordered_names, "Name order mismatch!"

# Build graph
graph_data = Data(x=x, edge_index=edge_index)

# Train model
train_graph(graph_data, target_gain)
