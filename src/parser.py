import codecs


def remove_blank_lines(lineList):
    element = 0
    while element < len(lineList) and lineList[element].startswith("\n"):
        lineList.pop(element)
    element = len(lineList) - 1
    while element == len(lineList) - 1 and lineList[element].startswith("\n"):
        lineList.pop(element)


handle = codecs.open('vtorograund.txt', encoding='utf-8')

messageLine = handle.readlines()
remove_blank_lines(messageLine)

lineCount = len(messageLine)
nameList = []
messageList = []

i = 0
while i < lineCount:
    mes = messageLine[i+1]

    if i + 1 < lineCount and messageLine[i + 1].startswith("\n"):
        i += 2
    else:
        line = messageLine[i]
        name = line[:line.find('(') - 1]
        nameList.append(name)
        i += 1

        message = ""
        while i < lineCount and not messageLine[i].startswith("\n") and not messageLine[i].startswith("Прикрепления"):
            message += messageLine[i][:messageLine[i].find("\n")]
            i += 1
        messageList.append(message)

        if i < lineCount and (messageLine[i].startswith("Прикрепления")):
            i += 1
            while i < lineCount and not messageLine[i].startswith("\n"):
                i += 1
        i += 1

handle.close()
