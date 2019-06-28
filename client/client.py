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



kivy.require("1.10.1") #vw voor de versie

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
            verbind met de server en start een client, deze zorgt voor de 
            communicatie met de server
        '''
        pass

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


class KassaClientApp(App):
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
    
    
def show_error(message):
    KassaClientApp.info_pagina.change_info(message)
    KassaClientApp.screen_manager.current = 'info'
    Clock.schedule_once(sys.exit, 10)

if __name__ == "__main__":
    m_app = KassaClientApp()
    m_app.run()
