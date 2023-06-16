import torch
import numpy as np


class SnakeNNet(torch.nn.Module):
    def __init__(self, PATH="SnakeAI.pt"):
        super(SnakeNNet, self).__init__()
        self.PATH = PATH

        self.act = torch.nn.ReLU()
        self.fc1 = torch.nn.Linear(16, 64)
        self.fc2 = torch.nn.Linear(64, 64)
        self.fc3 = torch.nn.Linear(64, 4)

    def forward(self, x):
        out = self.act(self.fc1(x))

        out = self.act(self.fc2(out))

        out = self.fc3(out)
        return out
