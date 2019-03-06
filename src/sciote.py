import os

import tensorflow as tf

from fancy_stuff import banner, banner_width
from network.config import FILENAME, CLIENTS, QUOTIENT
from network.trainer import train
from parser import parse_file

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)

print(banner)
print('version 0.1'.center(banner_width))

print('Parsing the file...')
messages, labels = parse_file(FILENAME)
print(f'Parsing complete: {len(messages)} messages and {len(labels)} labels')
print()

print(f'Filtering data to only include {len(CLIENTS)} authors...')
f_lbls, f_msgs = [[l for l, m in zip(labels, messages) if l in CLIENTS],
                  [m for l, m in zip(labels, messages) if l in CLIENTS]]
print('Data filtered')
print()

# print('Training the neural network...')
train(f_msgs, f_lbls, QUOTIENT)
# print(f'Training complete with accuracy of {accuracy}')
