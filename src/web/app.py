from datetime import datetime
from multiprocessing import Process
from threading import Thread

from flask import Flask, render_template, request, abort, json, redirect, \
    url_for

from db import training_status, get_all_trainings, remove_training
from main import actual_train, actual_predict

app = Flask(__name__)

threads = {}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', models=get_all_trainings())


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'GET':
        return render_template('train.html')
    else:
        amt = request.form.get('a')
        qnt = request.form.get('q')
        if amt is not None and qnt is not None:
            tid = int(datetime.now().timestamp())
            thread = Process(target=actual_train, args=(int(amt),
                                                        float(qnt),
                                                        tid))
            thread.start()
            threads[tid] = thread

            # actual_train(int(amt), float(qnt), tid)
            return redirect(url_for('train_status_page', tid=tid))
        else:
            abort(400)


@app.route('/train/<int:tid>', methods=['GET'])
def train_status_page(tid):
    tr = training_status(tid)
    if tr is None:
        abort(404)
    completed, acc, loss, epoch = tr
    return render_template('status.html',
                           training_id=tid,
                           completed=completed,
                           accuracy=acc,
                           loss=loss,
                           epoch=epoch)


@app.route('/train/<int:tid>/status', methods=['GET'])
def training_status_json(tid):
    if request.method == 'GET':
        tr = training_status(tid)
        if tr is None:
            abort(404)
        completed, acc, loss, epoch = tr
        return json.jsonify(
            **{'completed': completed, 'accuracy': acc, 'loss': loss,
               'epoch': epoch})


@app.route('/train/<int:tid>/stop', methods=['POST'])
def stop_training(tid):
    if tid in threads:
        threads[tid].terminate()
        del threads[tid]
        remove_training(tid)
        return redirect(url_for('index'))
    else:
        return json.jsonify(**{'status': 'No training exists'}), 410


@app.route('/predict/<int:tid>', methods=['GET', 'POST'])
def predict(tid):
    if request.method == 'GET':
        return render_template('predict.html', training_id=tid)
    else:
        message = request.form.get('msg')
        results = actual_predict(tid, message)
        res_dict = {}

        for person, prob in results:
            res_dict[person] = float(prob)

        return json.jsonify(res_dict)


@app.context_processor
def timestamp():
    return {'now': int(datetime.now().timestamp())}
