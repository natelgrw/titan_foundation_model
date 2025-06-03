import torch
from torch_geometric.data import Data
from torch_geometric.nn import TransformerConv
import torch.nn.functional as F

class GraphTransformer(torch.nn.Module):
    def __init__(self, in_dim, hidden_dim=32, out_dim=1):
        super(GraphTransformer, self).__init__()
        self.conv1 = TransformerConv(in_dim, hidden_dim, heads=4, dropout=0.1)
        self.conv2 = TransformerConv(hidden_dim * 4, hidden_dim)
        self.out = torch.nn.Linear(hidden_dim, out_dim)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = x.mean(dim=0)  # Global pooling
        return self.out(x)

def train_graph(graph_data, target_value):
    model = GraphTransformer(in_dim=graph_data.num_node_features)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
    loss_fn = torch.nn.MSELoss()

    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        out = model(graph_data.x, graph_data.edge_index)
        loss = loss_fn(out, target_value)
        loss.backward()
        optimizer.step()
        if epoch % 10 == 0:
            print(f"Epoch {epoch} | Loss: {loss.item():.4f}")

    print("Final Prediction:", model(graph_data.x, graph_data.edge_index).item())
    print("Target:", target_value.item())
