from tensorflow.python.keras.backend import get_session
from tensorflow.python.keras.models import load_model
from tensorflow.python.saved_model.simple_save import simple_save

model = load_model('../configs/1554370971/model.h5')
export_path = './models/2'

with get_session() as sess:
    simple_save(
        sess,
        export_path,
        inputs={t.name: t for t in model.inputs},
        outputs={t.name: t for t in model.outputs}
    )

if __name__ == '__main__':
    pass
