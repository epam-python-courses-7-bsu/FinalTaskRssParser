import colored

def colorize_text(data: dict):
    yellow = colored.fg(11)
    red = colored.fg(9)
    green = colored.fg(82)
    pink = colored.fg(200)
    blue = colored.fg(20)
    description_color = colored.fg(14)
    default = colored.fg(230)
    print()
    if 'error' in data.keys():
        print(('{0} ' + data['error'] + ' {1}').format(red, default))
    print(('{0} ' + data['title'] + '\n').format(yellow))
    for index_news, dict_news in enumerate(data['items']):
        print(('{0}Title: {1}' + dict_news['title']).format(green, red))
        print(('{0}Date: {1}' + dict_news['published']).format(green, pink))
        print(('{0}Link: {1}' + dict_news['link']).format(green, blue))
        print(('{0}Description: {1}' + dict_news['summary'] + '{2}\n').format(green, description_color, default))
    print('{0}Links:'.format(colored.fg(89)))
    for index_links, link in enumerate(data['links']):
        print(('{0}[' + str(index_links+1) + '] - {1}' + link + '{2}').format(green, blue, default))
