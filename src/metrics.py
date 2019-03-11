import re

# Spacing before and/or after punctuation
# if ok           ->  point += 1
# if before       ->  point += 2
# if on both side ->  point += 0
# if nowhere      ->  point += 3
def spacing_before_after_punctuation(message):
    result = 0
    punctuation_count = 0
    points = 0
    i = 0
    for i in range(0, len(message)):
        cur = message[i]
        if 0 < i < len(message) - 1 and (
                cur == "." or cur == "," or cur == "?" or cur == "!" or cur == ":" or cur == ";"):
            punctuation_count += 1
            if message[i - 1] == " " and message[i + 1] != " ":
                points += 2
            elif message[i - 1] != " " and message[i + 1] == " ":
                points += 1
            elif message[i - 1] != " " and message[i + 1] != " ":
                points += 3

        elif i > 0 and i == len(message) - 1 and (
                cur == "." or cur == "," or cur == "?" or cur == "!" or cur == ":" or cur == ";"):
            punctuation_count += 1
            if message[i - 1] != " ":
                points += 1
    if punctuation_count != 0:
        result = (points / punctuation_count) / 3
    return result


# Usage of ellipsis
# return average ellipsis length
def avg_len_ellipsis(message):
    result = 0
    length = 0
    count_sequence = 0
    i = 0
    duration = 1
    for i in range(0, len(message)):
        if i < len(message) - 1 and message[i] == "." and message[i + 1] == ".":
            if duration == 1:
                count_sequence += 1
            duration += 1
        elif duration > 1:
            length += duration
            duration = 1

    if count_sequence != 0:
        result = length / count_sequence
    return result


# Usage of em and en dashes
# result[0] = "-"
# result[1] = "–"
# result[2] = "—"
def number_different_dashes(message):
    result = [0, 0, 0]
    for i in message:
        if i == "-":
            result[0] += 1
        elif i == "–":
            result[1] += 1
        elif i == "—":
            result[2] += 1
    return result


# Usage of all caps
# return average length of substrings written by caps
def avg_len_usage_caps(message):
    caps_summary_len = 0
    all_words_length = 0
    delimiters = "?", "!", ".", ",", "\n", ":", ";"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    words = re.split(regex_pattern, message)
    for word in words:
        all_words_length += len(word)
        i = 0
        size = len(word)
        duration = 1
        for i in range(0, size):
            if i < size - 1 and 'А' <= word[i] <= 'Я' and 'А' <= word[i + 1] <= 'Я':
                duration += 1
            elif duration > 1:
                caps_summary_len += duration
                duration = 1

    result = 0
    if caps_summary_len > 0:
        result = caps_summary_len / all_words_length
    return result


# Usage of single parenthesis smileys
# result[0] -> avg length of substrings consisting only of ")"
# result[1] -> average length of substrings consisting only of "("
def avg_len_brackets_smile(message):
    result = [0, 0]
    count_happy_brackets_seq = 0
    count_sad_brackets_seq = 0
    len_happy_brackets = 0
    len_sad_brackets = 0

    i = 0
    size = len(message)
    happy_duration = 0
    sad_duration = 0
    for i in range(0, size):
        if message[i] == ")":
            if happy_duration == 0:
                count_happy_brackets_seq += 1
            len_happy_brackets += 1
            happy_duration += 1
        else:
            happy_duration = 0
        if message[i] == "(":
            if sad_duration == 0:
                count_sad_brackets_seq += 1
            len_sad_brackets += 1
            sad_duration += 1
        else:
            sad_duration = 0

    if count_happy_brackets_seq > 0:
        result[0] = len_happy_brackets / count_sad_brackets_seq
    if count_sad_brackets_seq > 0:
        result[1] = len_sad_brackets / count_sad_brackets_seq
    return result


# Если строка оканчивается точкой, возвращаем true,  иначе -  false
def hasDot(str):
    if str[len(str) - 1] == '.':
        return True
    else:
        return False


# Делим сообщения на предложения, считаем, сколько раз
# сообщение начинается с заглавной. Возвращаем отношение
def capitalLetter(str):
    delimiters = "?", "!", ".", "\n"
    regexPattern = "|".join(map(re.escape, delimiters))
    arr = re.split(regexPattern, str)
    arr = list(filter(lambda a: a != '', arr))
    for i, item in enumerate(arr):
        arr[i] = arr[i].replace(' ', '')
    count = 0
    for element in arr:
        if (element.istitle()):
            count += 1
    return count / len(arr)


# Если строка содержит ё, возвращаем true,  иначе -  false
def hasE(str):
    if str.find("ё") == -1:
        return False
    else:
        return True


# Считаем, сколько предложений содержит воскл знак, считаем общее кол-во предложений
# возвращаем отношение
def exclaMark(str):
    arr1 = str.split('!')
    arr1 = list(filter(lambda a: a != '', arr1))
    delimiters = "?", "!", ".", "\n"
    regexPattern = "|".join(map(re.escape, delimiters))
    arr2 = re.split(regexPattern, str)
    arr2 = list(filter(lambda a: a != '', arr2))
    if (str[len(str) - 1] == '!'):
        return (len(arr1)) / len(arr2)
    else:
        return (len(arr1) - 1) / len(arr2)


# возвращаем количество ; в сообщении
def countSemicolon(str):
    count = 0
    for i in str:
        if i == ';':
            count += 1
    return count


# считаем кол-во слов, которые содержат в себе подстроку из повторяющихся букв
# возвращаем отношение растянутые слова/все слова
def longLetters(str):
    arr = str.split()
    arr = list(filter(lambda a: a != '', arr))
    print(arr)
    count = 0
    for element in arr:
        i = 0
        c = 1
        while i < len(element) - 1:
            if (element[i] == element[i + 1]):
                c += 1
            else:
                c = 0
            if c == 3:
                count += 1
                continue
            i += 1
    return count / len(arr)

