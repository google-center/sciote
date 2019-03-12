import sys

from network.config import CLIENTS
from network.models import mlp, sepcnn


def tokenize_labels(trn_lbls, tst_lbls):
    y_trn = [CLIENTS.index(y) for y in trn_lbls]
    y_tst = [CLIENTS.index(y) for y in tst_lbls]

    return y_trn, y_tst


def _train(messages, labels, quotient):
    if len(messages) != len(labels):
        print('Messages and labels have different lengths')
        sys.exit(1)

    print('Splitting data...')
    train_len = int(len(messages) * quotient)
    train_data, train_labels = messages[:train_len], labels[:train_len]
    test_data, test_labels = messages[train_len:], labels[train_len:]
    print('Data split')
    print(f"Train dataset size: {len(train_data)}")
    print(f"Test dataset size: {len(test_data)}")
    print()

    avg = 0.0
    for msg in messages:
        avg += len(msg.split())
    avg /= len(messages)
    avg = len(messages) / avg

    train_labels, test_labels = tokenize_labels(train_labels, test_labels)

    if avg < 1500:
        print(f"Using the MLP model (S/W = {avg})")
        mlp.main(train_data, train_labels, test_data, test_labels)
    else:
        print(f"Using the sepCNN model (S/W = {avg})")
        sepcnn.main(train_data, train_labels, test_data, test_labels)
