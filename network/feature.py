import nn.word2vec as vec
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
                print('sentence is too long ...')
                break
            ans[i] = self.load_word(word[0])
            label.append(word[2])
        return ans, label

    def get_data(self):
        ans = np.zeros((self.batch_size, self.sentLen, self.wordDim), dtype = np.float32)
        label = []
        try:
            for i in range(self.batch_size):
                sent = self.file.readline()
                sent = json.loads(sent)
                ans[i], l = self.load_sent(sent)
                label.append(l)
        except Exception as err:
            return None
        return ans, label
