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
    print(f"{yellow} {data['title']} {default}")
    for index_news, dict_news in enumerate(data['items']):
        print(f"{green}Title: {red}{data['title']} ")
        print(f"{green}Title: {pink}{data['published']} ")
        print(f"{green}Title: {blue}{data['link']} ")
        print(f"{green}Title: {description_color}{data['summary']}{default} ")
    print(f'{colored.fg(89)}Links:')
    for index_links, link in enumerate(data['links']):
        print(f'{green}[{index_links+1}] - {blue}{default}')
