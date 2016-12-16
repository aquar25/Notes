#!/usr/bin/env python
# -*- coding:utf-8 -*-


def letter_in_phrase(phrase: str, letters: str='aeiou') -> set:
    """Get the letters in the phrase"""
    return set(letters).intersection(set(phrase))
