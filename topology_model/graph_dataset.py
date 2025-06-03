from torch_geometric.data import Data, Dataset
import torch
"""
    Input = graph + node features + specs
    Output = predicted sizing
"""
class GraphDataset(Dataset):
    def __init__(self, graph_dicts, edge_type_vocab):
        super().__init__()
        self.graph_dicts = graph_dicts
        self.edge_type_vocab = edge_type_vocab
    def __len__(self):
        return len(self.graph_dicts)
    def __getitem__(self, idx):
        g = self.graph_dicts[idx]
        x = torch.tensor(g["node_features"], dtype=torch.float)
        # edge_index = torch.tensor(g["edge_index"], dtype=torch.long).t().contiguous()
        edge_index = g["edge_index"]
        # edge_attr_str = g["edge_attr"]
        # edge_attr = torch.tensor(
        #     [self.edge_type_vocab.get(e, self.edge_type_vocab["UNK->UNK"]) for e in edge_attr_str],
        #     dtype=torch.long
        # )
        # {
        # "x": node_features,              # torch.Tensor [num_nodes, 6]
        # "edge_index": edge_index,        # torch.LongTensor [2, num_edges]
        # "edge_attr": edge_attr_tensor,   # torch.LongTensor [num_edges]
        # "spec": spec_tensor,             # torch.FloatTensor [4] (gain, UGBW, PM, power)
        # "y": sizing_targets              # torch.FloatTensor [num_nodes, 2] (L, W)
        # }
        edge_attr = g["edge_attr"]
        y = torch.tensor(g["sizing_targets"], dtype=torch.float)  # shape [num_nodes, 2]
        spec = torch.tensor(g["spec"], dtype=torch.float)         # shape [4]
        print(Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y, spec=spec))
        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y, spec=spec)
    