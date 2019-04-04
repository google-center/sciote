import pickle

import numpy as np
import requests
from flask import Flask, render_template, request, json

from config import CONFIG_DIR
from metrics import get_metrics
from tokenizer import tokenize, tokenize_

app = Flask(__name__)

model_id = 1554370971

with open(f'{CONFIG_DIR}{model_id}/actives.pickle', 'rb') as file:
    actives = pickle.load(file)

with open(f'{CONFIG_DIR}{model_id}/tokenizer.pickle', 'rb') as file:
    tokenizer = pickle.load(file)

with open(f'{CONFIG_DIR}{model_id}/max_len.pickle', 'rb') as file:
    max_len = pickle.load(file)


@app.route('/', methods=['GET'])
def new_index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    message = request.form.get('msg')

    metrics = np.array([get_metrics(message)])

    tokenized, _, _ = tokenize_([message], tokenizer, max_len)

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
