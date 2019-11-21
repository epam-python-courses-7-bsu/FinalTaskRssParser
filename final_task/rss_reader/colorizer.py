from termcolor import cprint


def printc(text, color):
    if color:
        cprint(text, 'green')
    else:
        print(text)


def print_link(link, color):
    if color:
        cprint(link, 'blue', attrs=['underline'])
    else:
        print(link)


def print_blink(text, color):
    if color:
        cprint(text, 'white', attrs=['blink'])
    else:
        print(text)

def printerr(text, color):
    if color:
        cprint(text, 'red')
    else:
        print(text)
