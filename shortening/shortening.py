from operator import xor
from math import ceil

__author__ = 'Romain'


def encode(number, base=62):
    ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    converted = []
    while number > 0:
        converted.append(ALPHABET[number % base])
        number //= base
    return ''.join(reversed(converted))

def to_hex(nb, nb_len=2):
    if nb == 0:
        return "0" * nb_len
    str_hex = hex(nb)[2::]
    return str_hex if len(str_hex) >= nb_len else "{}{}".format("0" * (nb_len - len(str_hex)), str_hex)

def process_url(base, url):
    if len(url) > len(base):
        base *= ceil(len(url) / len(base))
    base = base[:len(url)]

    # apply xor
    xored = list(map(lambda a, b: xor(a, b), base, url))
    number = int(''.join(to_hex(val) for val in xored[-8:]), 16)
    return encode(number)

if __name__ == "__main__":
    base_url_str = input().strip()
    base_url = [ord(c) for c in base_url_str]
    n = int(input())
    urls = [[ord(c) for c in input().strip()] for _ in range(0, n)]
    shortened = [process_url(base_url, url) for url in urls]
    print('\n'.join(map(lambda x : "{}/{}".format(base_url_str, x), shortened)))
