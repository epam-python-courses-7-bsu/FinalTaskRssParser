import feedparser
import html
import logging
import sys


def fill_dict_with_info(dict_with_info: dict, all_info: object, limit: str) -> tuple:
    if limit:

        try:
            if int(limit) > len(all_info.entries) or int(limit) < 0:
                limit = int(limit)
            else:
                limit = all_info.entries[0:int(limit)]
        except ValueError:
            print('\n Should try only integer numbers')
            sys.exit()

    else:
        limit = all_info.entries

    try:
        for enter in limit:
            dict_with_info['Title'] += [enter.title]
            dict_with_info['Date'] += [enter.published]
            dict_with_info['Links'] += [enter.link]
            dict_with_info['Info'] += [enter.summary]
            link, description = img_link_take(enter.summary)
            dict_with_info['Picture'] += [change_ascii(description) + ':  ' + link]
    except TypeError:
        print('\nTry other limit ')
        sys.exit()

    return dict_with_info, limit


def parse_info(source: str) -> tuple:
    """ take info from URL and create dict to storage news """

    logging.info("function that take info from URL and create dict to storage news")
    all_info = feedparser.parse(source)

    if all_info.bozo:
        dict_whit_info = 'Should try better url instead yours'
    else:
        dict_whit_info = {'Feed': all_info.feed.title,
                          'Title': [],
                          'Date': [],
                          'Links': [],
                          'Info': [],
                          'Picture': []}

    return dict_whit_info, all_info


def remove_part(links_list: list) -> list:
    """remove useless part from links"""

    logging.info("function that remove useless part from links")
    if '?' in links_list[0]:
        for link in links_list:
            true_line = link.split('?')[0]
            if link == links_list[0]:
                links_list = [true_line]
            else:
                links_list += [true_line]

    return links_list


def news_output(dict_with_info: dict, limit: str):

    if isinstance(dict_with_info, dict):
        print('\n' + 'Feed: ' + dict_with_info['Feed'])

        for index, _ in enumerate(limit):
            print('\n' + 'Title: ' + dict_with_info['Title'][index])
            print('Date: ' + dict_with_info['Date'][index])
            print('Link: ' + dict_with_info['Links'][index])
            print('Info: ' + dict_with_info['Info'][index])
            print('\nPicture link and description for it: ' + dict_with_info['Picture'][index])


def find_text_in_summary(text_of_news_list: list) -> list:
    """ get text from 'summary' to print """
    logging.info("function that get text from 'summary' and make look better")
    for number_of_new, text in enumerate(text_of_news_list):
        bad_list = text.split('>')
        for index, sentence in enumerate(bad_list):
            if sentence:
                if sentence[0].upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ0123456789(«"':
                    temp = sentence.split('<')
                    text_of_news_list[number_of_new] = temp[0]

    for index, message in enumerate(text_of_news_list):
        if message[0] == '<':
            text_of_news_list[index] = 'No more info here'

    return text_of_news_list


def calling_func(dict_with_info: dict):
    logging.info("function that calls all other methods ")
    if isinstance(dict_with_info, dict):
        dict_with_info['Links'] = remove_part(dict_with_info['Links'])
        dict_with_info['Info'] = find_text_in_summary(dict_with_info['Info'])
        dict_with_info['Title'] = change_ascii(dict_with_info['Title'])
        dict_with_info['Info'] = change_ascii(dict_with_info['Info'])


def change_ascii(list_with_text: list or str) -> list or str:
    """ change such symbols as &#39; into text """

    logging.info("change such symbols as &#39; into text")
    if isinstance(list_with_text, list):
        for number_of_new, word in enumerate(list_with_text):
            list_with_text[number_of_new] = html.unescape(word)
    else:
        list_with_text = html.unescape(list_with_text)
    return list_with_text


def img_link_take(string: str) -> tuple:
    """ Get links of pictures from summary """
    logging.info("function that Get links of pictures from summary")

    string = string[string.find('<img')+5:]

    first_cut = string[string.find('src="') + 5:string.find('>')]

    link = first_cut[:first_cut.find('"')]
    second_cut = first_cut[first_cut.find('alt="')+5:]

    description = second_cut[:second_cut.find('"')]

    """If src contain two links """
    if 'http' in link[link.find('http')+5:]:
        link = link[link.find('http')+5:]
        link = link[link.find('http'):]

    if not link:
        link = 'Could not find link for picture'
    if not description:
        description = 'This picture has no description'

    return link, description

