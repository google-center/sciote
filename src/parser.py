def remove_blank_lines(line_list):
    element = 0
    while element < len(line_list) and line_list[element].startswith("\n"):
        line_list.pop(element)
    element = len(line_list) - 1
    while element == len(line_list) - 1 and line_list[element].startswith("\n"):
        line_list.pop(element)


file = open('chat.txt', encoding='utf-8')

message_line = file.readlines()
remove_blank_lines(message_line)

line_count = len(message_line)
name_list = []
message_list = []

i = 0
while i < line_count:
    mes = message_line[i + 1]

    if i + 1 < line_count and message_line[i + 1].startswith("\n"):
        i += 2
    else:
        line = message_line[i]
        name = line[:line.find('(') - 1]
        name_list.append(name)
        i += 1

        message = ""
        while i < line_count and not message_line[i].startswith("\n") and not \
        message_line[i].startswith("Прикрепления"):
            message += message_line[i][:message_line[i].find("\n")]
            i += 1
        message_list.append(message)

        if i < line_count and (message_line[i].startswith("Прикрепления")):
            i += 1
            while i < line_count and not message_line[i].startswith("\n"):
                i += 1
        i += 1

file.close()
