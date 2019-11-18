import colored


def colorize_text(data: dict):
    yellow = colored.fg(11)
    red = colored.fg(9)
    green = colored.fg(82)
    pink = colored.fg(200)
    blue = colored.fg(20)
    description_color = colored.fg(14)
    default = colored.fg(230)
    result = '\n'
    result += f"{yellow} {data['title']} {default}\n\n"
    for index_news, dict_news in enumerate(data['items']):
        result += f"{green}Title: {red}{dict_news['title']}\n"
        result += f"{green}Date: {pink}{dict_news['published']}\n"
        result += f"{green}Link: {blue}{dict_news['link']}\n"
        result += f"{green}Description: {description_color}{dict_news['summary']}\n"
        if dict_news['contain_image']:
            result += f"{green}Link on image: {blue}{dict_news['link_on_image']}{default}\n\n"
    return result
