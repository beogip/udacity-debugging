import random

def fuzzer():
    string_length = int(random.random() * 1024)   # Strings up to 1024 characters long
    out = ""
    for i in range(0, string_length):
        out += chr(int(random.random() * 96 + 32)) # filled with ASCII 32..128
    return out