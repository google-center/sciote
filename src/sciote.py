#! usr/bin/env python3

import os
import pickle

import click
import tensorflow as tf
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing.sequence import pad_sequences

from fancy_stuff import banner
from network.config import FILENAME, CLIENTS, QUOTIENT
from network.trainer import _train
from parser import parse_file


@click.group()
@click.version_option('0.1.0')
def cli():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.logging.set_verbosity(tf.logging.ERROR)

    print(banner)
    print('version 0.1.0')


@cli.command()
@click.argument('file', default=FILENAME)
def train(file):
    print('Parsing the file...')
    messages, labels = parse_file(file)
    print(
        f'Parsing complete: {len(messages)} messages and {len(labels)} labels')
    print()

    print(f'Filtering data to only include {len(CLIENTS)} authors...')
    f_lbls, f_msgs = [[l for l, m in zip(labels, messages) if l in CLIENTS],
                      [m for l, m in zip(labels, messages) if l in CLIENTS]]
    print('Data filtered')
    print()
    _train(f_msgs, f_lbls, QUOTIENT)


@cli.command()
@click.argument('model')
@click.argument('message')
@click.option('--mode', '-m', default='sepcnn',
              type=click.Choice(['mlp', 'sepcnn']))
def predict(model, message, mode):
    m = load_model(model + '.h5')
    with open(model+'.pickle', 'rb') as handle:
        tknzr = pickle.load(handle)

    if mode == 'mlp':
        print('This mode is not supported yet')
    elif mode == 'sepcnn':
        data = tknzr.texts_to_sequences([message])
        data = pad_sequences(data, maxlen=m.layers[0].input_shape[1])
        result = m.predict(data,
                           batch_size=1)

        print()
        print(f'Автор сообщения "{message}":')

        res_tup = []

        for i in range(len(result[0])):
            res_tup.append((CLIENTS[i], result[0][i]))

        for name, val in sorted(res_tup, key=lambda x: x[1], reverse=True):
            print(f'{name}: {val}')


if __name__ == '__main__':
    cli()
