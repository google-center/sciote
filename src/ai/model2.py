from random import random

from tensorflow.python.keras import Sequential, Input, Model
from tensorflow.python.keras.layers import Dropout, Dense, Concatenate, Lambda, Embedding, SeparableConv1D, \
    MaxPooling1D, GlobalAveragePooling1D

from config import KERN_SIZE, BLOCKS, OUT_DIM, POOL_SIZE


def _last_layer_params(classes_len):
    """Calculates layer parameters based on classes set length

    :param classes_len: the amount of classes
    :return: the number of units and activation function
    """
    if classes_len == 2:
        activation = 'sigmoid'
        units = 1
    else:
        activation = 'softmax'
        units = classes_len

    return units, activation


def build_model(input_shape, dropout_rate, units, activation):
    metrics_num, words_num = input_shape

    inputs = [Input((metrics_num, )), Input((words_num, ))]

    metrics_tensor = inputs[0]
    metrics_tensor = Dense(units=50, activation='sigmoid')(metrics_tensor)
    metrics_tensor = Dense(units=units, activation='sigmoid')(metrics_tensor)

    words_tensor = inputs[1]
    words_tensor = Dense(400)(words_tensor)
    for _ in range(BLOCKS):
        words_tensor = Dense(words_num * 4)(words_tensor)
        words_tensor = Dense(words_num * 3)(words_tensor)

    words_tensor = Dense(units=units, activation='sigmoid')(words_tensor)

    output_tensor = Concatenate()([words_tensor, metrics_tensor])
    output_tensor = Dense(units=units, activation='sigmoid')(output_tensor)

    model = Model(inputs=inputs, outputs=[output_tensor])

    return model
