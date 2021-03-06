import network.word2vec as vec
import numpy as np
import json


class transformer(object):
    def __init__(self, config, datapath):
        self.word2vec = vec.Word2vec()
        self.wordDim = config.getint('data', 'wordDim')
        self.sentLen = config.getint('data', 'sentenceLen')
        self.batch_size = config.getint('data', 'batch_size')
        self.datapath = datapath

        self.file = open(datapath, 'r')

    def load_word(self, word):
        return self.word2vec.load(word)

    def load_sent(self, sentence):
        ans = np.zeros((self.sentLen, self.wordDim), dtype = np.float32)
        label = []
        for i, word in enumerate(sentence):
            if i >= self.sentLen:
                #print('sentence is too long ...')
                break
            ans[i] = self.load_word(word[0])
            label.append(int(word[2]))
        while len(label) < self.sentLen:
            label.append(0)
        return ans, label

    def get_data(self):
        ans = np.zeros((self.batch_size, self.sentLen, self.wordDim), dtype = np.float32)
        label = []
        seqlen = []
        try:
            for i in range(self.batch_size):
                sent = self.file.readline()
                sent = json.loads(sent)
                ans[i], l = self.load_sent(sent)
                label.append(l)
                if len(sent) <= self.sentLen:
                    seqlen.append(len(sent))
                else:
                    seqlen.append(self.sentLen)
        except Exception as err:
            self.file.close()
            self.file = open(self.datapath, 'r')
            return None

        '''
        while len(label) < self.batch_size:
            label.append([0] * self.sentLen)
        '''
        return ans, label, seqlen
