import torch
import torch.nn as nn


class BaseModel(nn.Module):
    def __init__(self):
        super(BaseModel, self).__init__()
        # Initialize the base model

    def forward(self, x):
        # Implement the forward pass of the base model
        pass
