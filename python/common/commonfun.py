#!/usr/bin/env python3
# -*- coding:utf-8 -*-


def letter_in_phrase(phrase: str, letters: str='aeiou') -> set:
    """Get the letters in the phrase"""
    return set(letters).intersection(set(phrase))

import struct

def hex2float(hex_str):
    return struct.unpack('!f', bytes.fromhex(hex_str))[0]

from ctypes import *

def hex2float_ctype(hex_str):
    i = int(hex_str, 16)             # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value         # dereference the pointer, get the float


if __name__ == '__main__':
    print(hex2float('41973333'))
    print(hex2float_ctype('41973333'))
    print(hex2float('381AA344'))

    print(struct.unpack('!f',b'\x38\x1A\xA3\x44'))