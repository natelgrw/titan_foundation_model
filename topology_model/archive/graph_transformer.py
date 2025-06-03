# graph_transformer.py
import torch
import torch.nn as nn
from torch_geometric.nn import TransformerConv, global_mean_pool

class GraphTransformer(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers=3):
        super(GraphTransformer, self).__init__()
        self.convs = nn.ModuleList()

        self.convs.append(TransformerConv(in_channels, hidden_channels))
        for _ in range(num_layers - 2):
            self.convs.append(TransformerConv(hidden_channels, hidden_channels))
        self.convs.append(TransformerConv(hidden_channels, hidden_channels))

        self.lin = nn.Sequential(
            nn.Linear(hidden_channels, hidden_channels),
            nn.ReLU(),
            nn.Linear(hidden_channels, out_channels)  # final output (e.g., 1 for reward)
        )

    def forward(self, x, edge_index, batch):
        for conv in self.convs:
            x = conv(x, edge_index)
            x = torch.relu(x)

        # Graph-level pooling
        x = global_mean_pool(x, batch)  # size: [num_graphs, hidden_channels]
        return self.lin(x)

from torch_geometric.data import Data

# Your node_feats, edge_index from earlier
data = Data(x=node_feats, edge_index=edge_index, y=torch.tensor([reward]), batch=torch.zeros(node_feats.size(0), dtype=torch.long))

model = GraphTransformer(in_channels=5, hidden_channels=64, out_channels=1)
out = model(data.x, data.edge_index, data.batch)
print("Predicted:", out)
