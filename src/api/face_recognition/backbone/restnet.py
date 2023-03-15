import torch
from torch import nn
from torch.utils import checkpoint

def conv3x3_layer(in_channel, out_channel, stride=1, groups=1, dilation=1):
    return nn.Conv2d(in_channel, 
                     out_channel, 
                     kernel_size=3,
                     stride=stride,
                     padding=dilation,
                     groups=groups,
                     bias=False,
                     dilation=dilation)
    
def conv1x1_layer(in_channel, out_channel, stride=1):
    return nn.Conv2d(in_channel, 
                     out_channel,
                     kernel_size=1,
                     stride=stride,
                     bias=False)

    