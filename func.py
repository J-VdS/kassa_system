# -*- coding: utf-8 -*-
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def to_dict(type, naam, prijs, zicht):
    return {'naam':naam, 'type':type, 'prijs':prijs, 'zichtbaar':zicht}


def sort_by_type(data):
    #recht van db (type, naam)
    d = {}
    for type, naam in data:
        if not(type in d):
            d[type] = [naam]
        else:
            d[type].append(naam)
    return d