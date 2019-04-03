import re

import numpy as np

from config import PRIORITIES, N_VAL


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

    if len(message) and message[-1] == '!':
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
    return count / len(arr) if len(arr) > 0 else 0


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


intro_words = [u'а быть может', u'а вернее', u'а вернее сказать', u'а впрочем',
               u'а главное',
               u'а значит', u'а лучше сказать', u'а между прочим',
               u'а может быть', u'а наоборот',
               u'а например', u'а следовательно', u'а точнее',
               u'без всякого сомнения', u'без сомнения',
               u'безусловно', u'без шуток', u'бесспорно', u'благодарение богу',
               u'бог даст', u'более того',
               u'больше того', u'бывает', u'бывало', u'быть может',
               u'вдобавок ко всему прочему',
               u'верите ли', u'веришь ли', u'вернее', u'вернее говоря',
               u'вернее сказать', u'верно',
               u'вероятнее всего', u'вероятно', u'вестимо', u'видать',
               u'видимо', u'видит бог',
               u'видите ли', u'видишь ли', u'видно', u'вишь', u'в конце концов',
               u'в итоге', u'вне всякого сомнения',
               u'вне сомнения', u'в общем', u'в общем-то', u'во всяком случае',
               u'во-вторых', u'возможно',
               u'воистину', u'воля ваша', u'воля твоя', u'вообрази',
               u'вообрази себе', u'вообразите',
               u'вообразите себе', u'вообще', u'вообще говоря', u'вообще-то',
               u'во-первых', u'в принципе',
               u'впрочем', u'в самом деле', u'в свою очередь', u'в сущности',
               u'в сущности говоря', u'в-третьих',
               u'в частности', u'выходит', u'главное', u'главное дело',
               u'главным делом', u'говорят',
               u'грешным делом', u'грубо говоря', u'да и то сказать',
               u'дай бог память', u'далее',
               u'действительно', u'делать нечего', u'должно быть', u'допустим',
               u'другими словами',
               u'если позволите', u'если позволишь', u'если угодно',
               u'если хотите', u'если хотите знать',
               u'если хочешь', u'если хочешь знать', u'естественно',
               u'еще лучше', u'еще того лучше',
               u'еще того хуже', u'еще хуже', u'жалко', u'жаль', u'знаете',
               u'знаете ли', u'знаешь',
               u'знаешь ли', u'знамо', u'знамо дело', u'знать', u'значит',
               u'значится', u'и вообще',
               u'известно', u'и кроме того', u'и лучше того', u'и наоборот',
               u'иначе говоря', u'иначе сказать',
               u'и однако', u'и правда', u'истинный бог', u'и таким образом',
               u'и того лучше',
               u'и того хуже', u'и хуже того', u'кажется', u'кажись',
               u'казалось', u'казалось бы',
               u'как бы там ни было', u'как бы то ни было', u'как вам известно',
               u'как видите',
               u'как видишь', u'как видно', u'как водится', u'как всегда',
               u'как выяснилось',
               u'как выясняется', u'как говорилось', u'как говорится',
               u'как говорят', u'как знать',
               u'как известно', u'как исключение', u'как на заказ',
               u'как назло', u'как например',
               u'как нарочно', u'как ни говори', u'как ни говорите',
               u'как ни странно', u'как обычно',
               u'как оказалось', u'как оказывается', u'как перед Богом',
               u'как по заказу',
               u'как полагается', u'как положено', u'как правило',
               u'как принято', u'как принято говорить',
               u'как сказано', u'как сказать', u'как следствие', u'как хотите',
               u'как хочешь', u'как это ни странно',
               u'к вашему сведению', u'к несчастью', u'ко всему прочему',
               u'к огорчению', u'конечно',
               u'коротко говоря', u'короче', u'короче говоря', u'к примеру',
               u'к примеру сказать',
               u'к прискорбию', u'к радости', u'к радости своей',
               u'кроме всего прочего', u'кроме того',
               u'кроме этого', u'кроме шуток', u'к слову', u'к слову сказать',
               u'к сожалению', u'кстати',
               u'кстати говоря', u'кстати сказать', u'к стыду',
               u'к стыду своему', u'к счастью',
               u'к твоему сведению', u'к удивлению', u'к ужасу', u'к чести',
               u'ладно', u'легко сказать', u'лучше',
               u'лучше сказать', u'мало сказать', u'мало того', u'между нами',
               u'между нами говоря',
               u'между прочим', u'может', u'может быть', u'может статься',
               u'можно подумать', u'можно сказать',
               u'мол', u'мягко выражаясь', u'мягко говоря', u'на беду',
               u'на ваш взгляд', u'наверно',
               u'наверное', u'надеюсь', u'надо быть', u'надо думать',
               u'надо полагать', u'называется',
               u'наконец', u'на мой взгляд', u'на несчастье', u'наоборот',
               u'на первый взгляд', u'например',
               u'напротив', u'на самом деле', u'на счастье', u'на твой взгляд',
               u'натурально', u'на худой конец',
               u'небось', u'несомненно', u'нет слов', u'нечего сказать',
               u'ничего не скажешь', u'но кроме того',
               u'но вообще-то', u'однако', u'однако же', u'одним словом',
               u'оказывается', u'определенно',
               u'откровенно', u'откровенно говоря', u'откровенно сказать',
               u'очевидно', u'по-вашему',
               u'по вашему мнению', u'поверите ли', u'поверишь ли',
               u'по-видимому', u'по видимости',
               u'по всей вероятности', u'по всей видимости', u'по данным',
               u'поди', u'подумать только',
               u'пожалуй', u'пожалуйста', u'по замыслу', u'позволь',
               u'позвольте', u'по идее', u'по-ихнему',
               u'по крайней мере', u'положим', u'положимте', u'получается',
               u'помилуй', u'помилуйте',
               u'помимо всего', u'помимо всего прочего', u'помимо того',
               u'помимо этого', u'по мне',
               u'по мнению', u'помнится', u'по-моему', u'по моему мнению',
               u'по-нашему', u'понятно',
               u'понятное дело', u'по обыкновению', u'по обычаю',
               u'по определению', u'по правде',
               u'по правде говоря', u'по правде сказать', u'по преданию',
               u'по прогнозам', u'попросту говоря',
               u'попросту сказать', u'по сведениям', u'по своему обыкновению',
               u'по словам', u'по слухам',
               u'по совести', u'по совести говоря', u'по совести сказать',
               u'по сообщению', u'по сообщениям',
               u'по справедливости', u'по справедливости говоря', u'по сути',
               u'по сути дела', u'по сути говоря',
               u'по существу', u'по существу говоря', u'по счастью',
               u'по-твоему', u'по твоему мнению',
               u'похоже', u'по чести говоря', u'по чести признаться ',
               u'по чести сказать', u'почитай',
               u'правда', u'правду говоря', u'правду сказать', u'правильнее',
               u'правильнее говоря',
               u'правильнее сказать', u'право', u'право слово', u'предположим',
               u'предположительно',
               u'представь', u'представь себе', u'представьте',
               u'представьте себе', u'прежде всего',
               u'признаться', u'признаться сказать', u'признаюсь', u'примерно',
               u'против обыкновения',
               u'проще говоря', u'проще сказать', u'разумеется', u'само собой',
               u'само собой разумеется',
               u'с вашего позволения', u'с вашего разрешения', u'сверх того',
               u'с другой стороны',
               u'серьезно', u'скажем', u'сказать по правде',
               u'сказать по совести', u'сказать по чести',
               u'скорее', u'скорее всего', u'слава богу', u'следовательно',
               u'слов нет', u'словом',
               u'случаем', u'случайно', u'слыхать', u'слышно', u'слышь',
               u'слышь ты', u'с моей точки зрения',
               u'собственно', u'собственно говоря', u'с одной стороны',
               u'соответственно',
               u'со своей стороны', u'с позволения сказать', u'спрашивается',
               u'стало быть',
               u'с твоего позволения', u'с твоего разрешения',
               u'с точки зрения', u'строго говоря',
               u'судя по всему', u'так', u'таким образом', u'так или иначе',
               u'так сказать', u'точнее',
               u'точнее говоря', u'точнее сказать', u'факт', u'хорошо', u'чай',
               u'часом', u'чего доброго',
               u'что и говорить', u'что называется', u'что ни говори',
               u'что ни говорите', u'шутка ли',
               u'шутка ли сказать', u'шутка сказать', u'ясное дело', 'отвечаю',
               'жаль', 'блин']


# Commas around introductory words
# if yes                                       ->  point = 2
# if no                                        ->  point = 1
# if no introductory words in message or
# if message consists of one introductory word ->  point = 0
def commas_around_introductory_words(message):
    message = message.lower()
    message_ = message.replace('.', '').replace('  ', '').split(",")
    points = 0
    for intro_word in intro_words:
        if intro_word in message_ and len(message_) > 1:
            points += 2
        elif intro_word in message:
            message = str(message).split(" ")
            if len(message) > 1:
                points += 1
    return points / len(intro_words) if len(intro_words) > 0 else 0


subordination_unions = ['чтобы', 'будто', 'когда', 'пока', 'ибо', 'потому что',
                        'оттого что', 'так как',
                        'т.к.', 'т.е.', 'дабы', 'если', 'словно', 'так что',
                        'что', 'как']


# Commas before subordination unions
def commas_before_subordination_unions(message):
    for i in range(0, len(subordination_unions) - 1):
        message = message.replace(subordination_unions[i], '<U>')
    words = message.split(" ")
    points_yes = 0
    points_no = 0
    for i in range(0, len(words)):
        if words[i] == "<U>" and "." not in words[i - 1] and "!" not in words[
            i - 1] \
                and "?" not in words[i - 1] and i > 0:
            if "," in words[i - 1]:
                points_yes += 1
            else:
                points_no += 1

    # if points_yes == 0:
    #     return 1
    # elif points_no == 0:
    #     return 2
    # else:
    return points_yes / (points_yes + points_no) if (points_yes + points_no) > 0 else 0


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
         probable_gender(message),
         commas_around_introductory_words(message),
         commas_before_subordination_unions(message)],
        np.float32
    )


def get_weighted_metrics(message):
    metrics = np.array(
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
         probable_gender(message),
         commas_around_introductory_words(message),
         commas_before_subordination_unions(message)],
        np.float32
    )

    for i in range(len(metrics)):
        metrics[i] = metrics[i] / N_VAL * PRIORITIES[i]

    return metrics
