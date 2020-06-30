# -*- coding: utf-8 -*-
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def to_dict(type, naam, prijs, zicht, parse):
    return {'naam':naam, 'type':type, 'prijs':prijs, 'zichtbaar':zicht, 'parser':parse}


def sort_by_type(data):
    #recht van db (type, naam)
    d = {"_parser":{}}
    for type, naam, parse, basis in data:
        if parse and basis:
            if not("basis" in d["_parser"]):
                d["_parser"]["basis"] = [(type, naam)]
            else:
                d["_parser"]["basis"].append((type, naam))
        elif parse:
            if not("extra" in d["_parser"]):
                d["_parser"]["extra"] = [(type, naam)]
            else:
                d["_parser"]["extra"].append((type, naam))
        elif not(type in d):
            d[type] = [naam]
        else:
            d[type].append(naam)
    return d


def print_dict(d):
    msg = []
    for key in d:
        msg.append("{:<28}{:>2}".format(key, d[key]))
    return ["{:^28}##".format("Product"), "-"*32] + sorted(msg)


#datastructuur voor alle info
#gebruikt in client maar aangepast
class Client_storage():
    _err = "ERROR"
    def __init__(self):
        self._prod = {} #{ prod:(type, prod, prijs)}
        self._prod_list = []
        
        #bevat alle info voor de server en de kassa
        self.bestelling = {} #{prod:aantal}
        self.edit = {}
        self.edit_order = {} # +-= self.edit maar incl types
        self.info = {}#ID, prijs, 
        
        self.parserDATA = ParserStorage(self)
        self.parserPrijs = ParserPrijs()
        
        self.product_set = False
        

    #setters
    #TODO: -------------- 1 functie -----------------
    def set_prod(self, prod):
        '''
            prod is lijst bestaande uit [(type, naam, prijs)]
        '''
        for type, naam, prijs in prod:
            self._prod[naam] = (type, naam, prijs)
        self._prod_list = prod
        self.product_set = True 

    
    def set_prod_parse(self, prod):
        '''
            prod<lijst> = [(type, naam, prijs, p_basis)]
        '''
        for _type, naam, prijs, p_basis in prod:
            if p_basis:
                self.parserDATA.add_basis(_type, naam)
                self.parserPrijs.add_basis(naam, prijs)
            else:
                self.parserDATA.add_extra(_type, naam)
                self.parserPrijs.add_extra(naam, prijs)
        
        self.product_set = True 
    
    #-------------------------------------------------
    
    def is_prod_set(self):
        return self.product_set
    
    
    def prod_reset(self):
        self.product_set = False
        self._prod.clear()
        self._prod_list.clear()
        self.parserDATA.clear()
        self.parserPrijs.clear()
        
    
    def set_prod_list(self, prod):
        self._prod_list = prod            
    
    
    def set_bestelling(self, bestelling):
        #print("[BST] nieuwe bestelling:",bestelling)
        self.bestelling = bestelling
        #set order // selecteer enkel parse producten
        self.parserDATA.set_order({naam:bestelling[naam] for naam in bestelling if (naam not in self._prod)})
        
    
    def set_info(self, info):
        self.info = info
        
        
    #getters
    def get_bestelling(self):
        return self.bestelling

    
    def get_rekening(self):
        ret = {}
        for key in self.bestelling:
            if key in self._prod:
                ret[key] = self.bestelling[key]
            else:
                ret[self.parserDATA.long(key)] = self.bestelling[key]
        return ret
    
    
    def get_prod(self):
        return self._prod_list
    
    
    def get_edit(self):
        return self.edit
    
    
    def get_edit_order(self):
        return self.edit_order
    
    
    #def get_sort_prod(self):
    #    return sorted(self._prod_list, key=lambda el: el[1])
    
    #def get_opm(self):
    #    return self.bestelling["opm"]
    
 
    def get_num_pages(self, COLS, ROWS):
        geh, rest = divmod(len(self._prod_list), COLS*ROWS)
        return geh if (rest==0) else (geh + 1)
    
    
    def get_info(self):
        return self.info
    
    
    def get_info_ticket(self):
        p_art = {prod: self._prod[prod][2]/100 for prod in self._prod} #{prod: prijs} #mss de /100 weglaten
        long_parse_dict = self.parserPrijs.get_prijs_long()
        p_art.update({prod: long_parse_dict[prod]/100 for prod in long_parse_dict})
        return (self.info, p_art)
    
    
    def get_parser(self):
        return self.parserDATA
    
    
    #bestelling
    def edit_reset(self):
        self.edit = {}
        self.edit_order = {}
        
        self.parserDATA.edit_reset()
    
    
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
        prod_type = self._prod[prod][0]
        if not(prod_type in self.edit_order):
            self.edit_order[prod_type] = {}
        if (aantal < 0):
            if self.edit.get(prod, 0) + self.bestelling.get(prod, 0) + aantal < 0:
                return -1
            else:
                self.edit[prod] = self.edit.get(prod, 0) + aantal
                self.edit_order[prod_type][prod] = self.edit[prod]
                return 0
        else:
            self.edit[prod] = self.edit.get(prod, 0) + aantal
            self.edit_order[prod_type][prod] = self.edit[prod]
            return 0
        
        
    def bestelling_del_prod(self, prod):
        if prod in self.bestelling:
            prod_type = self._prod[prod][0]
            if not(prod_type in self.edit_order):
                self.edit_order[prod_type] = {}
                
            self.edit[prod] = - self.bestelling[prod]
            self.edit_order[prod_type][prod] = self.edit[prod]
            return 0
        else:
            return -1
    
    
    def bestelling_list(self):
        msg = ["{:^28}{:>2}".format("Product", "#"), "-"*32]
        for key in self.bestelling:
            msg.append("{:<28}{:>2}".format(key, self.bestelling[key]))
        for key in self.edit:
            msg.append("[color=#ff0000]{:<28}{:>2}[/color]".format(key, self.edit[key]))
        return msg


    def bereken_prijs(self):
        prijs = self.bereken_prijs_raw()
        return prijs/100 if (prijs != self._err) else prijs
    
    
    def bereken_prijs_raw(self):
        totaal = 0
        #print(self._prod)
        for product in self.bestelling:
            #probleem wanneer product verwijdert wordt uit de DB!
            #prijs moet laatste vlag blijven!
            if product in self._prod:
                totaal += self._prod[product][-1] * self.bestelling[product]
            else:
                ret = self.parserPrijs.get_prijs(product)
                if ret == self._err:
                    return self._err
                totaal += ret * self.bestelling[product]
        return totaal


#analoog als bij client maar kleine aanpassingen
class ParserStorage(object):
    def __init__(self, DATA):
        """
        bevat een lijst met:
            basisproducten (W/Z)
            extra's (br/gr)
        houdt alles bij in een lijst
        gebruikt str methode om het te printen ?
        """
        self.parent = DATA
        
        self._basis = [] #[(type, naam), (type, naam)]
        self._extra = [] #[(type, naam), (type, naam)]
        self._extra_shortLong = {}
        #self._extra_short = []
        self.order = {}  #{"WW gr":1, ...}
        self.edit = {}
        
        self.current = ["",""] #lijst van 2, [basis, extra]
        self.current_type = []
        
    
    def set_order(self, order):
        self.order = order


    def get_basis(self):
        return self._basis
    
    
    def get_extra(self):
        return self._extra
    
    
    def get_extra_short(self):
        return [(i, j[:2]) for i,j in self._extra]

    
    def add_basis(self, _type, naam):
        self._basis.append((_type, naam))
    
    
    def add_extra(self, _type, naam):
        self._extra.append((_type, naam))
        self._extra_shortLong[naam[:2]] = naam

        
    def current_basis_add(self, t, n):
        self.current[0] = "".join(sorted(self.current[0] + n))
        if not(t in self.current_type):
            self.current_type.append(t)


    def current_extra_add(self, t, n):
        ext = self.current[1].strip().split(' ')
        if n in ext:
            return
        ext.append(n)
        
        new_ext = ""
        for i in sorted(ext):
            new_ext += i + ' '
        self.current[1] = new_ext.strip()
        
        if not(n in self.current_type):
            self.current_type.append(t)
        

    def current_basis(self, basis):
        self.current[0] = basis
    
    
    def current_extra(self, extra):
        new = ""
        for t, n in extra:
            if not(n in self.current_type):
                self.current_type.append(t)
            new+= n + " "
        self.current[1] = new.strip()
        
    
    def current_delete(self):
        self.current = ["",""]
        self.current_type.clear()
        
    
    def current_empty(self):
        return len(self.current[0].strip()) == 0
        
    
    def set_current(self, new):
        self.current = new
    
    
    def get_current(self):
        return "{} {}".format(*self.current)
    
    
    def get_current_raw(self):
        return self.current
    
    
    def add_order(self, mode):
        '''
            {1:+, -1:-, 0:del}
        '''
        cu = self.get_current().strip()
        if mode == 1:
            self.edit[cu] = self.edit.get(cu,0) + 1
            return 0
        elif mode == 0:
            if cu in self.order:
                self.edit[cu] = -self.order[cu]
                return 0
            elif cu in self.edit:
                del self.edit[cu]
                return 0
            else:
                return -1
        elif mode == -1:
            if self.edit.get(cu, 0) -1 + self.order.get(cu, 0) >= 0:
                self.edit[cu] = self.edit.get(cu, 0) - 1
                return 0
            else:
                return -1

    
    def get_order(self):
        #TODO: include types indien nodig!
        return self.order
    
    
    def get_num_pages(self, num):
        geh, rest = divmod(len(self._basis), num)
        return geh if (rest==0) else (geh + 1)
    
    
    def bestelling_list(self):
        msg = ["{:^28}{:>2}".format("Product", "#"), "-"*32]
        for k in self.order:
            msg.append("{:<28} {:>2}".format(k, self.order[k]))
        for key in self.edit:
            msg.append("[color=#ff0000]{:<28} {:>2}[/color]".format(key, self.edit[key]))
        return msg
       
    
    def is_empty(self):
        return len(self.order) == 0
    
    
    def dump(self):
        return self.order
    
    
    def save_edit(self):
        for i in self.edit:
            self.order[i] = self.order.get(i, 0) + self.edit[i]
            self.parent.bestelling[i] = self.order.get(i, 0) + self.edit[i]
               
        self.parent.edit = self.edit.copy()
        #TODO echte types
        self.parent.edit_order = {"parser":self.parent.edit} 
        self.edit.clear()
        
        
    def load_order(self, order):
        self.order = order
        
    
    def reset(self):
        self.order.clear()
        self.current_type.clear()
        self.current = ["",""]
        
    
    def edit_reset(self):
        self.edit.clear()
        self.current_type.clear()
        self.current = ["", ""]
        
    
    def clear(self):
        self._basis.clear()
        self._extra.clear()
        self._extra_shortLong.clear()
        
    
    def long(self, prod):
        prodnaam = prod.strip().split(' ')
        if len(prodnaam) == 1:
            return prod
        else:
            naam = prodnaam[0] + ' '
            for p in prodnaam[1:]:
                naam += self._extra_shortLong.get(p, p) + " "
            return naam.strip()


class ParserPrijs(object):
    _err = "ERROR"
    def __init__(self):
        self._prod = []

        self.prijs_basis = {}
        self.prijs_extra = {}
        self.prijs_extra_short = {}
        
        self._extra_shortLong = {}
          
        self.prijs = {}
        self.prijs_long = {}
        
    
    def add_basis(self, _naam, _prijs):
        self.prijs_basis[_naam] = _prijs
    
    
    def add_extra(self, _naam, _prijs):
        self.prijs_extra[_naam] = _prijs
        self.prijs_extra_short[_naam[:2]] = _prijs
        #voor rekening
        self._extra_shortLong[_naam[:2]] = _naam
        
        
    def get_prijs(self, product):
        if product in self.prijs:
            return self.prijs[product]
        plijst = product.strip().split(' ')
        if len(plijst) == 1:
            prijs = self._prijs_basis(plijst[0])
            self.prijs_long[product] = prijs
        else:
            prijs = self._prijs_basis(plijst[0])
            if prijs == self._err:
                return self._err
            else:
                exprijs = self._prijs_extra(*plijst[1:])
                if exprijs == self._err:
                    return self._err
                prijs += exprijs
                self.prijs_long[self.longExtra(product)] = prijs
                
                
        self.prijs[product] = prijs
        return prijs

    
    def get_prijs_long(self):
        return self.prijs_long
        
    
    def _prijs_basis(self, basis):
        """
            basis<str>
        """
        prijs = 0
        for i in basis:
            if i in self.prijs_basis:
                prijs += self.prijs_basis[i]
            else:
                return self._err
        return prijs
    
    
    def _prijs_extra(self, *args):
        prijs = 0
        for i in args:
            i = i.strip()
            if i in self.prijs_extra:
                prijs += self.prijs_extra[i]
            elif i in self.prijs_extra_short:
                prijs += self.prijs_extra_short[i]
            else:
                return "ERROR"
        return prijs
    
    
    def longExtra(self, prod):
        #gebaseerd op functie uit parserStorage
        prodnaam = prod.strip().split(' ')
        naam = prodnaam[0] + ' '
        for p in prodnaam[1:]:
            naam += self._extra_shortLong.get(p, p) + " "
        return naam.strip() #compare with [:-1]
    
    
    def clear(self):
        #opgeroepen indien er een nieuw product/edit is
        self.prijs.clear()
        self.prijs_basis.clear()
        self.prijs_extra.clear()
        self.prijs_extra_short.clear()
    

    