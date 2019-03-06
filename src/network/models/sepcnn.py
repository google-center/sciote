"""
This module contains module for a sepCNN model of the NN.

For this model the text is tokenized as sequences and is classified using a
separable convolutional neural network.
"""
from datetime import datetime

from tensorflow.python.keras import models
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import Embedding, Dense, Dropout, \
    SeparableConv1D, MaxPooling1D, GlobalAveragePooling1D
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer

from network.config import CLIENTS, EPOCHS, BAT_SIZE, SC_DICT_SIZE, \
    LEN_LIMIT, OUT_DIM, BLOCKS, SC_DO_RATE, KERN_SIZE, POOL_SIZE
from network.models import _last_layer_params


def main(trn_data, trn_lbls, tst_data, tst_lbls):
    print('Tokenizing data...')
    trn_data, tst_data, index, trn_lbls, tst_lbls = \
        tokenize(trn_data, tst_data, trn_lbls, tst_lbls)
    print('Data tokenized')
    print()

    print('Building model...')
    model = build_model(len(index), trn_data.shape[1:])
    print('Model built')
    print()

    print('Training model...')
    if len(CLIENTS) == 2:
        loss = 'binary_crossentropy'
    else:
        loss = 'sparse_categorical_crossentropy'

    adam_opt = Adam(lr=0.001)
    model.compile(optimizer=adam_opt, loss=loss, metrics=['acc'])

    cbs = [EarlyStopping(monitor='val_loss', patience=5)]

    fit = model.fit(
        trn_data,
        trn_lbls,
        epochs=EPOCHS,
        callbacks=cbs,
        validation_data=(tst_data, tst_lbls),
        verbose=2,
        batch_size=BAT_SIZE
    )

    result = fit.history
    print('Model trained')
    print(f"Accuracy: {result['val_acc'][-1]}")
    print(f"Loss: {result['val_loss'][-1]}")
    print()

    print('Saving model...')
    model_name = str(int(datetime.now().timestamp())) + '.h5'
    model.save(model_name)
    print(f'Model saved as {model_name}')


def tokenize(trn_data, tst_data, trn_lbls, tst_lbls):
    x_tknzr = Tokenizer(SC_DICT_SIZE)
    x_tknzr.fit_on_texts(trn_data)

    x_trn = x_tknzr.texts_to_sequences(trn_data)
    x_tst = x_tknzr.texts_to_sequences(tst_data)

    # если максимальная длина больше лимита — обубаем до лимита
    # если меньше — оставляем как есть
    max_len = len(max(x_trn, key=len))
    if max_len > LEN_LIMIT:
        max_len = LEN_LIMIT

    x_trn = pad_sequences(x_trn, maxlen=max_len)
    x_tst = pad_sequences(x_tst, maxlen=max_len)

    y_trn = [CLIENTS.index(y) for y in trn_lbls]
    y_tst = [CLIENTS.index(y) for y in tst_lbls]

    return x_trn, x_tst, x_tknzr.word_index, y_trn, y_tst


def build_model(num_words, in_shape):
    units, activation = _last_layer_params(len(CLIENTS))
    model = models.Sequential()

    model.add(Embedding(input_dim=num_words+1,
                        output_dim=OUT_DIM,
                        input_shape=in_shape))

    for _ in range(BLOCKS - 1):
        model.add(Dropout(rate=SC_DO_RATE))
        model.add(SeparableConv1D(filters=OUT_DIM,
                                  kernel_size=KERN_SIZE,
                                  activation='relu',
                                  bias_initializer='random_uniform',
                                  depthwise_initializer='random_uniform',
                                  padding='same'))
        model.add(SeparableConv1D(filters=OUT_DIM,
                                  kernel_size=KERN_SIZE,
                                  activation='relu',
                                  bias_initializer='random_uniform',
                                  depthwise_initializer='random_uniform',
                                  padding='same'))
        model.add(MaxPooling1D(pool_size=POOL_SIZE))

    model.add(SeparableConv1D(filters=OUT_DIM * 2,
                              kernel_size=KERN_SIZE,
                              activation='relu',
                              bias_initializer='random_uniform',
                              depthwise_initializer='random_uniform',
                              padding='same'))

    model.add(SeparableConv1D(filters=OUT_DIM * 2,
                              kernel_size=KERN_SIZE,
                              activation='relu',
                              bias_initializer='random_uniform',
                              depthwise_initializer='random_uniform',
                              padding='same'))

    model.add(GlobalAveragePooling1D())
    model.add(Dropout(rate=SC_DO_RATE))
    model.add(Dense(units=units,
                    activation=activation))
    return model
