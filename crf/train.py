from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import json
import pycrfsuite


def word2feature(sentence, i):

    feature = {
        'word': sentence[i],
        'part-of-speech': sentence[i][1]
    }

    return feature

def sentence2feature(sentence):
    return [word2feature(sentence, i) for i in range(len(sentence))]


def sentence2label(sentence):
    return [v[2] for v in sentence]


def test(tagger, X_test, y_test):
    y_pred = [tagger.tag(xseq) for xseq in X_test]

    print(classification_report([int(y) for y in y_test], [int(y) for y in y_pred]))

def train(data, taskName):
    X_train = [sentence2feature(s) for s in data]
    y_train = [sentence2label(s) for s in data]

    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,  # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty

        'max_iterations': 100,  # stop earlier
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })

    trainer.train(taskName + '.crfsuite')

    print(taskName)
    print('result for train data:')

    tagger = pycrfsuite.Tagger()
    tagger.open(taskName + '.crfsuite')
    test(tagger, X_train, y_train)


