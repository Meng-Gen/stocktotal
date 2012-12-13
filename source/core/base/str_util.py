# coding: utf-8

def is_float(test_str):
    try:
        float(test_str)
        return True
    except ValueError:
        return False

def is_str(test_str):
    try:
        str(test_str)
        return True
    except ValueError:
        return False
