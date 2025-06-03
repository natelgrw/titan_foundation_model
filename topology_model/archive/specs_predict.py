import numpy as np

sizing = {
    'nA1': 6.66e-08, 'nB1': 5.0, 'nA2': 7.1e-08, 'nB2': 6.0, 'vbiasp2': 0.216,
    'vbiasn0': 0.642, 'vbiasn2': 0.692, 'vcm': 0.4, 'vdd': 0.8, 'tempc': 27.0
}

input_vector = np.array([v for v in sizing.values()], dtype=np.float32)


import torch
import torch.nn as nn

class CircuitTransformer(nn.Module):
    def __init__(self, input_dim, d_model=64, nhead=4, num_layers=3, output_dim=3):
        super().__init__()
        self.embedding = nn.Linear(input_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model, nhead)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        self.readout = nn.Linear(d_model, output_dim)

    def forward(self, x):
        # x shape: (batch_size, input_dim)
        x = self.embedding(x).unsqueeze(1)  # (batch_size, seq_len=1, d_model)
        x = self.transformer(x)  # still (batch_size, 1, d_model)
        x = self.readout(x.squeeze(1))  # (batch_size, output_dim)
        return x
