"""
This module contains module for an MLP model of the NN.

For this model the text is tokenized as n-grams and is classified using a simple
multi-layer perceptron.
"""
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, f_classif
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.python.keras.layers import Dropout, Dense
from tensorflow.python.keras.optimizers import Adam

from network.config import NGRAM_RANGE, TOKEN, MIN_FREQ, DICT_SIZE, CLIENTS, \
    MLP_DO_RATE
from network.models import _last_layer_params, sepcnn


selector = None


def tokenize_and_train(trn_data, trn_lbls, tst_data):
    vctrzr = TfidfVectorizer(
        ngram_range=NGRAM_RANGE,
        dtype='int32',
        strip_accents='unicode',
        decode_error='replace',
        analyzer=TOKEN,
        min_df=MIN_FREQ
    )

    x_trn = vctrzr.fit_transform(trn_data)

    x_tst = vctrzr.transform(tst_data)

    global selector
    selector = SelectKBest(f_classif, k=min(DICT_SIZE, x_trn.shape[1]))
    selector.fit(x_trn, trn_lbls)
    x_trn = selector.transform(x_trn).astype('float32')
    x_tst = selector.transform(x_tst).astype('float32')

    return x_trn, x_tst


def tokenize(data):
    return selector.transform(data).astype('float32')



def main(trn_data, trn_lbls, tst_data, tst_lbls):
    print('Vectorizing data...')
    # trn_data, tst_data, trn_lbls, tst_lbls = tokenize(trn_data, trn_lbls,
    #                                                   tst_data, tst_lbls)

    trn_data, tst_data = \
        tokenize_and_train(trn_data, trn_lbls, tst_data)
    print('Data vectorized')
    print()

    print('Building model...')
    model, model_name = build_model(trn_data.shape[1:])
    print('Creating optimizer...')
    adam = Adam(lr=0.001)
    print('Compiling model...')
    model.compile(optimizer=adam,
                  loss='sparse_categorical_crossentropy',
                  metrics=['acc'])
    print('Model ready to train.')
    print()

    print('Fitting model...')
    cbs = [EarlyStopping(monitor='val_loss', patience=5)]
    history = model.fit(
        trn_data,
        trn_lbls,
        epochs=100,
        callbacks=cbs,
        validation_data=(tst_data, tst_lbls),
        verbose=2,
        batch_size=64)

    history = history.history
    print('Training complete.')
    print(f"Accuracy: {history['val_acc'][-1]}")
    print(f"Loss: {history['val_loss'][-1]}")
    print()

    print('Saving model...')
    model.save(model_name + '.h5')
    print(f'Model saved as {model_name}')


LAYERS = {
    Dropout: 'dr',
    Dense: 'de'
}


def build_model(in_shape):
    units, activation = _last_layer_params(len(CLIENTS))
    model = Sequential()
    model.add(Dropout(rate=MLP_DO_RATE,
                      input_shape=in_shape))

    model.add(Dense(units=50, activation='relu'))
    model.add(Dropout(rate=MLP_DO_RATE))

    model.add(Dense(units=50, activation='relu'))
    model.add(Dropout(rate=MLP_DO_RATE))

    model.add(Dense(units=units, activation=activation))
    return model, \
           ''.join([(LAYERS[type(l)] + '_') for l in model.layers]) \
           + str(int(datetime.now().timestamp()))
