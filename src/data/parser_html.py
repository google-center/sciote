import os
import lxml.html as html

# files_path - относительный путь папки с файлами HTML
def parse_html(files_path):
    label_list = []
    message_list = []
    attachment_list = []

    for html_file in os.listdir(files_path):
        page = html.parse(files_path + "/" + html_file)
        message_blocks = page.xpath('//div[@class = "message"]')
        
        for message_block in message_blocks:

            label = message_block.xpath('.//div[@class = "message__header"]/a/text()')
            label_list.append(label[0] if label else None)

            attachment = message_block.xpath('.//div[@class = "attachment__description"]/text()')
            attachment_list.append(attachment[0] if attachment else None)

            message = message_block.xpath('.//div/text()')[1]
            message_list.append(message if message != '\n  ' else None)
            print("Parcing " + html_file)

    return message_list, label_list, attachment_list

