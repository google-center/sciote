import os
import pickle
import random
import statistics
from datetime import datetime

from keras_preprocessing.text import Tokenizer

from ai.tokenizer import tokenize

import click
import numpy as np
from tensorflow import logging
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import Dropout, Dense
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.optimizers import Adam

from ai.model import build_model
from config import FILENAME, QUOTIENT, DICT_SIZE, DICT_FILE
from data.extractor import get_most_active
from data.parser import parse_file
from metrics import get_metrics
from tensorflow.python.keras.utils import plot_model

__version__ = '0.2.0'


@click.group()
@click.version_option(__version__)
def cli():
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    logging.set_verbosity(logging.ERROR)


@cli.command()
@click.argument('chat_file', default=FILENAME)
@click.option('--amount', '-a', default=5,
              help='Amount of people to analyze')
@click.option('--quotient', '-q', default=QUOTIENT,
              help='Relation between train/test data')
def train(chat_file, amount, quotient):
    print('Parsing file...')
    msgs, lbls = parse_file(chat_file)
    print(f'Parsed {len(msgs)} messages')
    if len(msgs) != len(lbls):
        raise AssertionError('Amounts of messages and labels are not equal. '
                             'Please check your parser.')

    print('Filtering data...')
    actives = get_most_active(lbls, amount)
    data_zip = list(zip(msgs, lbls))
    random.shuffle(data_zip)

    print('Justifying data...')
    least_count = len(list(filter(lambda x: x[1] == actives[-1], data_zip)))
    just_data = []
    for act in actives:
        just_data += list(filter(lambda x: x[1] == act, data_zip))[:least_count]

    f_msgs = [m for m, l in just_data]
    f_lbls = [l for m, l in just_data]

    # перемешивание, иначе неравномерные выборки
    random.seed(42)
    random.shuffle(f_msgs)
    random.seed(42)
    random.shuffle(f_lbls)

    print('Tokenizing data...')
    metrics = [get_metrics(msg) for msg in f_msgs]
    words = tokenize(f_msgs)
    metrics = np.array(metrics)
    words = np.array(words)

    print('Tokenizing labels...')
    f_lbls = [actives.index(y) for y in f_lbls]

    print('Splitting data...')
    train_len = int(len(metrics) * quotient)
    m_trn_data, w_trn_data, trn_lbls = metrics[:train_len], words[
                                                            :train_len], f_lbls[
                                                                         :train_len]
    m_tst_data, w_tst_data, tst_lbls = metrics[train_len:], words[
                                                            train_len:], f_lbls[
                                                                         train_len:]

    trn_data = [m_trn_data, w_trn_data]
    tst_data = [m_tst_data, w_tst_data]

    print('Building model...')
    model = build_model((22, len(words[0])),
                        0.1,
                        1 if amount == 2 else amount,
                        'sigmoid' if amount == 2 else 'softmax')

    print('Creating optimizer...')
    adam = Adam(lr=0.001)

    print('Compiling model...')
    model.compile(optimizer=adam,
                  loss='sparse_categorical_crossentropy',
                  metrics=['acc'])

    # plot_model(model, to_file='model.png', show_shapes=True)

    print('Training model...')
    cbs = [EarlyStopping(monitor='val_loss', patience=10,
                         restore_best_weights=True)]
    fit = model.fit(
        trn_data,
        trn_lbls,
        epochs=100,
        callbacks=cbs,
        validation_data=(tst_data, tst_lbls),
        verbose=2,
        batch_size=64)
    print('Training complete.')
    print(f"Accuracy: {fit.history['val_acc'][-1]}")
    print(f"Loss: {fit.history['val_loss'][-1]}")
    print()

    print('Saving model...')
    layers = {
        Dropout: 'do',
        Dense: 'dn'
    }
    file_id = '-'.join(["%.3f" % fit.history['val_acc'][-1]] +
                       [str(amount), str(quotient)])

    #  +
    #                        [f'{layers[type(l)]}'
    #                         f'{l.units if isinstance(l, Dense) else l.rate}'
    #                         for l in model.layers]

    name = f'configs/{file_id}.pickle'
    with open(name, 'xb') as file:
        pickle.dump(actives, file, protocol=4)
    model.save(f'configs/{file_id}.h5')
    np.save(f"{DICT_FILE}{file_id}.npy", f_msgs)
    print(f'Model saved as {file_id}')


@cli.command()
@click.argument('model')
@click.argument('message')
def predict(model, message):
    with open(f'configs/{model}.pickle', 'rb') as file:
        actives = pickle.load(file)
    words = np.load(f"{DICT_FILE}{model}.npy")

    model = load_model(f'configs/{model}.h5')

    metrics = np.array([get_metrics(message)])

    words = np.append(words, message)
    words = tokenize(words)

    tokenized = [words[len(words) - 1]]
    tokenized = np.array(tokenized)
    result = model.predict([metrics, tokenized],
                           batch_size=1)
    print()
    print(f'Автор сообщения "{message}":')

    res_tup = []

    for i in range(len(result[0])):
        res_tup.append((actives[i], result[0][i]))

    for name, val in sorted(res_tup, key=lambda x: x[1], reverse=True):
        print(f'{name}: {val}')
        

@cli.command()
@click.argument('chat_file', default=FILENAME)
@click.option('--amount', '-a', default=5,
              help='Amount of people to analyze')
@click.option('--quotient', '-q', default=QUOTIENT,
              help='Relation between train/test data')
def kfold(chat_file, amount, quotient):
    print('Parsing file...')
    msgs, lbls = parse_file(chat_file)
    print(f'Parsed {len(msgs)} messages')
    if len(msgs) != len(lbls):
        raise AssertionError('Amounts of messages and labels are not equal. '
                             'Please check your parser.')

    print('Filtering data...')
    actives = get_most_active(lbls, amount)
    data_zip = list(zip(msgs, lbls))
    random.shuffle(data_zip)

    print('Justifying data...')
    least_count = len(list(filter(lambda x: x[1] == actives[-1], data_zip)))
    just_data = []
    for act in actives:
        just_data += list(filter(lambda x: x[1] == act, data_zip))[:least_count]

    f_msgs = [m for m, l in just_data]
    f_lbls = [l for m, l in just_data]

    # перемешивание, иначе неравномерные выборки
    random.seed(42)
    random.shuffle(f_msgs)
    random.seed(42)
    random.shuffle(f_lbls)

    print('Tokenizing data...')
    metrics = [get_metrics(msg) for msg in f_msgs]
    words = tokenize(f_msgs)
    metrics = np.array(metrics)
    words = np.array(words)

    f_lbls = [actives.index(y) for y in f_lbls]
    test_len = int(len(metrics) * (1 - quotient))

    accuracy_data = []
    test_left_bound = 0
    test_right_bound = test_len
    while test_right_bound <= int(len(metrics)):
        m_tst_data, w_tst_data, tst_lbls = metrics[
                                           test_left_bound:test_right_bound], words[
                                                                              test_left_bound:test_right_bound], f_lbls[
                                                                                                                 test_left_bound:test_right_bound]
        m_trn_data, w_trn_data, trn_lbls = np.concatenate(
            (metrics[:test_left_bound], metrics[test_right_bound:])), \
                                           np.concatenate((words[
                                                           :test_left_bound],
                                                           words[
                                                           test_right_bound:])), \
                                           np.concatenate((f_lbls[
                                                           :test_left_bound],
                                                           f_lbls[
                                                           test_right_bound:]))

        trn_data = [m_trn_data, w_trn_data]
        tst_data = [m_tst_data, w_tst_data]

        model = build_model((22, len(words[0])),
                            0.1,
                            1 if amount == 2 else amount,
                            'sigmoid' if amount == 2 else 'softmax')

        print('Creating optimizer...')
        adam = Adam(lr=0.001)

        print('Compiling model...')
        model.compile(optimizer=adam,
                      loss='sparse_categorical_crossentropy',
                      metrics=['acc'])

        # plot_model(model, to_file='model.png', show_shapes=True)

        print('Training model...')
        cbs = [EarlyStopping(monitor='val_loss', patience=10,
                             restore_best_weights=True)]
        fit = model.fit(
            trn_data,
            trn_lbls,
            epochs=50,
            callbacks=cbs,
            validation_data=(tst_data, tst_lbls),
            verbose=2,
            batch_size=64)
        print('Training complete.')
        print(f"Accuracy: {fit.history['val_acc'][-1]}")
        print(f"Loss: {fit.history['val_loss'][-1]}")
        print()

        print('Saving model...')
        layers = {
            Dropout: 'do',
            Dense: 'dn'
        }
        file_id = '-'.join(["%.3f" % fit.history['val_acc'][-1]] +
                           [str(amount), str(quotient)])

        #  +
        #                        [f'{layers[type(l)]}'
        #                         f'{l.units if isinstance(l, Dense) else l.rate}'
        #                         for l in model.layers]

        name = f'configs/{file_id}.pickle'
        with open(name, 'xb') as file:
            pickle.dump(actives, file, protocol=4)
        model.save(f'configs/{file_id}.h5')
        np.save(f"{DICT_FILE}{file_id}.npy", f_msgs)
        print(f'Model saved as {file_id}')

        accuracy_data.append(fit.history['val_acc'][-1])

        test_left_bound += test_len
        test_right_bound += test_len

    print('K-Fold Accuracy ', accuracy_data)
    numbers = [float(n) for n in accuracy_data]
    print("Dispersion: ", statistics.variance(numbers))


if __name__ == '__main__':
    cli()
