from tensorflow.python.keras.preprocessing.text import Tokenizer

from config import DICT_SIZE


def train_and_return_tknzr(texts):
    tknzr = Tokenizer(DICT_SIZE)
    tknzr.fit_on_texts(texts)

    return tknzr
