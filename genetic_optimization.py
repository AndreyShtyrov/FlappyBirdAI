import os
os.environ['TD_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf


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
            self.w = tf.random.truncated_normal((x.shape[-1], self.outputs), stddev=5, name="w")
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
        self.layer1 = DenseNN(3)
        self.layer2 = DenseNN(1)
        self.score = 0

    def inherit_gen(self, gen: list):
        self.layer2.init_variables(gen[0][0], gen[0][1])
        self.layer1.init_variables(gen[1][0], gen[1][1])

    def predict(self, x):
        return self.layer2(self.layer1(x))

    def get_gen(self):
        return [(self.layer2.w, self.layer2.b), (self.layer1.w, self.layer1.b)]


class GeneticArea():

    def __init__(self, n_specials: int):
        self.individals = []
        self.n_specials = n_specials
        self.generation = 0
        for i in range(n_specials):
            self.individals.append(Individals())

    def get_best(self, amount: int) -> list:
        survavals = sorted(self.individals, key=lambda item: item.score)
        return survavals[-amount:]

    def gen_move(self, survavels: list) ->list:
        genes = []
        amount = len(survavels)
        for survavel in survavels:
            genes.append(survavel.get_gen())
        best_gen = genes[-1]
        first_part = int(self.n_specials / 3)
        second_part = int(self.n_specials / 3) * 2
        for i in range(amount, self.n_specials):
            w1 = best_gen[0][0]
            b1 = best_gen[0][1]
            w2 = best_gen[1][0]
            b2 = best_gen[1][1]
            if i < first_part:
                w1 = w1 + tf.random.truncated_normal(w1.shape, stddev=0.1)
                b1 = b1 + tf.random.truncated_normal(b1.shape, stddev=0.1)
                w2 = w2 + tf.random.truncated_normal(w2.shape, stddev=0.1)
                b2 = b2 + tf.random.truncated_normal(b1.shape, stddev=0.1)
            elif first_part < i < second_part:
                w1 = w1 + tf.random.truncated_normal(w1.shape, stddev=0.4)
                b1 = b1 + tf.random.truncated_normal(b1.shape, stddev=0.4)
                w2 = w2 + tf.random.truncated_normal(w2.shape, stddev=0.4)
                b2 = b2 + tf.random.truncated_normal(b1.shape, stddev=0.4)
            elif second_part < i:
                w1 = w1 + tf.random.truncated_normal(w1.shape, stddev=2.4)
                b1 = b1 + tf.random.truncated_normal(b1.shape, stddev=2.4)
                w2 = w2 + tf.random.truncated_normal(w2.shape, stddev=2.4)
                b2 = b2 + tf.random.truncated_normal(b1.shape, stddev=2.4)
            genes.append([(w1, b1), (w2, b2)])
        return genes

    def make_select(self):
        bests = self.get_best(4)
        genes = self.gen_move(bests)
        self.individals = []
        for gen in genes:
            individal = Individals()
            individal.inherit_gen(gen)
            self.individals.append(individal)


    def make_decision(self, i, x):
        return self.individals[i].predict(x)


