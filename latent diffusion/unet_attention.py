from typing import Optional

import torch
import torch.nn.functional as F
from torch import nn


# class GeGLU()

class SpatialTransformer(nn.Module):
    def __init__(self, channels: int, n_heads: int, n_layers: int, d_cond: int):
        super().__init__()

        self.norm = nn. GroupNorm(32, channels, 1e-6, True)
        self.proj_in = nn.Conv2d(channels, channels, kernel_size=1, stride=1, padding=0)

        self.transformer_blocks = nn.ModuleList(
            
        )