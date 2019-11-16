
def cut_string_to_length_with_space(basic_str, length):
    """function that cut given string to the list of strings with a given max length"""
    my_strings = []
    my_str = ''
    for i, word in enumerate(basic_str.split()):
        my_str += word + ' '
        if i + 1 < len(basic_str.split()):
            next_word = basic_str.split()[i+1]
        else:
            next_word = ''
            my_strings.append(my_str)
        if len(my_str + next_word) >= length:
            my_strings.append(my_str)
            my_str = ''
    return my_strings


def make_string_readable(basic_str):
    """return copy of string, replace &#39; to ' and &quot; to " """
    my_str = basic_str[:]
    my_str = my_str.replace('&quot;', '\"')
    my_str = my_str.replace('&#39;', "\'")
    return my_str


def extract_topic_info_from_summary(basic_str):
    start = basic_str.find('></a>')
    len_ = 5
    if start == -1:
        start = basic_str.find('/>')
        len_ = 2
    if start == -1:
        start = 0
        len_ = 0
    end = basic_str.find('<p><br')
    if end == -1:
        end = basic_str.find('<br')
    if end == -1:
        end = len(basic_str)
    return basic_str[start + len_:end]


def extract_image_info_from_summary(basic_str):

    start_description = basic_str.find('alt="')
    len_ = len('alt="')
    if start_description == -1:
        start_description = 0
        len_ = 0
    end_description = min(basic_str.find('" border='), basic_str.find('" align='))
    if end_description == -1:
        end_description = len(basic_str)

    media_description = basic_str[start_description + len_: end_description]
    return media_description


def extract_date(parsed):
    try:
        date = parsed.published
    except KeyError:
        date = parsed.updated
    return date
