from string import ascii_letters, whitespace
import re

def clean_title(text):
    "Delete unnecessary symbols"
    good_chars = (ascii_letters + whitespace).encode()
    junk_chars = bytearray(set(range(0x100)) - set(good_chars))
    return text.encode('ascii', 'ignore').translate(None, junk_chars).decode()