import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import TransformerConv

class GraphTransformerModel(nn.Module):
    def __init__(self, node_feat_dim, edge_type_vocab_size, hidden_dim=64, out_dim=2):
        super().__init__()
        self.edge_emb = nn.Embedding(edge_type_vocab_size, hidden_dim)

        self.conv1 = TransformerConv(node_feat_dim, hidden_dim, edge_dim=hidden_dim)
        self.conv2 = TransformerConv(hidden_dim, hidden_dim, edge_dim=hidden_dim)

        self.output_layer = nn.Linear(hidden_dim, out_dim)

    def forward(self, data):
        x, edge_index, edge_attr = data.x, data.edge_index, data.edge_attr
        edge_attr = self.edge_emb(edge_attr)

        x = F.relu(self.conv1(x, edge_index, edge_attr))
        x = F.relu(self.conv2(x, edge_index, edge_attr))

        out = self.output_layer(x)  # shape [num_nodes, out_dim]
        return out
