import sqlite3 as sq

import numpy as np
from tensorflow.python.keras.callbacks import Callback

conn = sq.connect("sciote.sqlite3")
cur = conn.cursor()


def init():
    cur.execute("""CREATE TABLE trainings (
                id INTEGER PRIMARY KEY,
                amount INTEGER,
                quotient REAL,
                accuracy REAL,
                loss REAL,
                cur_epoch INTEGER,
                cur_acc REAL,
                cur_loss REAL);""")
    cur.execute("""CREATE TABLE messages (
                author TEXT,
                text TEXT,
                attachments TEXT);""")
    conn.commit()


def save_message(author, text, attachments):
    cur.execute("INSERT INTO messages(author, text, attachments) VALUES(?,?,?)",
                [author, text, attachments])
    conn.commit()


def save_training(t_id, amt, qnt):
    cur.execute("INSERT INTO trainings("
                "id, amount, quotient, cur_epoch, cur_acc, cur_loss)"
                " VALUES(?,?,?,0,0.0,0.0)",
                [t_id, amt, qnt])
    conn.commit()


def update_training(t_id, epoch, acc, loss):
    cur.execute(
        "UPDATE trainings SET cur_epoch=?, cur_acc=?, cur_loss=? WHERE id=?",
        [epoch, acc, loss, t_id])
    conn.commit()


def training_status(t_id):
    cur.execute("SELECT * FROM trainings WHERE id=?", [t_id])
    tr = cur.fetchone()
    conn.commit()

    if tr is None:
        return None

    if tr[3] is not None and tr[4] is not None:
        completed = True
        acc = tr[3]
        loss = tr[4]
    else:
        completed = False
        acc = tr[6]
        loss = tr[7]
    epoch = tr[5]
    return completed, acc, loss, epoch


def save_training_result(t_id, acc, loss):
    cur.execute("UPDATE trainings SET accuracy=?, loss=? WHERE id=?",
                [acc, loss, t_id])
    conn.commit()


def remove_training(t_id):
    cur.execute("DELETE FROM trainings WHERE id=?",
                [t_id])
    conn.commit()


def get_all_messages():
    cur.execute("SELECT * FROM messages")
    tr = cur.fetchall()
    conn.commit()
    return tr


def get_all_trainings():
    cur.execute("SELECT id, amount, quotient, accuracy, cur_acc FROM trainings")
    tr = cur.fetchall()
    conn.commit()
    return tr


class UpdateProgressCallback(Callback):
    def __init__(self, tid):
        super(UpdateProgressCallback, self).__init__()
        self.tid = tid

    def on_epoch_begin(self, epoch, logs=None):
        return

    def on_epoch_end(self, epoch, logs=None):
        update_training(self.tid,
                        epoch + 1,
                        float(logs.get("acc")),
                        float(logs.get("loss")))


if __name__ == '__main__':
    init()
