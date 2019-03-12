import re
import sys


def parse_file(filename):
    try:
        file = open(filename, encoding='utf-8')
    except FileNotFoundError:
        print(f"File {filename} not found.")
        sys.exit(1)

    lines = file.readlines()
    line_count = len(lines)
    name_list = []
    message_list = []

    # Имя Фамилия (01 янв. 1970 г. 0:00:00):
    lbl_pat = re.compile(
        r"^([A-Za-zА-Яа-яЁё]+ [A-Za-zА-Яа-яЁё]+) \(\d+ [а-я]+.? \d{4} г. \d{1,2}:\d{2}:\d{2}\):$")

    i = 0
    while i < line_count:
        # проверяем, является ли строка лейблом
        match = re.match(lbl_pat, lines[i])

        # если это лейбл
        if match:
            # вытаскиваем имя
            name = match.group(1)
            msg = ''
            i += 1
            skip = False

            # для каждой строки, которая не является лейблом
            while not re.match(lbl_pat, lines[i]):
                # если начались прикрепления, то сообщение закончилось
                if not skip and lines[i].strip().endswith('Прикрепления:'):
                    skip = True
                if not skip:
                    msg += lines[i]

                i += 1

                # последнее сообщение отправляет цикл
                # за рамки списка -> исправляем
                if i == line_count:
                    break

            if msg.strip() != '':
                name_list.append(name)
                # обрезаем сообщение, чтобы не хранить символы новой строки
                message_list.append(msg.strip())
        else:
            i += 1

    file.close()

    # функция возвращает по отдельности сообщения и лейблы
    return message_list, name_list
