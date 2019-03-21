import re

import numpy as np


def split_into_words(message):
    """Разделяет сообщение на слова

    :param message: сообщение
    :return: массив слов
    """
    delimiters = "?", "!", ".", "\n", ""
    regex_pattern = "|".join(map(re.escape, delimiters))
    arr = re.split(regex_pattern, message)
    return list(filter(lambda a: a.strip() != '', arr))


def split_into_sentences(message):
    """Разделяет сообщение на предложения

    :param message: исходное сообщение
    :return: массив строк, каждая из которых представляет отдельное предложение
    """
    delimiters = "?", "!", ".", "\n"
    regex_pattern = "|".join(map(re.escape, delimiters))
    arr = re.split(regex_pattern, message)
    return list(filter(lambda a: a.strip() != '', arr))


def spacing_around_punctuation(message):
    """Метрика пробелов вокруг знаков препинания

    :param message: сообщение
    :return: массив из четырех элементов
    """
    result = 0
    punctuation_count = 0
    points = 0

    stats = [0, 0, 0, 0]

    for i in range(0, len(message)):
        cur = message[i]
        if cur in [".", ",", "?", "!", ":", ";"]:
            if 0 < i < len(message) - 1:
                punctuation_count += 1
                if message[i - 1] == " " and message[i + 1] != " ":
                    points += 2
                    stats[2] += 1
                elif message[i - 1] != " " and message[i + 1] == " ":
                    points += 1
                    stats[1] += 1
                elif message[i - 1] != " " and message[i + 1] != " ":
                    points += 3
                    stats[3] += 1
                else:
                    stats[0] += 1

            elif i > 0 and i == len(message) - 1:
                punctuation_count += 1
                if message[i - 1] != " ":
                    points += 1
                    stats[1] += 1
    if punctuation_count != 0:
        result = (points / punctuation_count) / 3
        stats = [n / punctuation_count for n in stats]
    return stats


def avg_ellipsis_length(message):
    """Метрика многоточий

    :param message: сообщение
    :return: средняя длина многоточия
    """
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


def number_of_dashes(message: str):
    """Метрика использования дефисов и коротких/длинных тире

    :param message: сообщение
    :return: массив из трёх чисел: коэффициент дефисов, коэффициент коротких
             тире, количество длинных тире
    """

    result = [
        message.count("-"),
        message.count("–"),
        message.count("—")
    ]

    dash_sum = sum(result)  # 9

    return [n / dash_sum for n in result] if dash_sum != 0 else result


def all_caps_avg_length(message):
    """Метрика использование капса

    :param message: сообщение
    :return: средняя длина подстрок, набранных капсом
    """
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


def smiley_parenthesis_avg_lengths(message):
    """Метрика использования скобочек-смайликов

    :param message: сообщение
    :return: массив из двух чисел: средняя длина подстроки вида /)+/, средняя
             длина подстроки вида /(+/
    """
    result = [0, 0]
    count_happy_brackets_seq = 0
    count_sad_brackets_seq = 0
    len_happy_brackets = 0
    len_sad_brackets = 0

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
        result[0] = len_happy_brackets / count_happy_brackets_seq
    if count_sad_brackets_seq > 0:
        result[1] = len_sad_brackets / count_sad_brackets_seq
    return result


def period_stats(message):
    """Метрика количества точек

    :param message: сообщение
    :return: коэффициент предложений, кончающихся на точку, ко всем предложениям
    """
    sentences = split_into_sentences(message)
    periods = message.count('.')
    return periods / len(sentences) if len(sentences) > 0 else 0


def capitalized_amount(message):
    """Метрика заглавных букв в начале предложений

    :param message: сообщение
    :return: коэффициент предложений, начинающихся с заглавной буквы
    """
    arr = split_into_sentences(message)
    count = 0
    for element in arr:
        if element[0].isupper():
            count += 1
    return count / len(arr) if len(arr) > 0 else 0


def uses_yo(message):
    """Метрика буквы Ё

    :param message: сообщение
    :return: True, если "Ё" есть, иначе False
    """
    return "ё" in message or "Ё" in message


# Считаем, сколько предложений содержит воскл знак, считаем общее кол-во
# предложений
# возвращаем отношение
def exclamation_amount(message):
    amt = message.count('!')
    sentences = split_into_sentences(message)

    if message[-1] == '!':
        return amt / len(sentences) if len(sentences) > 0 else 0
    else:
        return (amt - 1) / len(sentences) if len(sentences) > 0 else 0


# возвращаем количество ; в сообщении
def semicolon_amount(message):
    amt = len(split_into_sentences(message))
    return message.count(';') / amt if amt != 0 else 0


# считаем кол-во слов, которые содержат в себе подстроку из повторяющихся букв
# возвращаем отношение растянутые слова/все слова
def elongated_words(message):
    arr = message.split()
    arr = list(filter(lambda a: a != '', arr))
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


def probable_gender(message):
    words = split_into_words(message)

    if len(words) > 1 and words[0].lower() == "я":
        if len(words[1]) >= 3:
            result = 0
            for word in words[1:5]:
                if word[-3:] in ["ала", "ыла", "ола", "ила", "ела", "ула",
                                 "яла"] \
                        or word[-5:] in ["алась", "ылась", "олась", "илась",
                                         "елась", "улась", "ялась"]:
                    result += 1
                elif word[-2:] in ["ал", "ыл", "ол", "ил", "ел", "ул", "ял"] \
                        or word[-4:] in ["ался", "ылся", "олся", "ился", "елся",
                                         "улся", "ялся"]:
                    result -= 1

            return result / 4

    return 0


def get_metrics(message):
    """Возвращает массив метрик для сообщения

    :param message: сообщение
    :return: NumPy-массив чисел в формате float32
    """
    return np.array(
        [len(message),
         len(split_into_words(message)),
         *spacing_around_punctuation(message),
         avg_ellipsis_length(message),
         *number_of_dashes(message),
         all_caps_avg_length(message),
         *smiley_parenthesis_avg_lengths(message),
         period_stats(message),
         capitalized_amount(message),
         exclamation_amount(message),
         semicolon_amount(message),
         elongated_words(message),
         1 if uses_yo(message) else 0,
         probable_gender(message)],
        np.float32
    )
