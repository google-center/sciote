import sqlite3 as sq

import numpy as np

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
    cur.execute("INSERT INTO trainings(id, amount, quotient) VALUES(?,?,?)",
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


def get_all_messages():
    cur.execute("SELECT * FROM messages")
    return cur.fetchall()


if __name__ == '__main__':
    init()
