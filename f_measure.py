import numpy as np
from tensorflow.python.keras.models import load_model

from ai.tokenizer import tokenize
from config import CONFIG_DIR
from metrics import get_metrics


def f1(model):
    msgs = np.load(f"{CONFIG_DIR}{model}/msgs.npy")
    lbls = np.load(f"{CONFIG_DIR}{model}/lbls.npy")

    metrics = np.array([get_metrics(msg) for msg in msgs])
    tokenized = np.array(tokenize(msgs))

    model = load_model(f'{CONFIG_DIR}{model}/model.h5')

    people = lbls.max() + 1
    lens = np.zeros((people,))
    for i in lbls:
        lens[i] += 1

    # 4 arrays for recall and precision calculations
    relevant = lens  # сообщения принадлежащие конкретному человеку
    true_positives = np.zeros((people,))  # сообщения конкретного человека выбранные нейронкой
    false_positives = np.zeros((people,))  # сообщения не принадлежащие конкретному человеку выбранные нейронкой

    if metrics.shape[0] == lbls.shape[0]:
        for i in range(metrics.shape[0]):
            res = np.array(
                model.predict([np.array([metrics[i]]),
                               np.array([tokenized[i]])],
                              batch_size=1))
            if res.argmax() == lbls[i]:
                true_positives[res.argmax()] += 1
            else:
                false_positives[res.argmax()] += 1
    else:
        raise Exception("Labels and messages arrays have different sizes")

    precision = np.zeros((people,))
    recall = np.zeros((people,))
    f = np.zeros((people,))
    for i in range(people):
        # Сколько выбранных сообщений правильны?
        precision[i] = true_positives[i] / relevant[i]

        # Сколько правильных сообщений выбрано?
        recall[i] = true_positives[i] / (true_positives[i] + false_positives[i])

        # F-measure для каждого отдельного человека
        f[i] = (2 * precision[i] * recall[i]) / (precision[i] + recall[i])

    return f
