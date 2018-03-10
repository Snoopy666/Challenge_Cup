import json
import torch
from torch import nn
import network.model as model
import network.feature as feature
import configparser
from torch import optim
from torch.autograd import Variable
import torch.nn.functional as F
from sklearn.metrics import classification_report as report


def train(configpath, datapath, classes, usegpu):
    config = configparser.ConfigParser()
    config.read(configpath)
    getdata = feature.transformer(config, datapath)

    print('building net...')
    net = model.LSTM(config, classes)
    if usegpu:
        net = net.cuda()
    optimer = optim.Adam(net.parameters(), lr = config.getfloat('train', 'learning_rate'))
    criterion = nn.CrossEntropyLoss()

    print('brgin training ...')
    for epoch in range(config.getint('train', 'epoch')):
        print('epoch:', epoch)
        trueTag = []
        predTag = []
        while True:
            data = getdata.get_data()
            if data is None:
                break

            traindata, label0 = data
            if usegpu:
                traindata = Variable(torch.Tensor(traindata).cuda())
                label = Variable(torch.LongTensor(label0).cuda())
            else:
                traindata = Variable(torch.Tensor(traindata))
                label = Variable(torch.LongTensor(label0))

            net.init_hidden(usegpu)
            output = net.forward(traindata)
            # print(output.size())

            loss = 0

            _, pred = torch.max(output, 2)

            for i, l in enumerate(label0):

                trueTag += l
                predTag += pred[i].data.tolist()

            for i, seq in enumerate(output):
                # print(seq.size())
                # print(label)
                loss += criterion(seq, label[i])
            # print(loss)
            optimer.zero_grad()
            loss.backward()
            optimer.step()
        print('train result')
        print(report(trueTag, predTag))
        print('test result')
        test(config, net, '/Users/Smart/Desktop/code/Challenge_Cup/test.json', usegpu)

def test(config, model, datapath, usegpu):
    getdata = feature.transformer(config, datapath)

    trueTag = []
    predTag = []
    while True:
        data = getdata.get_data()
        if data is None:
            break

        data0, label0 = data
        if usegpu:
            testdata = Variable(torch.Tensor(data0).cuda())
            # label = Variable(torch.LongTensor(label0).cuda())
        else:
            testdata = Variable(torch.Tensor(data0))
            # label = Variable(torch.LongTensor(label0))

        model.init_hidden(usegpu)
        output = model.forward(testdata)
        _, pred = torch.max(output, 2)

        for i, l in enumerate(label0):
            trueTag += l
            predTag += pred[i].data.tolist()

    print(report(trueTag, predTag))

