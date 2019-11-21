from json import dumps as jdumps
from dataclasses import asdict


def news_as_json_str(item_group):
    """ Convert news in json format

    :type item_group: 'item_group.ItemGroup'
    :rtype: str
    """
    news_dict = asdict(item_group)

    return jdumps(news_dict, indent=4, ensure_ascii=False)


def news_as_json_str_from_list(item_groups):
    """ Convert list of news in json format

    :type item_groups: list of 'item_group.ItemGroup'
    :rtype: str
    """
    lst = [asdict(item_gr) for item_gr in item_groups]

    return jdumps(lst, indent=4, ensure_ascii=False)


def news2html(item_groups):
    """ Convert news to HTML code

    :type item_groups: list of 'item_group.ItemGroup'
    :return: HTML code
    :rtype: str
    """
    green_line = '<hr align=center size=3 width=70% color=green>'
    font = '../fonts/DejaVuSansCondensed.ttf'

    html_code = '<html><head><title>News</title><meta content="text/html; charset=utf-8" http-equiv="Content-Type">' \
                '<style>@font-face {font-family: DejaVuSans;src: url("' + font + '");}' \
                'body {font-family: DejaVuSans;}</style></head><body>_content_</body></html>'

    content = ''

    for item_gr in item_groups:
        item_gr_html = '<div>' + green_line + '<h1 align=center>' + item_gr.feed + '</h1>' + green_line + \
                       '<div>' + items2html(item_gr.items) + '</div></div>'
        content += item_gr_html

    html_code = html_code.replace('_content_', content)

    return html_code


def items2html(items):
    """ Convert items to HTML code

    :type items: list of 'item.Item'
    :return: HTML code
    :rtype: str
    """
    black_line = '<hr align=center size=1 width=70% color=black>'
    source_link_text = 'Go to source..'
    items_html = ''

    for item in items:
        itm_html = '<div style="margin: 60px 15% 20px 15%;"><h3 align=center>' + item.title + '</h3>' + \
                    '<p align="justify">' + item_text_with_imgs2html(item.text, item.img_links) + '</p>' + \
                    '<br><small><i><a href=' + item.link + ' color=blue>' + source_link_text + '</a><br>' + \
                    '<span style="float:right; margin-right:90">' + str(item.date) + '</span></i></small><br></div>'

        items_html += itm_html + black_line

    items_html = items_html[:-len(black_line)]
    return items_html


def item_text_with_imgs2html(text, img_links):
    """ Convert text with images to HTML code

    :type text: str
    :type img_links: list of str

    :return: HTML code
    :rtype: str
    """
    text_and_imgs = ''

    for i, link in enumerate(img_links):
        img_num = i + 1
        img_begin = text.find(f'[image {img_num}:')
        img_end = text.find(f'[{img_num}]', img_begin) + len(str(img_num)) + 2

        len_num = len(str(img_num))
        alt = text[img_begin+len_num+9:img_end-len_num-3]

        before_picture = text[:img_begin]
        text = text[img_end:]

        if before_picture:
            text_and_imgs += before_picture

        text_and_imgs += '<p style="text-align: center;">' \
                         '<img src="' + link + '" alt="' + alt + '" style="margin-bottom: 30px;"></p>'

    text_and_imgs += text
    return text_and_imgs
