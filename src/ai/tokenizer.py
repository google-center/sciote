import pickle
from datetime import datetime

from tensorflow.python.keras.preprocessing.text import Tokenizer

from network.config import SC_DICT_SIZE


def train_and_return_tknzr(texts):
    tknzr = Tokenizer(SC_DICT_SIZE)
    tknzr.fit_on_texts(texts)

    with open(f'tknzrs/{datetime.now()}.pickle', 'wb') as file:
        pickle.dump(tknzr, file, protocol=4)

    return tknzr


def txts_to_seqs(texts, tknzr_id=None):
    if tknzr_id:
        with open(f'tknzrs/{tknzr_id}.pickle', 'rb') as file:
            tknzr = pickle.load(file)
    else:
        tknzr = train_and_return_tknzr(texts)

    return tknzr.texts_to_sequences(texts)


def seqs_to_txts(seqs, tknzr=None, tknzr_id=None):
    if not tknzr and not tknzr_id:
        raise ValueError('Please provide either a Tokenizer instance or a '
                         'filename of a pickled Tokenizer')
    if tknzr_id and not tknzr:
        with open(f'tknzrs/{tknzr_id}.pickle', 'rb') as file:
            tknzr = pickle.load(file)

    return tknzr.sequences_to_texts(seqs)
