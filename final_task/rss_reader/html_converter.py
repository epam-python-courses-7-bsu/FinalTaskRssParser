import urllib.request


def is_connected() -> bool:
    """Checks internet connection"""
    hostname = 'https://www.google.com/'
    try:
        urllib.request.urlopen(hostname)
        return True
    except urllib.request.HTTPError:
        return False
    except urllib.request.URLError:
        return False


def convert_to_html(articles_list: list, path: str) -> None:
    """Converts articles to html format"""
    html = "<html>\n\n"
    html += "<head>\n\t<title>\n\t\tNEWS\n\t</title>\n"
    style = """\t<style>
        body {
            padding: 1em;
        }     

        th {
            width: 80px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        td, 
        th {
            padding: .25em;
            border: 1px solid black;
        }
    </style>\n"""

    html += style
    html += "</head>\n\n<body>\n"

    connection = is_connected()

    for index, value in enumerate(articles_list, 1):
        html += f'\t<h3>Article #{index}</h3>\n'
        html += f'\t<table>\n'
        html += f'\t\t\t<tr>\n\t\t\t\t<th>Feed</th>\n\t\t\t\t<td>' \
                f'{value.feed}</td>\n\t\t\t</tr>\n'
        html += f'\t\t\t<tr>\n\t\t\t\t<th>Title</th>\n\t\t\t\t<td>' \
                f'{value.title}</td>\n\t\t\t</tr>\n'
        html += f'\t\t\t<tr>\n\t\t\t\t<th>Date</th>\n\t\t\t\t<td>' \
                f'{value.date}</td>\n\t\t\t</tr>\n'
        html += f'\t\t\t<tr>\n\t\t\t\t<th>Link</th>\n\t\t\t\t<td>' \
                f'<a href=\"{value.link}\">{value.link}</a></td>\n\t\t\t</tr>\n'
        html += f'\t\t\t<tr>\n\t\t\t\t<th>Article</th>\n\t\t\t\t<td>' \
                f'{value.summary}</td>\n\t\t\t</tr>\n'

        if connection:
            for number, link in enumerate(value.links, 1):

                if link[1] == 'image':
                    if number == 1:
                        html += f'\t\t\t<tr>\n\t\t\t\t<th rowspan="{len(value.links)}">' \
                                f'Links:</th>\n\t\t\t\t<td>[{number}]: ' \
                                f'<a href=\"{link[0]}\"><img src=\"{link[0]}\" alt={link[0]}></a>\n' \
                                f'\t\t\t\t</td>\n\t\t\t</tr>\n'
                    else:
                        html += f'\n\t\t\t<tr>\n\t\t\t\t<td>[{number}]: ' \
                                f'<a href=\"{link[0]}\"><img src=\"{link[0]}\" alt={link[0]} height="400"></a>\n' \
                                f'\t\t\t\t</td>\n\t\t\t</tr>\n'
                else:
                    if number == 1:
                        html += f'\t\t\t<tr>\n\t\t\t\t<th rowspan="{len(value.links)}">' \
                                f'Links:</th>\n\t\t\t\t<td>[{number}]: ' \
                                f'<a href=\"{link[0]}\">{link[0]}</a>\n\t\t\t\t</td>\n\t\t\t</tr>\n'
                    else:
                        html += f'\n\t\t\t<tr>\n\t\t\t\t<td>[{number}]: ' \
                                f'<a href=\"{link[0]}\">{link[0]}</a>\n\t\t\t\t</td>\n\t\t\t</tr>\n'
        else:
            for number, link in enumerate(value.links, 1):
                if number == 1:
                    html += f'<tr><th rowspan="{len(value.links)}">Links:</th><td>[{number}]: ' \
                            f'<a href=\"{link[0]}\">{link[0]}</a></td></tr>\n'
                else:
                    html += f'<tr><td>[{number}]: <a href=\"{link[0]}\">{link[0]}</a></td></tr>\n'

        html += "\t</table>\n"

    html += "</body>\n\n</html>"
    try:
        with open(path, 'w', encoding="utf-8") as the_file:
            the_file.write(html)
    except PermissionError:
        print('You need to run program as system administrator, to save files in that location')
