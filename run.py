import network.train as t

t.train('network/config/test.config', '/Users/Smart/Desktop/code/Challenge_Cup/train1.json', 9, False)
#t.train_LC('network/config/test.config', '/Users/Smart/Desktop/code/Challenge_Cup/train.json', 9, False)


'''
crf: result
             precision    recall  f1-score   support

          0       0.92      0.95      0.94      4513
          1       0.80      0.84      0.82       574
          2       0.73      0.55      0.63       206
          3       0.44      0.10      0.16        40
          4       0.77      0.65      0.70       245
          5       0.00      0.00      0.00        13
          6       0.90      0.91      0.91       724
          7       0.91      0.78      0.84       371
          8       0.92      0.90      0.91       106

avg / total       0.89      0.90      0.89      6792

'''