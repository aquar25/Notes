import re

def match_chater_index(text):
    # \d+ 一位或多位数字 (?:\.\d+){0,3}表示这个组里面的内容重复0到3次，?:表示这个括号的内容不作为组列出来
    pattern = re.compile(r'(\d+\.\d+(?:\.\d+){0,3})')
    m = pattern.findall(text)
    return m

def test_match_function():
    text = "2.1 life is always hard to confront 5.3.1 6.5.4.2 4.3.2.1.0 5.5.4.3.2.1"
    # ['2.1', '5.3.1', '6.5.4.2', '4.3.2.1.0', '5.5.4.3.2']
    print(match_chater_index(text))

if __name__ == "__main__":
    test_match_function()