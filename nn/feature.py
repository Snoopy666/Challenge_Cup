import nn.word2vec as vec
import numpy as np


class transformer(object):
    def __init__(self):
        self.word2vec = vec.Word2vec()


    def loadSent(self, sentence, config):
        ans = np.zeros((config.getint('data', ''), config.getint('data', '')), dtype = np.float32)

        pass