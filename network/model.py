import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import torch.optim as optim

class LSTM(nn.Module):
    def __init__(self, config, classes):
        super(LSTM, self).__init__()
        self.wordDim = config.getint('data', 'wordDim')
        self.hiddenDim = config.getint('data', 'hiddenDim')
        self.nLayers = config.getint('data', 'lstmLayer')
        self.batch_size = config.getint('data', 'batch_size')
        self.classes = classes
        self.dropout = config.getfloat('data', 'dropout')

        self.lstm = nn.LSTM(self.wordDim, self.hiddenDim, num_layers = self.nLayers, batch_first = True, dropout = self.dropout, bidirectional = False)
        self.f = nn.Linear(self.hiddenDim, self.classes)

    def init_hidden(self, useGpu):
        if useGpu:
            self.hidden = (
                torch.autograd.Variable(torch.zeros(self.nLayers, self.batch_size, self.hiddenDim).cuda()),
                torch.autograd.Variable(torch.zeros(self.nLayers, self.batch_size, self.hiddenDim).cuda())
            )
        else:
            self.hidden = (
                torch.autograd.Variable(torch.zeros(self.nLayers, self.batch_size, self.hiddenDim)),
                torch.autograd.Variable(torch.zeros(self.nLayers, self.batch_size, self.hiddenDim))
            )

    def get_loss(self, tag_predict, tag_true):
        pass

    def forward(self, x):
        # print(x.size())
        out, self.hidden = self.lstm(x, self.hidden)
        # out size batch_size * sequenceLen * hiddenDim

        out = self.f(out)

        return out


