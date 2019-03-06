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
