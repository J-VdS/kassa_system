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


#datastructuur voor alle info
#gebruikt in client maar aangepast
class Client_storage():
    def __init__(self):
        self._prod = {}
        self._prod_list = []
        
        #bevat alle info voor de server en de kassa
        self.bestelling = {} #{prod:aantal}
        self.info = {}#ID, prijs, 
        
    
    
    #setters
    def set_prod(self, prod):
        '''
            prod (dict): {type:[product,]}
        '''
        self._prod = prod
        for type in self._prod:
            for prod in self._prod[type]:
                self._prod_list.append((type, prod))
                    
    
    def set_prod_list(self, prod):
        self._prod_list = prod            
    
    
    def set_bestelling(self, bestelling):
        print("[BST] nieuwe bestelling:",bestelling)
        self.bestelling = bestelling
        
    
    def set_info(self, info):
        self.info = info
        
    #getters
    def get_bestelling(self):
        return self.bestelling
    
    
    def get_prod(self):
        return self._prod_list
    
    
    #def get_sort_prod(self):
    #    return sorted(self._prod_list, key=lambda el: el[1])
    
    #def get_opm(self):
    #    return self.bestelling["opm"]
    
 
    def get_num_pages(self, COLS, ROWS):
        geh, rest = divmod(len(self._prod_list), COLS*ROWS)
        return geh if (rest==0) else (geh + 1)
    
    #bestelling
    def bestelling_add_prod(self, prod, aantal, opm=None):
        '''
            voegt een product toe aan de bestelling        
        '''
        if prod in self.bestelling:
            self.bestelling[prod] += aantal
        else:
            self.bestelling[prod] = aantal
            
    
    def bestelling_list(self):
        msg = []
        for key in self.bestelling:
            msg.append("{:<28}{}".format(key, self.bestelling[key]))
        return msg
            