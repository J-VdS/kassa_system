# -*- coding: utf-8 -*-
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
