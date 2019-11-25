from string import ascii_letters, whitespace
import re

def delete_unnecessary_symbols(text):
    "Delete unnecessary symbols"
    good_chars = (ascii_letters + whitespace).encode()
    junk_chars = bytearray(set(range(0x100)) - set(good_chars))
    return text.encode('ascii', 'ignore').translate(None, junk_chars).decode()