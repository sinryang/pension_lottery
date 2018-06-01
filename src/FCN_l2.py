#-*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

import tensorflow as tf

from datasets.pension_lottery import datasets

N_INPUT_DATA = 100
N_TARGET_NUM = 35

NUM_INPUTS = N_INPUT_DATA * (N_TARGET_NUM + 8)

N_HL1_UNITS = NUM_INPUTS
N_HL2_UNITS = N_TARGET_NUM

epoch = 900

def main(_):
    data = datasets.load_pension_lottery_fcn_datasets(n_data=N_INPUT_DATA, shuffle=True, ratio=[0.7, None, 0.3])

    train = data.train
    test = data.test

    # Neural Network
    # Input
    X = tf.placeholder(tf.float32, [None, NUM_INPUTS])

    # Layer_1
    w_1 = tf.Variable(tf.truncated_normal([NUM_INPUTS, N_HL1_UNITS], stddev=1.0 / math.sqrt(float(NUM_INPUTS))), name='weights_1')
    b_1 = tf.Variable(tf.ones([N_HL1_UNITS]), name='biases_1')
    l_1 = tf.nn.relu(tf.matmul(X, w_1) + b_1)

    # Layer_2
    w_2 = tf.Variable(tf.truncated_normal([N_HL1_UNITS, N_HL2_UNITS], stddev=1.0 / math.sqrt(float(N_HL1_UNITS))), name='weights_2')
    b_2 = tf.Variable(tf.ones([N_HL2_UNITS]), name='biases_2')
    l_2 = tf.nn.relu(tf.matmul(l_1, w_2) + b_2)

    # Output
    Y = l_2

    # Define loss and optimizer
    Y_ = tf.placeholder(tf.float32, [None, N_TARGET_NUM])

    mse = tf.losses.mean_squared_error(labels=Y_, predictions=Y)
    cost = mse
    train_step = tf.train.AdamOptimizer().minimize(cost)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    tf_epoch = tf.constant('epoch: ' + str(epoch))

    print(sess.run(tf_epoch))
    print('=======================================')

    # Train
    for _ in range(epoch):
        sess.run(train_step, feed_dict={X: train.data, Y_: train.target})

        if _ % 200 == 0:
            tmp_cost = sess.run(cost, feed_dict={X: train.data, Y_: train.target})
            print('')
            print('Iteration: ', _)
            print('Current cost on train dataset: ', tmp_cost)
            print('=======================================')


    # Test
    correct_prediction = tf.equal(tf.argmax(Y, 1), tf.argmax(Y_, 1))
    l = tf.scalar_mul(10, Y_)
    p = tf.round(tf.scalar_mul(10, Y))
    e = tf.reduce_mean(tf.cast(tf.equal(l, p), tf.float32))

    print("MSE: ", sess.run(cost, feed_dict={X: test.data, Y_: test.target}))
    print("Match Rate: ", sess.run(e, feed_dict={X: test.data, Y_: test.target}))

if __name__ == '__main__':
    tf.app.run(main=main)
