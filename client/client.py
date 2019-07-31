import os
import sys

#algemeen
import kivy
from kivy.app import App
from kivy.clock import Clock
#core
from kivy.core.window import Window
#achtergrond
from kivy.graphics import Color, Rectangle
#uix elementen
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

#networking
import socket_client


kivy.require("1.10.1") #vw voor de versie

DATA = None#Client_storage()
COLOURS = {} #type:color_tuple 

DEBUG = False
#ToDo: aanpasbaar door de gebruiker
COLS = 2
ROWS = 4

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        self.cols = 2
        
        if os.path.isfile("credentials.txt"):
            with open("credentials.txt", "r") as f:
                ip, poort, naam = f.read().strip().split(',')
        else:
            ip = ""
            poort = ""
            naam = ""
        
        
        self.add_widget(Label(text="ip:"))
        self.ip_veld = TextInput(text=ip, multiline=False)
        self.add_widget(self.ip_veld)
        
        self.add_widget(Label(text="Poort:"))
        self.poort = TextInput(text=poort, multiline=False)
        self.add_widget(self.poort)
        
        self.add_widget(Label(text="Naam:"))
        self.naam = TextInput(text=naam, multiline=False)
        self.add_widget(self.naam)
        
        self.add_widget(Label(text="Wachtwoord:"))
        self.password = TextInput(multiline=False, password=True)
        self.add_widget(self.password)
        
        self.add_widget(Label())
        self.knop = Button(text="verbind")
        self.knop.bind(on_press=self.gedrukt)
        self.add_widget(self.knop)
        
    
    def gedrukt(self, instance):
        #instance:  enter of klik
        ip = self.ip_veld.text
        poort = self.poort.text
        naam = self.naam.text
        wachtwoord = self.password.text
        
        if ip != "" and poort != "" and naam != "" and wachtwoord != "":
            with open("credentials.txt", "w") as f:
                f.write(f"{ip},{poort},{naam}")
            
            m_app.info_pagina.change_info(f"{naam} probeert te verbinden met {ip}:{poort}")
            m_app.screen_manager.current = "info"
            #start de verbinding
            Clock.schedule_once(self.connect, 1)
            
        else:
            popup = Popup(title="test")
            layout = GridLayout(cols=1)
            
            layout.add_widget(Label(text="Vul alle velden in!",
                                    height=Window.size[1]*.8,
                                    size_hint_y=None,
                                    font_size=30))
            
            knop = Button(text="sluit",width=Window.size[0]*.75)
            knop.bind(on_press=popup.dismiss)
            layout.add_widget(knop)
            
            popup.add_widget(layout)                        
            popup.open()
        
        
    def connect(self, dt):
        '''
            verbind met de server en start een client(?), deze zorgt voor de 
            communicatie met de server
        '''
        ip = self.ip_veld.text
        poort = int(self.poort.text)
        naam = self.naam.text
        wachtwoord = self.password.text
        
        
        if not socket_client.connect(ip, poort, naam, wachtwoord, show_error):
            #connection failed
            return
        
        #maak de product page en sla alle data op in de datastructuur
        req = {'req':'GET'}
        DATA.set_prod(socket_client.requestData(req))
        
        DATA.set_verkoper(naam)
        #maak productpage
        print("switch...")
        m_app.make_prod_page()
        m_app.make_connect_pages()
        
        m_app.screen_manager.current = "klantinfo"


#https://pythonprogramming.net/screen-manager-pages-screens-kivy-application-python-tutorial/
class InfoScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 1
        
        self.label = Label(halign="center", valign="middle", font_size=30)
        
        self.label.bind(width=self.update_text_width)
        
        self.add_widget(self.label)
        
    
    def change_info(self, info):
        self.label.text = info
    
    def update_text_width(self, *_):
        self.label.text_size = (self.label.width * .9, None)
        
        
class KlantInfoScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        self.add_widget(Label(text="Info van de klant."))
        
        self.add_widget(Label(text="Verkoper: "))
        self.verkoper = TextInput(text=DATA.get_verkoper())
        self.add_widget(self.verkoper)
        
        self.add_widget(Label(text="ID:"))
        self.ID = TextInput(input_type='number')
        self.add_widget(self.ID)
        
        self.add_widget(Label(text="Tafelnummer:"))
        self.tafel = TextInput(input_type='number') 
        self.add_widget(self.tafel)
        
        self.add_widget(Label(text="Naam:"))
        self.naam = TextInput()
        self.add_widget(self.naam)
        
        knop = Button(text="Ga verder")
        knop.bind(on_press=self.start_bestelling)
        self.add_widget(knop)
        
    
    def start_bestelling(self, _):
        verkoper = self.verkoper.text.strip()
        ID = self.ID.text.strip()
        naam = self.naam.text.strip()
        tafel = self.tafel.text.strip()
        
        #TODO popups wanneer
        DATA.set_creds(naam, ID, tafel, verkoper)
        
        #restore de velden
        self.ID.text = ""
        self.naam.text = ""
        self.tafel.text = ""
        
        m_app.screen_manager.current = "product"
        
        

class HuidigeBestellingScreen(GridLayout):
    '''
        geeft weer wat er al besteld is
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        #verzend knop, stuurt je terug naar nieuwe rekening
        knop = Button(text="Send", size_hint_y=None, height=50,
                      background_color=(0,1,0,1))
        knop.bind(on_press=self.send_bestelling)
        self.add_widget(knop)        
        
        #voeg opmerking toe
        knop = Button(text="Opmerkingen", size_hint_y=None, height=50)
        #knop.bind(on_press=)
        self.add_widget(knop)
                
        #knop terug
        knop = Button(text="ga terug", size_hint_y=None, height=50,
                      background_color=(0,0.2,0.8,1))
        knop.bind(on_press=self.terug)
        self.add_widget(knop)
        
        
        #order
        self.bestelling = LijstLabel()
        self.add_widget(self.bestelling)
        
        
    def send_bestelling(self, _):
        socket_client.sendData({'req':'BST', 'bestelling':DATA.get_bestelling()})
        m_app.screen_manager.current = "klantinfo"
    
    
    def terug(self, _):
        m_app.screen_manager.current = "product"
        
        
class ProductScreen(GridLayout):
    '''
        knoppen
        knop ('<', '>') en in het midden textinput voor aantal
        label met paginanr
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        
        self.paginaNr = 0
        self.prods = []
        self.prods_knoppen = []
        
        #paginaNr:
        self.paginaNr_label = Label(
                text=f"Pagina {self.paginaNr+1}",
                size_hint_y=None,
                height=35)
        self.add_widget(self.paginaNr_label)
        
        #knopjes
        self.knopLayout = GridLayout(cols=COLS)
        for _ in range(COLS*ROWS):
            self.prods_knoppen.append(Button(text=""))
            self.prods_knoppen[-1].bind(on_press=self.klik)
            self.knopLayout.add_widget(self.prods_knoppen[-1])
        
        knop = Button(text="<-")
        knop.bind(on_press=self.switch_page)
        self.knopLayout.add_widget(knop)
        
        knop = Button(text="->")
        knop.bind(on_press=self.switch_page)
        self.knopLayout.add_widget(knop)
        
        self.add_widget(self.knopLayout)
        
        knop = Button(
                text="Huidige bestelling...",
                background_color=(0,1,0,1),
                size_hint_y=0.15)
        knop.bind(on_press=self.zie_huidig)
        self.add_widget(knop)
            
        self.vul_in()          
        
        
    def zie_huidig(self, _):
        m_app.screen_manager.current = "bestelling"
            
        
    def klik(self, instance):
        if instance.text != "":
            DATA.bestelling_add_prod(instance.text, 1)
            #temp
            m_app.bestelling_pagina.bestelling.verklein_bestelling() #volledig weg
            self.update_list = DATA.bestelling_list()
            Clock.schedule_once(self.refill, 0.5)
            #message = "{:<28}1".format(instance.text.strip())
    

    def switch_page(self, instance):
        vorig = self.paginaNr
        if instance.text == "->":
            self.paginaNr += 1 if (self.paginaNr+1<DATA.get_num_pages()) else 0
        else:
            self.paginaNr -= 1 if (self.paginaNr>0) else 0
        
        #controles nodig
        #kan beter met een return waarde gebeuren !
        if vorig != self.paginaNr:
            #pas de producten aan
            self.vul_in()
            #pas paginaNrlabel aan
            self.paginaNr_label.text = f"Pagina {self.paginaNr+1}"
        
        
    def vul_in(self):
        data = DATA.get_sort_prod()
        if len(data)<self.paginaNr*COLS*ROWS:
            end = len(data)
        else:
            end = COLS*ROWS*(self.paginaNr+1)
        data = data[COLS*ROWS*self.paginaNr:end]
        for i in range(COLS*ROWS):
            try:
                print(data[i])
                self.prods_knoppen[i].text = data[i][1]
            except:
                self.prods_knoppen[i].text = ""
    
    
    def refill(self, *_):
        if len(self.update_list):
            m_app.bestelling_pagina.bestelling.update_bestelling(self.update_list.pop(0))
            Clock.schedule_once(self.refill,0.01)
                

class KassaClientApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.prod_pages = []
        
    
    def build(self):
        self.screen_manager = ScreenManager(transition=FadeTransition())
        
        self.login_pagina = LoginScreen()
        scherm = Screen(name='login')
        scherm.add_widget(self.login_pagina)
        self.screen_manager.add_widget(scherm)
        
        self.info_pagina = InfoScreen()
        scherm = Screen(name='info')
        scherm.add_widget(self.info_pagina)
        self.screen_manager.add_widget(scherm)
        
        return self.screen_manager

    
    def make_connect_pages(self):
        #login
        self.klant_info_pagina = KlantInfoScreen()
        scherm = Screen(name="klantinfo")
        scherm.add_widget(self.klant_info_pagina)
        self.screen_manager.add_widget(scherm)
        
        #huidige bestelling
        self.bestelling_pagina = HuidigeBestellingScreen()
        scherm = Screen(name="bestelling")
        scherm.add_widget(self.bestelling_pagina)
        self.screen_manager.add_widget(scherm)
        
    
    def make_prod_page(self):
        self.prod_pagina = ProductScreen()
        scherm = Screen(name="product")
        scherm.add_widget(self.prod_pagina)
        self.screen_manager.add_widget(scherm)
    
    
    def delete_prod_pages(self):
        pass
    
    
    def goHome(self, *_):
        self.screen_manager.current = "login"


#datastructuur voor alle info
class Client_storage():
    def __init__(self):
        self._prod = {}
        self._prod_list = []
        self.verkoper = ""
        
        #bevat alle info voor de server en de kassa
        self.bestelling = {} 
    
    #setters
    def set_prod(self, prod):
        self._prod = prod
        for type in self._prod:
            for prod in self._prod[type]:
                self._prod_list.append((type, prod))
        
    
    def set_verkoper(self, verkoper):
        self.verkoper = verkoper
    
    
    def set_creds(self, naam, id, tafelnr, verkoper):
        if verkoper != self.verkoper:
            self.verkoper = verkoper
        self.bestelling.clear() #maak alles leeg
        self.bestelling["info"] = {"naam":naam, "id":id, "tafel":tafelnr, "verkoper":verkoper}
        self.bestelling["opm"] = []
            
        
    #getters
    def get_bestelling(self):
        return self.bestelling
    
    
    def get_prod(self):
        return self._prod_list
    
    
    def get_sort_prod(self):
        return sorted(self._prod_list, key=lambda el: el[1])
        
    
    def get_verkoper(self):
        return self.verkoper
    
    
    def check_prod(self, prod):
        return prod == self._prod
 
    def get_num_pages(self):
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
            
        if opm:
            self.bestelling["opm"].append(opm)
            
        print("[BESTELLING] %s" %(self.bestelling))
    
    def bestelling_list(self):
        msg = []
        for key in self.bestelling:
            if key == "opm" or key == "info":
                continue
            msg.append("{:<28}{}".format(key, self.bestelling[key]))
        return msg
            
        
        
#scrolllabel
class LijstLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #witte achtergrond

        with self.canvas.before:
            #rgba
            Color(220/255, 220/255, 230/255, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        #Scrollview attributen
        self.bar_width = 5
        
        self.layout = GridLayout(size_hint_y=None, cols=1)
        self.add_widget(self.layout)

        self.bestelling = Label(
                text="\n", markup=True,
                size_hint_y=None,
                color=(0,0,0,1),
                font_name="RobotoMono-Regular") #noodzakelijk voor spacing
        #oproepen via een andere functie/later is enige opl, op een zeer kleininterval
        #een andere optie is om het te samen te doen en eerste de volledigetekste te maken
        self.layout.add_widget(self.bestelling)
            
    
    # Methos called externally to add new message to the chat history  
    def update_bestelling(self, lijn):
        #we kunnen geen nieuw label maken, dit zal voor problemen zorgen
        #ook kunnen we update_chat_history pas oproepen als het scherm getekent wordt

        #voeg bericht toe
        self.bestelling.text += lijn + '\n'
        
        # Set layout height to whatever height of self.naam text is + 15 pixels
        # (adds a bit of space at the bottom)
        # Set chat history label to whatever height of chat history text is
        # Set width of chat history text to 98 of the label width (adds small margins)
        self.layout.height = self.bestelling.texture_size[1] + 15
        self.bestelling.height = self.bestelling.texture_size[1]
            #el.text_size = (el.width * 0.98, None) #kan later problemen geven
    
    def verklein_bestelling(self, aantal=-1, _=None):
        if (aantal == -1):
            aantal = self.bestelling.text.count('\n')
        self.bestelling.text = "".join([i+'\n' for i in self.bestelling.text.split('\n')][:-aantal])

        self.layout.height = self.bestelling.texture_size[1] - 15*aantal
        self.bestelling.height = self.bestelling.texture_size[1]
                    
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    
    
def show_error(message):    
    m_app.info_pagina.change_info(message)
    m_app.screen_manager.current = 'info'
    if DEBUG:
        Clock.schedule_once(sys.exit, 5)
    else:
        Clock.schedule_once(m_app.goHome, 5)
    socket_client.disconnect()


if __name__ == "__main__":
    DATA = Client_storage()
    m_app = KassaClientApp()
    m_app.run()
    