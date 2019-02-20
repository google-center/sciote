def newlines_to_literals(string: str):
    return string.replace('\n', r'\n')


def literals_to_newlines(string: str):
    return string.replace(r'\n', '\n')

