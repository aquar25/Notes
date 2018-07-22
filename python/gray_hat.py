from ctypes import *

def call_vc_dll():
    msvcrt = cdll.msvcrt
    print(cdll.msvcrt)
    message_string = "Hello world!\n"
    msvcrt.printf("Testing: %s", message_string)

if __name__ == '__main__':
    call_vc_dll()