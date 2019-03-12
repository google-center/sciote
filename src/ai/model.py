from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dropout, Dense


def _last_layer_params(classes_len):
    """Calculates layer parameters based on classes set length

    :param classes_len: the amount of classes
    :return: the number of units and activation function
    """
    if classes_len == 2:
        activation = 'sigmoid'
        units = 1
    else:
        activation = 'softmax'
        units = classes_len

    return units, activation


def build_model(input_shape, dropout_rate, units, activation):
    model = Sequential()

    model.add(Dropout(rate=dropout_rate,
                      input_shape=input_shape))

    model.add(Dense(units=50,
                    activation='relu'))
    model.add(Dropout(rate=dropout_rate))
    model.add(Dense(units=units,
                    activation=activation))

    return model
