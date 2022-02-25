import os
os.environ['TD_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from keras.datasets import mnist



class DenseNN(tf.Module):
    def __init__(self, outputs, activate='relu'):
        super().__init__()
        self.outputs = outputs
        self.activate = activate
        self.fl_init = False


    def init_variables(self, w, b):
        self.w = tf.Variable(w)
        self.b = tf.Variable(b)
        self.fl_init = True

    def __call__(self, x):
        if not self.fl_init:
            self.w = tf.random.truncated_normal((x.shape[-1], self.outputs), stddev=0.1, name="w")
            self.b = tf.zeros([self.outputs], dtype=tf.float32, name='b')

            self.w = tf.Variable(self.w)
            self.b = tf.Variable(self.b)

            self.fl_init = True

        y = x @ self.w + self.b
        if self.activate == "relu":
            return tf.nn.relu(y)
        if self.activate == "softmax":
            return tf.nn.softmax(y)
        return y


class Individals():
    def __init__(self):
        self.layer1 = DenseNN(4)
        self.layer2 = DenseNN(2)
        self.score = 0

    def predict(self, x):
        return self.layer2(self.layer1(x))

    def get_gen(self):
        return self.layer2.w, self.layer2.b, self.layer1.w, self.layer1.b


class GeneticArea():

    def __init__(self, n_specials: int):
        self.individals = []
        self.generation = 0
        for i in range(n_specials):
            self.individals.append(Individals)

    def get_best(self, amount: int):
        survavals = [self.individals[:amount]]

        def compare(item1, item2):
            if item1.score > item2.score:
                return 1
            elif item2.score > item1.score:
                return -1
            else:
                return 0

        survavals.sort(key=compare)
        min_score = survavals[0].score
        for individal in self.individals[amount:]:
            if individal.score < min_score:
                continue
            survavals.append(individal)
            survavals.sort(key=compare)
            survavals.__delitem__(0)
        return survavals

    def gen_move(self, survavels: list):
        genes = []
        amount = len(survavels)
        for survavel in survavels:
            genes.append(survavel.get_gen())

        for _ in range(amount * 2):
            pass




