import os
from bs4 import BeautifulSoup

# files_path - относительный путь папки с файлами HTML
def parse_html(files_path):
    label_list = []
    message_list = []
    attachment_list = []

    for html_file in os.listdir(files_path):
        soup = BeautifulSoup(open(files_path + "/" + html_file).read(), features="html.parser")
        messages_blocks = soup.find_all('div', {'class': 'message'})

        for messages_block in messages_blocks:

            label = messages_block.find('a')
            label_list.append(label.text if label else None)

            attachment = messages_block.find('div', {'class': 'attachment__description'})
            attachment_list.append(attachment.text if attachment else None)

            messages_block.find('div', {'class': 'kludges'}).decompose()
            messages_block.find('div', {'class': 'message__header'}).decompose()
            message_list.append(messages_block.find('div').text)

    return label_list, message_list, attachment_list
