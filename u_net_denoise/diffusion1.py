from typing import Tuple, Optional

import torch
import torch.nn.functional as F
import torch.utils.data
from torch import nn

from labml_nn.diffusion.ddpm.utils import gather
from part_module import cosine_schedule

device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.mps.is_available() else 'cpu'

class DenoiseDiffusion:
    def __init__(self, eps_model: nn.Module,  n_steps: int, device: torch.device):
        super().__init__()
        self.eps_model = eps_model

        steps = torch.randint(0, n_steps, (64, ), device=device)
        # self.beta = 0.02 + 0.5 * (1e-4 - 0.02) * (1 + torch.cos(3.14159 * steps / n_steps))  
        # self.beta = beta.sort()
        # self.alpha = 1. - self.beta
        # beta_values, _ = self.beta.sort()  # Chỉ lấy giá trị đã sắp xếp, không cần chỉ số
        self.beta = torch.linspace(0.0001, 0.02, n_steps).to(device)
        
        self.alpha = 1. - self.beta
        self.alpha_bar = torch.cumprod(self.alpha, dim=0).to(device)

        self.n_steps = n_steps
        self.sigma2 = self.beta

    def q_xt_x0(self, x0: torch.Tensor, t: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        mean = gather(self.alpha_bar, t) ** 0.5 * x0
        var = 1 - gather(self.alpha_bar, t)
        return mean, var
    
    def q_sample(self, x0: torch.Tensor, t: torch.Tensor, eps: Optional[torch.Tensor] = None):
        if eps is None:
            eps = torch.randn_like(x0)

        mean, var = self.q_xt_x0(x0, t)
        return mean + (var ** 0.5) * eps
    
    def p_sample(self, xt: torch.Tensor, t: torch.Tensor):
        eps_theta = self.eps_model(xt, t)
        alpha_bar = gather(self.alpha_bar, t)
        alpha = gather(self.alpha, t)
        eps_coef = (1 - alpha) / (1 - alpha_bar) ** 0.5
        mean = 1 / (alpha ** 0.5) * (xt - eps_coef * eps_theta)
        var = gather(self.sigma2, t)
        eps = torch.randn(xt.shape, device=xt.device)
        return mean + (var ** 0.5) * eps
    
    def loss(self, x0: torch.Tensor, noise: Optional[torch.Tensor] = None):
        batch_size = x0.shape[0]
        t = torch.randint(0, self.n_steps, (batch_size, ), device=x0.device, dtype=torch.long)
        if noise is None:
            noise = torch.randn_like(x0)

        xt = self.q_sample  (x0, t, eps=noise)
        eps_theta = self.eps_model(xt, t)
        return F.mse_loss(noise, eps_theta)
