# -*- coding: utf-8 -*-
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def to_dict(type, naam, prijs, zicht):
    return {'naam':naam, 'type':type, 'prijs':prijs, 'zichtbaar':zicht}