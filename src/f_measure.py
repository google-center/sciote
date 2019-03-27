import pickle

import numpy as np
from tensorflow.python.keras.models import load_model

from ai.tokenizer import tokenize
from config import CONFIG_FOLDER
from metrics import get_metrics


def f1(model):
    with open(f'{CONFIG_FOLDER}{model}.pickle', 'rb') as file:
        actives = pickle.load(file)
    msgs = np.load("%s%s-msgs.npy" % (CONFIG_FOLDER, model))
    lbls = np.load("%s%s-lbls.npy" % (CONFIG_FOLDER, model))

    metrics = np.array([get_metrics(msg) for msg in msgs])
    tokenized = np.array(tokenize(msgs))

    model = load_model(f'{CONFIG_FOLDER}{model}.h5')

    people = lbls.max() + 1
    lens = np.zeros((people,))
    for i in lbls:
        lens[i] += 1

    # 4 arrays for recall and precision calculations
    relevant = lens  # сообщения принадлежащие конкретному человеку
    irrelevant = [_len * (people - 1) for _len in lens]  # сообщения не принадлежащие конкретному человеку
    true_positives = np.zeros((people,))  # сообщения конкретного человека выбранные нейронкой
    false_positives = np.zeros((people,))  # сообщения не принадлежащие конкретному человеку выбранные нейронкой

    if metrics.shape[0] == lbls.shape[0]:
        for i in range(metrics.shape[0]):
            res = np.array(model.predict([np.array([metrics[i]]), np.array([tokenized[i]])], batch_size=1))
            if res.argmax() == lbls[i]:
                true_positives[res.argmax()] += 1
            else:
                false_positives[res.argmax()] += 1
    else:
        raise Exception("Labels and messages arrays have different sizes")

    precision = np.zeros((people,))
    recall = np.zeros((people,))
    f1 = np.zeros((people,))
    for i in range(people):
        # Сколько выбранных сообщений правильны?
        precision[i] = true_positives[i] / relevant[i]

        # Сколько правильных сообщений выбрано?
        recall[i] = true_positives[i] / (true_positives[i] + false_positives[i])

        # F-measure для каждого отдельного человека
        f1[i] = (2 * precision[i] * recall[i]) / (precision[i] + recall[i])

    return f1


if __name__ == '__main__':
    f1("0.318-5-0.5")
