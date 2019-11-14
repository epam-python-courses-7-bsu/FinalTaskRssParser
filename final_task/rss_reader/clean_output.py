from string import ascii_letters, whitespace
import re

def delete_html(summary):
    "Delete html, take description"
    clean_summary_list = re.findall('</a>(.+)<p>', summary)
    clean_summary_str = ' '.join(clean_summary_list)
    return clean_summary_str

def clean(text):
    "Delete unnecessary symbols"
    good_chars = (ascii_letters + whitespace).encode()
    junk_chars = bytearray(set(range(0x100)) - set(good_chars))
    return text.encode('ascii', 'ignore').translate(None, junk_chars).decode()