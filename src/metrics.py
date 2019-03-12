import re


def split_into_sentences(message):
    delimiters = "?", "!", ".", "\n"
    regex_pattern = "|".join(map(re.escape, delimiters))
    arr = re.split(regex_pattern, message)
    return list(filter(lambda a: a != '', arr))


# Spacing before and/or after punctuation
# if ok           ->  point += 1
# if before       ->  point += 2
# if on both side ->  point += 0
# if nowhere      ->  point += 3
def spacing_around_punctuation(message):
    result = 0
    punctuation_count = 0
    points = 0
    for i in range(0, len(message)):
        cur = message[i]
        if cur in [".", ",", "?", "!", ":", ";"]:
            if 0 < i < len(message) - 1:
                punctuation_count += 1
                if message[i - 1] == " " and message[i + 1] != " ":
                    points += 2
                elif message[i - 1] != " " and message[i + 1] == " ":
                    points += 1
                elif message[i - 1] != " " and message[i + 1] != " ":
                    points += 3

            elif i > 0 and i == len(message) - 1:
                punctuation_count += 1
                if message[i - 1] != " ":
                    points += 1
    if punctuation_count != 0:
        result = (points / punctuation_count) / 3
    return result


# Usage of ellipsis
# return average ellipsis length
def avg_ellipsis_length(message):
    result = 0
    length = 0
    count_sequence = 0
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
def number_of_dashes(message):
    result = [0, 0, 0]
    for char in message:
        if char == "-":
            result[0] += 1
        elif char == "–":
            result[1] += 1
        elif char == "—":
            result[2] += 1
    return result


# Usage of all caps
# return average length of substrings written by caps
def all_caps_avg_length(message):
    caps_seqs = []
    tracking = False
    cur_seq_length = 0

    for char in message:
        if char.isalpha():
            if char.isupper():
                if not tracking:
                    tracking = True
                cur_seq_length += 1
            else:
                if tracking:
                    tracking = False
                    if cur_seq_length > 1:
                        caps_seqs.append(cur_seq_length)
                    cur_seq_length = 0

    total_length = 0
    for seq in caps_seqs:
        total_length += seq

    return total_length / len(caps_seqs) if len(caps_seqs) != 0 else 0


# Usage of single parenthesis smileys
# result[0] -> avg length of substrings consisting only of ")"
# result[1] -> average length of substrings consisting only of "("
def smiley_parenthesis_avg_lengths(message):
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
def ends_with_period(sentence):
    if sentence[len(sentence) - 1] == '.':
        return True
    else:
        return False


# Делим сообщения на предложения, считаем, сколько раз
# сообщение начинается с заглавной. Возвращаем отношение
def capitalized_amount(message):
    arr = split_into_sentences(message)
    count = 0
    for element in arr:
        if element[0].isupper():
            count += 1
    return count / len(arr)


# Если строка содержит ё, возвращаем true,  иначе -  false
def uses_yo(message):
    return "ё" in message or "Ё" in message


# Считаем, сколько предложений содержит воскл знак, считаем общее кол-во
# предложений
# возвращаем отношение
def exclamation_amount(message):
    amt = message.count('!')
    sentences = split_into_sentences(message)

    if message[-1] == '!':
        return amt / len(sentences)
    else:
        return amt / len(sentences)


# возвращаем количество ; в сообщении
def semicolon_amount(message):
    return message.count(';')


# считаем кол-во слов, которые содержат в себе подстроку из повторяющихся букв
# возвращаем отношение растянутые слова/все слова
def elongated_words(message):
    arr = message.split()
    arr = list(filter(lambda a: a != '', arr))
    print(arr)
    count = 0
    for element in arr:
        c = 1
        for i in range(len(element) - 1):
            if element[i] == element[i + 1]:
                c += 1
            else:
                c = 1
            if c == 3:
                count += 1
                break
    return count / len(arr)
