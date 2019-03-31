import sqlite3 as sq

import numpy as np
from tensorflow.python.keras.callbacks import Callback

conn = sq.connect("sciote.sqlite3")
cur = conn.cursor()


def init():
    cur.execute("""CREATE TABLE trainings (
                id INTEGER PRIMARY KEY,
                amount INTEGER NOT NULL ,
                quotient REAL NOT NULL ,
                accuracy REAL DEFAULT 0,
                loss REAL DEFAULT 0,
                epoch INTEGER DEFAULT 0,
                finished INTEGER DEFAULT 0,
                avg_f REAL);""")
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
                "id, amount, quotient)"
                " VALUES(?,?,?)",
                [t_id, amt, qnt])
    conn.commit()


def update_training(t_id, epoch, acc, loss):
    cur.execute(
        "UPDATE trainings SET epoch=?, accuracy=?, loss=? WHERE id=?",
        [epoch, acc, loss, t_id])
    conn.commit()


def training_status(t_id):
    cur.execute("SELECT * FROM trainings WHERE id=?", [t_id])
    tr = cur.fetchone()
    conn.commit()

    if tr is None:
        return None

    acc = tr[3]
    loss = tr[4]
    epoch = tr[5]
    completed = bool(tr[6])
    return completed, acc, loss, epoch


def save_training_result(t_id, acc, loss):
    cur.execute("UPDATE trainings SET accuracy=?, loss=?, finished=1 WHERE id=?",
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
    cur.execute("SELECT id, amount, quotient, accuracy, finished FROM trainings")
    tr = cur.fetchall()
    conn.commit()
    return list([(row[0], row[1], row[2], row[3], bool(row[4]))for row in tr])


def save_fmeasure(tid, f_value):
    cur.execute("UPDATE trainings SET avg_f=? WHERE id=?",
                [f_value, tid])
    conn.commit()


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
