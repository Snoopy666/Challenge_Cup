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
import numpy as np
import network.LSTM_CRF as lc


def train_LC(configpath, datapath, classes, usegpu):
    config = configparser.ConfigParser()
    config.read(configpath)
    getdata = feature.transformer(config, datapath)

    print('building net...')
    net = lc.BiLSTM_CRF(config, classes, usegpu)

    if usegpu:
        net = net.cuda()
    optimer = optim.Adam(net.parameters(), lr = config.getfloat('train', 'learning_rate'))
    for epoch in range(config.getint('train', 'epoch')):
        print('epoch:', epoch)
        while True:
            data = getdata.get_data()
            if data is None:
                break

            traindata, label0, seqlen = data
            if usegpu:
                traindata = Variable(torch.Tensor(traindata).cuda())
                label = Variable(torch.LongTensor(label0).cuda())
            else:
                traindata = Variable(torch.Tensor(traindata))
                label = Variable(torch.LongTensor(label0))

            loss = net.neg_log_likelihood(traindata, label)
            loss.backward()
            optimer.step()

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

    print('begin training ...')
    for epoch in range(config.getint('train', 'epoch')):
        print('epoch:', epoch)
        trueTag = []
        predTag = []
        while True:
            data = getdata.get_data()
            if data is None:
                break

            traindata, label0, seqlen = data

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

            # print(output.size())
            for i, seq in enumerate(output):
                # print(seq.size())
                # print(label[i])
                # print(seq.size())
                for j, l in enumerate(label[i]):
                    # print(seq[j])
                    if l.data.tolist()[0] == 0:
                        loss += 0.05 * criterion(seq[j].view(1, -1), l)
                    else:
                        loss += criterion(seq[j].view(1, -1), l)
            # print(loss)
            optimer.zero_grad()
            loss.backward()
            optimer.step()
        print('train result')
        # print(trueTag)
        # print(predTag)
        print(report(trueTag, predTag))
        print('test result')
        test(config, net, '/Users/Smart/Desktop/code/Challenge_Cup/test1.json', usegpu)

def test(config, model, datapath, usegpu):
    getdata = feature.transformer(config, datapath)

    trueTag = []
    predTag = []
    while True:
        data = getdata.get_data()
        if data is None:
            break

        data0, label0, seqlen = data
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


def train_LSTM_CRF(configPath, datapath, classes, usegpu):

    config = configparser.ConfigParser()
    config.read(configPath)
    getdata = feature.transformer(config, datapath)

    print('building net...')
    net = model.Lstm_crf(config, classes)
    if usegpu:
        net = net.cuda()
    optimer = optim.Adam(net.parameters(), lr = config.getfloat('train', 'learning_rate'))
    criterion = nn.CrossEntropyLoss()

    print('begin to train net...')
    for epoch in range(config.getint('train', 'epoch')):
        print('epoch:', epoch)

        trueTag = []
        predTag = []
        loss_sum = 0
        while True:
            p = getdata.get_data()

            if p is None:
                break
            data_old, label_old, seqlen_old = p

            '''
            把数据按照 seqlen 进行排序
            '''
            sort_label = [i for i in range(config.getint('data', 'batch_size'))]
            sort_label = sorted(sort_label, key = lambda x:seqlen_old[x], reverse = True)
            traindata = np.zeros((config.getint('data', 'batch_size'), config.getint('data', 'sentenceLen'), config.getint('data', 'wordDim')))
            seqlen = []
            label = []
            for i in range(config.getint('data', 'batch_size')):
                seqlen.append(seqlen_old[sort_label[i]])
                label.append(label_old[sort_label[i]])
                traindata[i] = data_old[sort_label[i]]
            '''
            排序完毕
            '''
            if usegpu:
                traindata = Variable(torch.Tensor(traindata).cuda())
                label = Variable(torch.LongTensor(label).cuda())
            else:
                traindata = Variable(torch.Tensor(traindata))
                label = Variable(torch.LongTensor(label))

            net.init_hidden(usegpu)
            loss = net.loss(traindata, label, seqlen)
            net.zero_grad()
            loss.backward()
            optimer.step()









