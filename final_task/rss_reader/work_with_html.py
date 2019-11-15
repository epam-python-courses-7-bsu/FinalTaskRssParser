import os
import datetime


def write_to_html_file(data: dict, path: str):
    if os.path.isdir(path):
        date_str = datetime.datetime.now().date().strftime('%Y%m%d')
        filename = path + os.path.sep + date_str + '_' + data['title'][:data['title'].find(' ')].replace(':', '') + '.html'
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(text_processing_for_html(data))
        return f'the recording has been completed in the file:\n{filename}'
    else:
        return f'{path} is not found'

def text_processing_for_html(data: dict):
    style = '<style type="text/css">body{text-align: center; font-size: 120%;' + \
            'font-family: Verdana, Arial, Helvetica, sans-serif;' + \
            'color: #333366; } </style>'
    result = '<!DOCTYPE html><html><head><title>' + data['title'] + '</title>' + style + '</head><center><h1>' \
             + data['title'] + '</h1></center><br>'
    for index_news, dict_news in enumerate(data['items']):
        result += '<h3><center><a href="' + dict_news['link'] + '">' + dict_news['title'] + '</a></center></h3>'
        result += dict_news['published'] + '<br>'
        result += '<img src="' + data['links'][index_news] + '" alt="' + \
                  dict_news['summary'][dict_news['summary'].find(': ') + 1:dict_news['summary'].find(']')] + '"><br>'
        result += dict_news['summary'][dict_news['summary'].rfind(']') + 1:]
        result += '<br><br>'
    return result


