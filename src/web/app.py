from datetime import datetime

from flask import Flask, render_template, request, abort, json

app = Flask(__name__)


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'GET':
        return render_template('train.html')
    else:
        amt = request.form.get('a')
        qnt = request.form.get('q')
        if amt is not None and qnt is not None:
            # TODO: обработка запроса
            pass
        else:
            abort(400)


@app.context_processor
def timestamp():
    return {'now': int(datetime.now().timestamp())}
