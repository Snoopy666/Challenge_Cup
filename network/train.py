import json
import network.model as model
import network.feature as feature
import configparser
from torch import optim
from torch.autograd import Variable
import torch.nn.functional as F

def train(configpath, datapath, classes, usegpu):
    config = configparser.ConfigParser()
    config.read(configpath)
    data = feature.transformer(config, datapath)

    print('building net...')
    net = model.LSTM(config, classes)
    if usegpu:
        net = net.cuda()
    optimer = optim.SGD()
    criterion = nn.CrossEn