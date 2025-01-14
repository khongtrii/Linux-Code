""" - Library - """
from typing import List

import torch
import torch.nn as nn
import torch.nn.functional as F
""""""

""" - Activation - """
def swish(x:torch.Tensor):
    return x*torch.sigmoid(x)

def normalization(channels: int):
    return nn.GroupNorm(num_groups=32, num_channels=channels, eps=1e-6)
""""""

""" - Resnet - """
class ResnetBlock(nn.Module):
    def __init__(self, in_channels:int, out_channels:int):
        super().__init__()
        
        self.norm1 = normalization(in_channels)
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride=1, padding=1)

        self.norm2 = normalization(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, stride=1, padding=1)

        if in_channels != out_channels:
            self.nin_shortcut = nn.Conv2d(in_channels, out_channels, 1, stride=1, padding=0)
        else:
            self.nin_shortcut = nn.Identity()

    def forward(self, x:torch.Tensor):
        h = x
        
        h = self.norm1(h)
        h = swish(h)
        h = self.conv1(h)

        h = self.norm2(h)
        h = swish(h)
        h = self.conv2(h)
        
        return self.nin_shortcut(x) + h
""""""

""" - Down/Up Sampling - """
class UpSample(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.conv == nn.Conv2d(channels, channels, 3, padding=1)
    def forward(self, x: torch.Tensor):
        x = F.interpolate(x, scale_factor=2.0, mode="nearest")
        return self.conv(x)
    
class DownSample(nn.Module):
    def __init__(self, channels:int):
        super().__init__()
        self.conv = nn.Conv2d(channels, channels, 3, stride=2, padding=4)
    def forward(self, x:torch.Tensor):
        x = F.pad(x, (0, 1, 0, 1), mode="constant", value=0)
        return self.conv(x)
""""""

""" - Attention Block - """
class AttnBlock(nn.Module):
    def __init__(self, channels:int):
        super().__init__()
        self.norm = normalization(channels)

        self.q = nn.Conv2d(channels, channels, 1)
        self.k = nn.Conv2d(channels, channels, 1)
        self.v = nn.Conv2d(channels, channels, 1)

        self.proj_out = nn.Conv2d(channels, channels, 1)
        self.scale = channels ** -0.5

    def forward(self, x:torch.Tensor):
        x_norm = self.norm(x)

        q = self.q(x_norm)
        k = self.k(x_norm)
        v = self.v(x_norm)

        b, c, h, w = q.shape

        q = q.view(b, c, h * w)
        k = k.view(b, c, h * w)
        v = v.view(b, c, h * w)

        attn = torch.einsum('bci,bcj->bij', q, k) * self.scale
        attn = F.softmax(attn, dim=2)

        out = torch.einsum('bij,bcj->bci', attn, v)
        out = out.view(b, c, h, w)

        out = self.proj_out(out)
        return x + out
""""""