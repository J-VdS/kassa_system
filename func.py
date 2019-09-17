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
        self.edit = {}
        self.info = {}#ID, prijs, 
        

    #setters
    def set_prod(self, prod):
        '''
            prod is lijst bestaande uit [(type, naam, prijs)]
        '''
        for type, naam, prijs in prod:
            self._prod[naam] = (type, naam, prijs)
        self._prod_list = prod
        
    
    def set_prod_list(self, prod):
        self._prod_list = prod            
    
    
    def set_bestelling(self, bestelling):
        #print("[BST] nieuwe bestelling:",bestelling)
        self.bestelling = bestelling
        
    
    def set_info(self, info):
        self.info = info
        self.edit_reset()
        
    #getters
    def get_bestelling(self):
        return self.bestelling
    
    
    def get_prod(self):
        return self._prod_list
    
    
    def get_edit(self):
        return self.edit
    
    
    #def get_sort_prod(self):
    #    return sorted(self._prod_list, key=lambda el: el[1])
    
    #def get_opm(self):
    #    return self.bestelling["opm"]
    
 
    def get_num_pages(self, COLS, ROWS):
        geh, rest = divmod(len(self._prod_list), COLS*ROWS)
        return geh if (rest==0) else (geh + 1)
    
    
    def get_info(self):
        return self.info
    
    #bestelling
    def edit_reset(self):
        self.edit = {}
    
    
    def bestelling_add_prod(self, prod, aantal, opm=None):
        '''
            voegt een product toe aan de bestelling        
        
        if (aantal < 0) and not(prod in self.bestelling) and (self.edit.get(prod, 0) == 0):
            return -1        
        elif prod in self.edit:
            if self.bestelling.get(prod, 0) + self.edit[prod] + aantal < 0: #plus aantal want aantal zal in dit geval negatief zijn
                return -1
            else:
                self.edit[prod] += aantal
                return 0
        else:
            if self.bestelling.get(prod, 0) + aantal < 0:
                return -1
                
            else:
                self.edit[prod] = aantal
                return 0
        '''
        if (aantal < 0):
            if self.edit.get(prod, 0) + self.bestelling.get(prod, 0) + aantal < 0:
                return -1
            else:
                self.edit[prod] = self.edit.get(prod, 0) + aantal
                return 0
        else:
            self.edit[prod] = self.edit.get(prod, 0) + aantal
            return 0
        
    def bestelling_del_prod(self, prod):
        if prod in self.bestelling:
            self.edit[prod] = - self.bestelling[prod]
            return 0
        else:
            return -1
    
    
    def bestelling_list(self):
        msg = ["{:^28}{}".format("Product", "#"), "-"*29]
        for key in self.bestelling:
            msg.append("{:<28}{}".format(key, self.bestelling[key]))
        for key in self.edit:
            msg.append("[color=#ff0000]{:<28}{}[/color]".format(key, self.edit[key]))
        return msg


    def bereken_prijs(self):
        totaal = 0
        for product in self.bestelling:
            #probleem wanneer product verwijdert wordt uit de DB!
            #prijs moet laatste vlag blijven!
            prod_prijs = self._prod.get(product, ["ERROR"])[-1]
            if prod_prijs == "ERROR":
                return prod_prijs
            totaal += prod_prijs * self.bestelling[product]
        #TODO: live prijs update
        
        return round(totaal, 2)

            





            