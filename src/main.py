import os
import pickle
from datetime import datetime

import click
import numpy as np
from tensorflow import logging
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.optimizers import Adam

from ai.model import build_model
from config import FILENAME, QUOTIENT
from data.extractor import get_most_active
from data.parser import parse_file
from metrics import get_metrics

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
    f_msgs = [m for m, l in data_zip if l in actives]
    f_lbls = [l for m, l in data_zip if l in actives]

    print('Tokenizing data...')
    data = [get_metrics(msg) for msg in f_msgs]
    data = np.array(data)

    print('Tokenizing labels...')
    f_lbls = [actives.index(y) for y in f_lbls]

    print('Splitting data...')
    train_len = int(len(data) * quotient)
    trn_data, trn_lbls = data[:train_len], f_lbls[:train_len]
    tst_data, tst_lbls = data[train_len:], f_lbls[train_len:]

    print('Building model...')
    model = build_model((15,),
                        0.1,
                        1 if amount == 2 else amount,
                        'sigmoid' if amount == 2 else 'softmax')

    print('Creating optimizer...')
    adam = Adam(lr=0.001)

    print('Compiling model...')
    model.compile(optimizer=adam,
                  loss='sparse_categorical_crossentropy',
                  metrics=['acc'])

    print('Training model...')
    cbs = [EarlyStopping(monitor='val_loss', patience=5)]
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
    file_id = int(datetime.now().timestamp())
    name = f'configs/{file_id}.pickle'
    with open(name, 'xb') as file:
        pickle.dump(actives, file, protocol=4)
    model.save(f'configs/{file_id}.h5')
    print(f'Model saved as {file_id}')


@cli.command()
@click.argument('model')
@click.argument('message')
def predict(model, message):
    with open(f'configs/{model}.pickle', 'rb') as file:
        actives = pickle.load(file)

    model = load_model(f'configs/{model}.h5')

    data = np.array([get_metrics(message)])
    result = model.predict(data,
                           batch_size=1)
    print()
    print(f'Автор сообщения "{message}":')

    res_tup = []

    for i in range(len(result[0])):
        res_tup.append((actives[i], result[0][i]))

    for name, val in sorted(res_tup, key=lambda x: x[1], reverse=True):
        print(f'{name}: {val}')


if __name__ == '__main__':
    cli()
