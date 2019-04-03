from keras_preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer

from config import DICT_SIZE, LEN_LIMIT, STOP_WORDS
from data.parser import parse_file


def train_and_return_tknzr(texts):
    tknzr = Tokenizer(DICT_SIZE)
    tknzr.fit_on_texts(texts)

    return tknzr


def tokenize(trn_data):
    x_tknzr = Tokenizer(DICT_SIZE)
    x_tknzr.fit_on_texts(trn_data)

    x_trn = x_tknzr.texts_to_sequences(trn_data)

    max_len = len(max(x_trn, key=len))
    if max_len > LEN_LIMIT:
        max_len = LEN_LIMIT

    x_trn = pad_sequences(x_trn, maxlen=max_len)

    return x_trn


def tokenize_(data):
    _dict = {}
    for msg in data:
        for word in msg.split(" "):
            _dict[word] += 1

    sorted_dict = sorted(_dict.items(), key=lambda kv: kv[1])
    words, frequency = zip(*sorted_dict)

    for w in STOP_WORDS:
        words.remove(w)

    for msg in data:
        new_msg = []
        for word in msg.split(" "):
            if word in words:
                new_msg.append(words.index(word))
            else:
                new_msg.append(0)

        msg = new_msg

    return data
