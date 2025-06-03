import torch
import torch.nn as nn
from torch_geometric.nn import TransformerConv, global_mean_pool

class SimpleGraphormer(nn.Module): # designs curstom NN class
    def __init__(self, in_channels, hidden_dim, out_dim, num_heads=4, num_layers=3):
        '''
        in_channels: Size of input node feature vectors (5 in your case).

        hidden_dim: Dimensionality of the hidden layers.

        out_dim: Final output size (1 for predicting gain).

        num_heads: Number of attention heads in each TransformerConv layer.

        num_layers: Number of TransformerConv layers.
        '''
        super().__init__()
        self.layers = nn.ModuleList()
        self.layers.append(TransformerConv(in_channels, hidden_dim, heads=num_heads)) # it takes the 5D input features and projects them into a new space of size hidden_dim * num_heads
        for _ in range(num_layers - 1): 
            self.layers.append(TransformerConv(hidden_dim * num_heads, hidden_dim, heads=num_heads)) # layers (from 2 to num_layers) that operate on the output of the previous layer

        self.pool = global_mean_pool #  pooling (averages all node embeddings to get a graph-level representation)
        self.mlp = nn.Sequential(
            nn.Linear(hidden_dim * num_heads, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim)
        ) # process the pooled graph representation

    def forward(self, x, edge_index, batch): # main logic that runs during model execution
        for layer in self.layers: # applies
            x = layer(x, edge_index)
        x = self.pool(x, batch)
        return self.mlp(x)

model = SimpleGraphormer(in_channels=5, hidden_dim=64, out_dim=1)  # 5 features per node
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

for epoch in range(100):
    model.train()
    total_loss = 0
    for batch in loader:
        batch = batch.to('cuda' if torch.cuda.is_available() else 'cpu')
        optimizer.zero_grad()
        out = model(batch.x, batch.edge_index, batch.batch)
        loss = loss_fn(out.view(-1), batch.y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch}: Loss {total_loss:.4f}")
