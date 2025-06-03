import torch
from torch_geometric.loader import DataLoader
import pickle

from graph_dataset import GraphDataset
from graph_model import GraphTransformerModel

# Load graph data
with open("compiled_graphs.pkl", "rb") as f:
    graph_dicts = pickle.load(f)

# define edge types (should match graph)
EDGE_TYPE_VOCAB = {
    "G->D": 0, "D->G": 1,
    "G->S": 2, "S->G": 3,
    "G->bias": 4, "bias->G": 5,
    "D->S": 6, "S->D": 7,
    "D->VDD": 8, "S->VDD": 9, "B->VDD": 10,
    "D->GND": 11, "S->GND": 12, "B->GND": 13,
    "G->vout": 14, "D->vout": 15,"S->vout": 16,
    "UNK->UNK": 99
}

# Create dataset and dataloader
dataset = GraphDataset(graph_dicts, EDGE_TYPE_VOCAB)
loader = DataLoader(dataset, batch_size=1, shuffle=True)

model = GraphTransformerModel(
    node_feat_dim=6,   # match input features
    edge_type_vocab_size=max(EDGE_TYPE_VOCAB.values())+1,
    hidden_dim=64,
    out_dim=2  # predicting [L, W]
)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = torch.nn.MSELoss()

print("Max edge_attr ID in dataset:", max([int(e.max()) for e in [g["edge_attr"] for g in graph_dicts]]))
print("Embedding vocab size:", len(EDGE_TYPE_VOCAB))

for epoch in range(50):
    model.train()
    total_loss = 0

    for batch in loader:
        optimizer.zero_grad()
        pred = model(batch)            # shape: [num_nodes, 2]
        loss = loss_fn(pred, batch.y)  # y shape: [num_nodes, 2]
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"Epoch {epoch:03d} | Loss: {total_loss:.6f}")

torch.save(model.state_dict(), "graph_model.pt") 

model.load_state_dict(torch.load("graph_model.pt"))
model.eval()