from keras_preprocessing.sequence import pad_sequences
from tensorflow.python.keras.preprocessing.text import Tokenizer

from config import DICT_SIZE, LEN_LIMIT, STOP_WORDS


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

    return x_trn, x_tknzr


def tokenize_with_existing(data, tknzr):
    data = tknzr.texts_to_sequences(data)

    max_len = len(max(data, key=len))
    if max_len > LEN_LIMIT:
        max_len = LEN_LIMIT

    data = pad_sequences(data, maxlen=max_len)
    return data


def create_tknzr(data):
    words = {}
    for msg in data:
        for word in msg.split(" "):
            word = word.lower()
            word = word.strip('0123456789!?.,;:@#$%&*()')
            if word is not '':
                if word in words.keys():
                    words[word] += 1
                else:
                    words[word] = 1

    words = sorted(words.items(), key=lambda kv: -kv[1])
    words = [word for word, frequency in words]

    for w in STOP_WORDS:
        if w in words:
            words.remove(w)

    return words


def tokenize_(data, words=None, max_len=None):
    if not words:
        words = create_tknzr(data)

    new_data = []

    for msg in data:
        new_msg = []
        for word in msg.split(" "):
            word = word.lower()
            word = word.strip("0123456789!?.,;:@#$%&*()")
            if word is not '':
                if word in words:
                    new_msg.append(words.index(word))
                else:
                    new_msg.append(0)

        new_data.append(new_msg)

    if not max_len:
        max_len = len(max(new_data, key=len))
        if max_len > LEN_LIMIT:
            max_len = LEN_LIMIT

    new_data = pad_sequences(new_data, maxlen=max_len)

    return new_data, words, max_len
