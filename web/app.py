import pickle

import numpy as np
import requests
from flask import Flask, render_template, request, json
from tensorflow.python.keras.models import load_model

from config import CONFIG_DIR
from metrics import get_metrics
from ai.tokenizer import tokenize, tokenize_

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

    model = load_model(f'{CONFIG_DIR}{model_id}/model.h5')

    result = model.predict([metrics, tokenized],
                           batch_size=1)

    res_tup = []

    for i in range(len(result[0])):
        res_tup.append((actives[i], result[0][i]))

    res_dict = {}
    for person, prob in res_tup:
        res_dict[person] = float(prob)

    return json.jsonify(res_dict)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
