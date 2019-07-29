import os
import sys

#algemeen
import kivy
from kivy.app import App
from kivy.clock import Clock
#core
from kivy.core.window import Window
#uix elementen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout 
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

#networking
import socket_client


kivy.require("1.10.1") #vw voor de versie

DATA = None#Client_storage()

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
        m_app.make_prod_pages()
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
        self.add_widget(TextInput(text=DATA.get_verkoper()))
        self.add_widget(Label(text="ID:"))
        self.add_widget(TextInput(input_type='number'))     
        self.add_widget(Label(text="Tafelnummer:"))
        self.add_widget(TextInput(input_type='number'))   
        self.add_widget(Label(text="Naam:"))
        self.add_widget(TextInput())
        
        knop = Button(text="Ga verder")
        knop.bind(on_press=self.start_bestelling)
        self.add_widget(knop)
        
    
    def start_bestelling(self, _):
        m_app.info_pagina.change_info("start bestelling")
        m_app.screen_manager.current = "info"
    

class KassaClientApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.prod_pages = []
        
    
    def build(self):
        self.screen_manager = ScreenManager()
        
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
        self.klant_info_pagina = KlantInfoScreen()
        scherm = Screen(name="klantinfo")
        scherm.add_widget(self.klant_info_pagina)
        self.screen_manager.add_widget(scherm)
        
    
    def make_prod_pages(self):
        pass
    
    
    def delete_prod_pages(self):
        pass


class Client_storage():
    def __init__(self):
        self._prod = {}
        self._prod_list = []
        self.verkoper = ""
    
    
    def set_prod(self, prod):
        self._prod = prod
        for type in self._prod:
            for prod in self._prod[type]:
                self._prod_list.append((type, prod))
        
    
    def set_verkoper(self, verkoper):
        self.verkoper = verkoper
    
    
    def get_prod(self):
        return self._prod_list
    
    
    def get_sort_prod(self):
        return sorted(self._prod_list, key=lambda el: el[1])
        
    
    def get_verkoper(self):
        return self.verkoper
    
    
    def check_prod(self, prod):
        return prod == self._prod
        
    
def show_error(message):
    m_app.info_pagina.change_info(message)
    m_app.screen_manager.current = 'info'
    Clock.schedule_once(sys.exit, 5)

if __name__ == "__main__":
    DATA = Client_storage()
    m_app = KassaClientApp()
    m_app.run()
    DATA.set_prod({1:['k', 'b','x'], 3:['a','c'], 4:['t']})
    print(DATA.get_prod())
    print(DATA.get_sort_prod())
    