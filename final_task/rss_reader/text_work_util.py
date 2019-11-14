import feedparser
import html
import logging


def take_info(source: str, limit: str):
    # take info from URL and create dict to storage news
    logging.info("function that take info from URL and create dict to storage news")
    all_info = feedparser.parse(source)
    if all_info.bozo:
        dict_whit_info = 'Should try better url instead yours'
    else:
        dict_whit_info = {'Feed': all_info.feed.title,
                          'Title': [],
                          'Date': [],
                          'Links': [],
                          'Info': []}
        if limit:
            limit = all_info.entries[0:int(limit)]
        else:
            limit = all_info.entries

        for i in limit:
            dict_whit_info['Title'] += [i.title]
            dict_whit_info['Date'] += [i.published]
            dict_whit_info['Links'] += [i.link]
            dict_whit_info['Info'] += [i.summary]

    return dict_whit_info


def make_links_better(links_list: list):
    # delete everything after '?' symbol from links
    logging.info("function that delete everything after '?' symbol from links")
    if '?' in links_list[0]:
        for link in links_list:
            true_line = link.split('?')[0]
            if link == links_list[0]:
                links_list = [true_line]
            else:
                links_list += [true_line]

    return links_list


def news_output(dict_whit_info: dict, limit: str):

    if type(dict_whit_info) == dict:
        print('\n' + 'Feed: ' + dict_whit_info['Feed'])

        for index in range(int(limit)):
            print('\n' + 'Title: ' + dict_whit_info['Title'][index])
            print('Date: ' + dict_whit_info['Date'][index])
            print('Link: ' + dict_whit_info['Links'][index])
            print('Info: ' + dict_whit_info['Info'][index])
    else:
        print(dict_whit_info)


def make_text_better(text_of_news_list: list):
    # get text from 'summary' to print
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


def make_all_text_better(dict_with_info: dict):
    logging.info("function that calls all other methods ")
    if type(dict_with_info) == dict:
        dict_with_info['Links'] = make_links_better(dict_with_info['Links'])
        dict_with_info['Info'] = make_text_better(dict_with_info['Info'])
        dict_with_info['Title'] = deleting_bad_symbols(dict_with_info['Title'])
        dict_with_info['Info'] = deleting_bad_symbols(dict_with_info['Info'])


def deleting_bad_symbols(list_with_text: list):
    logging.info("function that delete such symbols as &#39; from text")
    # delete such symbols as &#39; from text
    for number_of_new, word in enumerate(list_with_text):
        list_with_text[number_of_new] = html.unescape(word)
    return list_with_text
