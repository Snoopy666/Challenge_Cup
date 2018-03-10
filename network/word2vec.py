
'''
class Word2vec(object):
    def __init__(self):
        pass

    def getWordVec(self, word):

        pass
'''

# coding:utf-8
import numpy as np
import json
import pickle
import gensim


class Word2vec:

    word_num = 0
    vec_len = 0
    word2id = None
    vec = None

    def __init__(self, word_dic="/home/guozhipeng/law/word2id.pkl", vec_path="/home/guozhipeng/law/vec_nor.npy"):
        print("begin to load word embedding")
        '''
        f = open(word_dic, "rb")
        (self.word_num, self.vec_len) = pickle.load(f)
        self.word2id = pickle.load(f)
        f.close()
        self.vec = np.load(vec_path)
        print("load word embedding succeed")
        '''
        #self.vec = wv.load('/Users/Smart/Desktop/code/law_eventExtraction/EventExtraction_law/data/vectors.bin')
        self.vec = gensim.models.KeyedVectors.load_word2vec_format('/Users/Smart/Desktop/code/law_eventExtraction/EventExtraction_law/data/vectors.bin', binary=True)


    def load(self, word):
        try:
            return self.vec[word]
        except Exception as err:
            return np.zeros((200,))
        '''
        try:
            return self.vec[self.word2id[word]].astype(dtype=np.float32)
        except:
            return self.vec[self.word2id['UNK']].astype(dtype=np.float32)
        '''