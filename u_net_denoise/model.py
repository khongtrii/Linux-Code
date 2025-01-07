""""""
from typing import Tuple, Union, List

import torch
import torch.nn as nn
import torch.nn.functional as F

from module import Module
from part_module import *
""""""

class Model(Module):
    def __init__(self, image_channels: int = 3, n_channels: int = 64,
                 ch_mults: Union[Tuple[int, ...], List[int]] = (1, 2, 2, 4),
                 is_attn: Union[Tuple[bool, ...], List[bool]] = (False, False, True, True),
                 n_blocks: int = 2):
        
        super().__init__()
        n_resolutions = len(ch_mults)

        self.image_proj = nn.Conv2d(image_channels, n_channels, kernel_size=(3, 3), padding=(1, 1))
        self.time_emb = TimeEmbedding(n_channels * 4)

        down = []
        out_channels = in_channels = n_channels
        for i in range(n_resolutions):
            out_channels = in_channels * ch_mults[i]
            for _ in range(n_blocks):
                down.append(DownBlock(in_channels, out_channels, n_channels * 4, is_attn[i]))
                in_channels = out_channels
            if i < n_resolutions - 1:
                down.append(Downsample(in_channels))
        self.down = nn.ModuleList(down)

        self.middle = MiddleBlock(out_channels, n_channels * 4)

        up = []
        in_channels = out_channels
        for i in reversed(range(n_resolutions)):
            out_channels = in_channels
            for _ in range(n_blocks):
                up.append(UpBlock(in_channels, out_channels, n_channels * 4, is_attn[i]))
            out_channels = in_channels // ch_mults[i]
            up.append(UpBlock(in_channels, out_channels, n_channels * 4, is_attn[i]))
            in_channels = out_channels
            if i > 0:
                up.append(Upsample(in_channels))
        self.up = nn.ModuleList(up)

        self.norm = nn.GroupNorm(8, n_channels)
        self.act = Swish()
        self.final = nn.Conv2d(in_channels, image_channels, kernel_size=(3, 3), padding=(1, 1))

    def forward(self, x: torch.Tensor, t: torch.Tensor):
        t = self.time_emb(t)
        x = self.image_proj(x)
        h = [x]

        for m in self.down:
            x = m(x, t)
            h.append(x)

        x = self.middle(x, t)

        for m in self.up:
            if isinstance(m, Upsample):
                x = m(x, t)
            else:
                s = h.pop()

                if x.size(2) != s.size(2) or x.size(3) != s.size(3):
                    x = F.interpolate(x, size=(s.size(2), s.size(3)), mode='bilinear', align_corners=True)
                
                x = torch.cat((x, s), dim=1)
                x = m(x, t)

        return self.final(self.act(self.norm(x)))

def count_parameters(model):
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    non_trainable_params = sum(p.numel() for p in model.parameters() if not p.requires_grad)
    trainable_params, non_trainable_params = "{:,}".format(trainable_params), "{:,}".format(non_trainable_params)
    print(f"Unet model: {model}")
    print(f"Trainable parameters: {trainable_params}")
    print(f"Non-trainable parameters: {non_trainable_params}")

def load_model(url: str, model, optimizer, check: bool = True):
    assert url.endswith(".pth"), "This is not a checkpoint file !!!"
    
    if check:
        checkpoint = torch.load(url)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    else:
        print(f"Check = {check}, so no model loaded !!!")

# if __name__ == "__main__":
#     device = torch.device('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')

#     def count_parameters(model):
#         trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
#         non_trainable_params = sum(p.numel() for p in model.parameters() if not p.requires_grad)
#         return trainable_params, non_trainable_params

#     model = Model(image_channels=1).to(device=device)
#     trainable, non_trainable = count_parameters(model)
#     trainable, non_trainable = "{:,}".format(trainable), "{:,}".format(non_trainable)
#     print(f"Unet model: {model}")
#     print(f"Trainable parameters: {trainable}")
#     print(f"Non-trainable parameters: {non_trainable}")