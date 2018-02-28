import json
import nn.model as model


def train(datapath):
    fin = open(datapath, 'r')
    data = []
    line = fin.readline()
    while line:
        data.append(json.loads(line))
        line = fin.readline()


