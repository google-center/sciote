import pickle

import numpy as np
import requests
from flask import Flask, render_template, request, json

from config import CONFIG_DIR
from metrics import get_metrics
from tokenizer import tokenize

app = Flask(__name__)

model_id = 1554207578

with open(f'{CONFIG_DIR}{model_id}/actives.pickle', 'rb') as file:
    actives = pickle.load(file)

MSGS = np.load(f"{CONFIG_DIR}{model_id}/msgs.npy")


@app.route('/', methods=['GET'])
def new_index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    message = request.form.get('msg')

    metrics = np.array([get_metrics(message)])

    words = np.append(MSGS, message)
    words = tokenize(words)

    tokenized = [words[len(words) - 1]]
    tokenized = np.array(tokenized)

    payload = {
        "instances": [{'input': [metrics, tokenized]}]
    }

    r = requests.post('http://localhost:9000/v1/models/Classifier:predict',
                      json=payload)
    results = json.loads(r.content.decode('utf-8'))

    res_dict = {}

    for person, prob in results:
        res_dict[person] = float(prob)

    return json.jsonify(res_dict)
