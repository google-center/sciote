def get_most_active(labels, amount=5):
    actives_dict = {}

    for label in labels:
        if label in actives_dict:
            actives_dict[label] += 1
        else:
            actives_dict[label] = 1

    actives_list = sorted(actives_dict.items(),
                          key=lambda el: el[1],
                          reverse=True)[:amount]

    return [el[0] for el in actives_list]
