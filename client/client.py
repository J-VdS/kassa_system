import os
import sys
from random import randint

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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
#save/dump
from kivy.storage.jsonstore import JsonStore

#networking
import socket_client


kivy.require("1.10.1") #vw voor de versie

DATA = None #Client_storage()
COLOURS = {"drank":(0.8,0.2,0,1),
           "gerecht":(0,0.2,1,1),} #type:color_tuple 
BACKUP = "datadump.json"


#debug
from kivy.logger import LoggerHistory
DEBUG = False
#ToDo: aanpasbaar door de gebruiker
COLS = 2
ROWS = 4
FS = 37 #fontsize

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        
        self.cols = 1
        
        if os.path.isfile("credentials.txt"):
            with open("credentials.txt", "r") as f:
                ip, poort, naam = f.read().strip().split(',')
        else:
            ip = ""
            poort = ""
            naam = ""
        
        lay_top = GridLayout(
                cols=2, rows=4,
                size_hint_y = None, 
                height=0.45*Window.size[1])
        lay_top.add_widget(Label(
                text="ip:", 
                font_size = FS))
        self.ip_veld = TextInput(
                text=ip,
                multiline=False,
                font_size = FS-4)
        lay_top.add_widget(self.ip_veld)
        
        lay_top.add_widget(Label(
                text="Poort:", 
                font_size = FS))
        self.poort = TextInput(
                text=poort,
                multiline=False,
                font_size = FS-4)
        lay_top.add_widget(self.poort)
        
        lay_top.add_widget(Label(
                text="Naam:", 
                font_size = FS))
        self.naam = TextInput(
                text=naam, 
                multiline=False, 
                font_size = FS-4)
        lay_top.add_widget(self.naam)
        
#        lay_top.add_widget(Label(
#                text="Wachtwoord:", 
#                font_size = 22))
#        self.password = TextInput(
#                multiline=False, 
#                password=True, 
#                font_size = 22)
#        lay_top.add_widget(self.password)
        
        self.add_widget(lay_top)
        
        self.knop = Button(
                text="verbinden", 
                font_size=FS,
                size_hint_y = None, 
                height=0.1*Window.size[1])
        self.knop.bind(on_press=self.gedrukt)
        self.add_widget(self.knop)
        
        self.add_widget(Label(text=""))
        
    
    def gedrukt(self, instance):
        #instance:  enter of klik
        ip = self.ip_veld.text
        poort = self.poort.text
        naam = self.naam.text
        wachtwoord =  "abc" #self.password.text
        
        if ip != "" and poort != "" and naam != "" and wachtwoord != "":
            with open("credentials.txt", "w") as f:
                f.write(f"{ip},{poort},{naam}")
            
            m_app.info_pagina.change_info(f"{naam} probeert te verbinden met {ip}:{poort}")
            m_app.screen_manager.current = "info"
            #start de verbinding
            Clock.schedule_once(self.connect, 1)
            
        else:
            popup = Popup(title="Info")
            layout = GridLayout(cols=1)
            
            layout.add_widget(Label(text="Vul alle velden in!",
                                    height=Window.size[1]*.8,
                                    size_hint_y=None,
                                    font_size=FS))
            
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
        wachtwoord = "abc" #self.password.text
        
        
        if not socket_client.connect(ip, poort, naam, wachtwoord, show_error):
            #connection failed
            return
        
        #maak de product page en sla alle data op in de datastructuur
        req = {'req':'GET'}
        ret = socket_client.requestData(req)
        if ret == -1:
            return
        DATA.set_prod(ret)
        
        DATA.set_verkoper(naam)
        
        #maak productpage
        m_app.make_prod_page()
        m_app.make_connect_pages()
        
        #if there is a backup
        if os.path.isfile(BACKUP):
            #set message that there is a backup!
            m_app.info_pagina.change_info("[color=#ffff00]Er is een BACKUP[/color]\nEr ging iets mis tijdens je laatste bestelling of je verliet/sloot de applicatie. Er werd een backup gemaakt. Deze kan je gebruiken zolang je geen [color=#00abab]nieuwe[/color] bestelling start!")
            m_app.screen_manager.current = "info"
            #and change to klaninfo after x seconds
            Clock.schedule_once(self.goKlantInfo, 5)
        else: 
            m_app.screen_manager.current = "klantinfo"
        
    
    def goKlantInfo(self, _=None):
        m_app.screen_manager.current = "klantinfo"


#https://pythonprogramming.net/screen-manager-pages-screens-kivy-application-python-tutorial/
class InfoScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 1
        
        self.label = Label(halign="center", valign="middle", font_size=FS, markup=True)
        
        self.label.bind(width=self._update_text_width)
        
        self.add_widget(self.label)
        
    
    def change_info(self, info):
        self.label.text = info
    
    def _update_text_width(self, *_):
        self.label.text_size = (self.label.width * .9, None)
        
        
class KlantInfoScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.cols = 1
        
        top_info = GridLayout(cols=2, rows=1, size_hint_y=0.15)
        top_info.add_widget(Label(text="Info over de klant:", font_size=FS-2))
        knop = Button(text="BACK UP", size_hint_x=0.5, background_color=(0,0.2,1,1), background_normal='', font_size=FS-2)
        knop.bind(on_press=self.check_backup)
        top_info.add_widget(knop)
        
        self.add_widget(top_info)
        lay_top = GridLayout(cols=2, rows=4, size_hint_y=0.85)
        
        
        lay_top.add_widget(Label(text="Naam:", size_hint_x=0.75, font_size=FS))
        self.naam = TextInput(multiline=False, font_size=FS-2)
        lay_top.add_widget(self.naam)
        
        lay_top.add_widget(Label(text="ID:", size_hint_x=0.75, font_size=FS))
        self.ID = TextInput(input_type='number', multiline=False, font_size=FS-2)
        lay_top.add_widget(self.ID)
        
        lay_top.add_widget(Label(text="Tafelnummer:", size_hint_x=0.75, font_size=FS))
        self.tafel = TextInput(input_type='number', multiline=False, font_size=FS-2) 
        lay_top.add_widget(self.tafel)
        
        lay_top.add_widget(Label(text="Verkoper:", size_hint_x=0.75, font_size=FS))
        self.verkoper = TextInput(text=DATA.get_verkoper(), multiline=False, font_size=FS-2)
        lay_top.add_widget(self.verkoper)
        
        self.add_widget(lay_top)
        
        knop = Button(text="Ga verder", font_size=FS, size_hint_y=0.3)
        knop.bind(on_press=self.start_bestelling)
        self.add_widget(knop)
        
        self.add_widget(Label(text="", size_hint_y=None, height=Window.size[1]*0.45))
        
    
    def start_bestelling(self, _):
        verkoper = self.verkoper.text.strip()
        ID = self.ID.text.strip()
        naam = self.naam.text.strip()
        tafel = self.tafel.text.strip()
        
        if (ID == "")+(naam == "")+(tafel == "")+(verkoper == ""):
            self.info_popup("Vul alle velden in!")
            return
        elif not(ID.isdigit()) or not(tafel.isdigit()):
            #popup gebruik nummers
            self.info_popup("ID en tafelnummer\nmoeten getallen zijn!")
            return
        
        #reset de huidige bestelling en vul nieuwe indentificaties in
        DATA.set_creds(naam, int(ID), int(tafel), verkoper)
        #maak huidige bestelling leeg
        m_app.bestelling_pagina.bestelling.verklein_bestelling()
        #reset de knoppen met producten + labels
        m_app.prod_pagina.reset()
        
        
        #restore de velden
        self.ID.text = ""
        self.naam.text = ""
        self.tafel.text = ""
        
        m_app.screen_manager.current = "product" 
        
    
    def info_popup(self, text):
        popup = Popup(title="Info")
        layout = GridLayout(cols=1)
        
        info_label = Label(text=text,
                           height=Window.size[1]*.8,
                           size_hint_y=None,
                           font_size=30,
                           halign="center")
        info_label.bind(width=self._update_text_width)
        layout.add_widget(info_label)
        
        knop = Button(text="sluit",width=Window.size[0]*.75)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()
        
        
    def _update_text_width(self, instance, _):
        instance.text_size = (instance.width * .9, None)
    
    
    #TODO
    def check_backup(self, _):
        if not(os.path.isfile(BACKUP)):
            self.info_popup("Er is geen backup gevonden.\nJe bestelling is verzonden en aangekomen.")
            return
        #probeer de backup in te laden
        try:
            store = JsonStore(BACKUP)
            info = store.get("backup").get("info") #gebruiken voor popup met info
            data = store.get("backup").get("data")
            DATA.load_data(data)
            
        except Exception as e:
            print("JSON load error", str(e))
            self.info_popup("Er ging iets mis bij het inladen van de backup.")
            return
        
        #maak popup met info over de klant/status
        popup = Popup(title="Klantinfo")
        layout = GridLayout(cols=1)
    
        
        layout.add_widget(Label(text="ID:  {}".format(info["id"]), font_size=30))
        layout.add_widget(Label(text="Naam:  {}".format(info["naam"]), font_size=28))
        layout.add_widget(Label(text="Tafel: {}".format(info["tafel"]), font_size=30))
        layout.add_widget(Label(text="Verzonden: {}".format("Ja" if (info["verzonden"]) else "Nee"), font_size=30))
        layout.add_widget(Label(text="Bevestigd: {}".format("Ja" if (info["bevestigd"]) else "Nee"), font_size=30))
        
        info_label = Label(text="[color=#ffff00]Indien je bestelling reeds verzonden is zullen veranderingen niet worden toegelaten![/color]",
                           font_size=30,
                           markup=True)
        info_label.bind(width=self._update_text_width)
        layout.add_widget(info_label)
        
        knop = Button(text="sluit",width=Window.size[0]*.75)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()
        
        #herlaad het bestellingscherm
        m_app.prod_pagina.klik(Label(text=""), True)
        m_app.prod_pagina.reset()
        m_app.screen_manager.current = "bestelling"
        

class HuidigeBestellingScreen(GridLayout):
    '''
        geeft weer wat er al besteld is
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        #verzend knop, stuurt je terug naar nieuwe rekening
        knop = Button(text="Send", size_hint_y=0.125,
                      background_color=(0,1,0,1),
                      font_size=FS)
        knop.bind(on_press=self.send_bestelling)
        self.add_widget(knop)
        
        #verwijder bestelling
        knop = Button(text="Verwijder", size_hint_y=0.125,
                      background_color=(1,1,0,1),
                      font_size=FS)
        knop.bind(on_press=self.verwijder)
        self.add_widget(knop)
        
        #voeg opmerking toe
        knop = Button(text="Opmerkingen", size_hint_y=0.125,
                      font_size=FS)
        knop.bind(on_press=self.opmerkingen)
        self.add_widget(knop)
                
        #knop terug
        knop = Button(text="ga terug", size_hint_y=0.125,
                      background_color=(0,0.2,0.8,1),
                      font_size=FS)
        knop.bind(on_press=self.terug)
        self.add_widget(knop)
        
        
        #order
        self.bestelling = LijstLabel(size_hint_y=0.5)
        self.add_widget(self.bestelling)
        
        
    def send_bestelling(self, _):
        #TODO: popup indien de bestelling leeg is
        if DATA.is_empty() and not(DATA.has_opm()):
            popup = Popup(title="Info")
            layout = GridLayout(cols=1)
            
            info_label = Label(text="[color=#ffff00]Je bestelling is leeg![/color]\nEr wordt niets gestuurd!",
                               height=Window.size[1]*.8,
                               size_hint_y=None,
                               font_size=30,
                               halign="center",
                               markup=True)
            info_label.bind(width=self._update_text_width)
            layout.add_widget(info_label)
            
            knop = Button(text="sluit",width=Window.size[0]*.75)
            knop.bind(on_press=popup.dismiss)
            layout.add_widget(knop)
            
            popup.add_widget(layout)                        
            popup.open()
            return

        if not(DATA.get_status()[0]):
            H = "{}{}".format(DATA.get_info()['id'], randint(0,99))
            DATA.set_hash(H)
            m_app.info_pagina.change_info("Bestelling onderweg...")
            
            #bevat {"status":"ontvangen"} indien de bestelling goed is aangekomen
            ret = socket_client.requestData({'req':'BST', 'bestelling':DATA.get_bestelling(), "hash":H})
            if ret == -1:
                print("disconnect dump")
                m_app.dump_data()
                return
            
            #check of bestelling is toegekomen
            DATA.set_verzonden(True)        
        
            
        else:
            H = DATA.get_hash()
            m_app.info_pagina.change_info("Aankomst bestelling aan het controleren")
        
        m_app.screen_manager.current = "info"
        
        #send check TCP-msg
        ret = socket_client.requestData({'req':'CHK', "hash":H})
        if ret == -1:
            #TODO sla alles op, voeg een knopje toe laadt laatste bestelling terug in
            print("ERROR")
            return
        elif not("status" in ret):
            print("ERROR, geen status")
            return
        #succes
        elif ret["status"] == 1:
            m_app.info_pagina.change_info("Bestelling goed ontvangen en verwerkt.")
            Clock.schedule_once(self.goKlantinfo, 2)
            DATA.set_bevestigd(True)
            #verwijder de json file (moest die er zijn)
            if os.path.isfile(BACKUP):
                os.remove(BACKUP)
            
        #closed
        elif ret["status"] == 0:
            m_app.make_bestelling_closed()
            m_app.screen_manager.current = "closedbest"
            DATA.set_verzonden(False) #terug op false want anders krijgen we een fake bestelling!
        #onbekend
        else:
            #geef foutmelding met hash en laat ze naar de keuken en kassa gaan
            popup = Popup(title="Onbekend")
            layout = GridLayout(cols=1)
            
            info_label = Label(text="[b][color=#00ff00]Hash: {}[/color][/b]\nGa nu naar de kassa en/of naar de togen om te controleren of er een ticket met deze hash is toegekomen!".format(DATA.get_hash()),
                               height=Window.size[1]*.8,
                               size_hint_y=None,
                               font_size=30,
                               halign="center",
                               markup=True)
            info_label.bind(width=self._update_width)
            layout.add_widget(info_label)
            
            knop = Button(text="sluit",width=Window.size[0]*.75)
            knop.bind(on_press=popup.dismiss)
            layout.add_widget(knop)
            
            popup.add_widget(layout)                        
            popup.open()
            
            m_app.screen_manager.current = "klantinfo"
        
        
    def goKlantinfo(self, *_):
        m_app.screen_manager.current = "klantinfo"
        
    
    def verwijder(self, _):
        self.popup = Popup(title="Info")
        layout = GridLayout(cols=1)
        
        label = Label(text="Wil je je bestelling verwijderen?\n\nDit kan niet ongedaan worden gemaakt.",
                      height=Window.size[1]*.8,
                      size_hint_y=None,
                      font_size=30,
                      halign="center",
                      valign="middle")
        label.bind(width=self._update_text_width)
        layout.add_widget(label)
        
        knoplayout = BoxLayout(orientation="horizontal")
        
        knop = Button(text="annuleer",width=Window.size[0]*.4)
        knop.bind(on_press=self.popup.dismiss)
        knoplayout.add_widget(knop)
        
        knop = Button(text="verwijder", width=Window.size[0]*.4)
        knop.bind(on_press=self._verwijder_bevestigd)
        knoplayout.add_widget(knop)
        
        
        layout.add_widget(knoplayout)
        self.popup.add_widget(layout)                        
        self.popup.open()        
       
        
    def _update_text_width(self, obj, _):
        obj.text_size = (obj.width * .9, None)
        
    
    def _verwijder_bevestigd(self, *_):
        m_app.screen_manager.current = "klantinfo"
        self.popup.dismiss() 
    
    
    def opmerkingen(self, _):
        self.popup = Popup(title="Opmerkingen")
        layout = GridLayout(cols=1)
        
        knop = Button(text="toevoegen", width=Window.size[0]*.4, font_size=FS)
        knop.bind(on_press=self._opmerking_toevoegen)
        layout.add_widget(knop)
        
        self.opm_input = TextInput(text=DATA.get_opm(), 
                                   height=Window.size[1]*.8,
                                   size_hint_y=None,
                                   font_size=30)
        self.opm_input.bind(width=self._update_text_width)
        layout.add_widget(self.opm_input)

        self.popup.add_widget(layout)                        
        self.popup.open()        
    
    
    def _opmerking_toevoegen(self, _):
        DATA.set_opm(self.opm_input.text.strip())
        self.popup.dismiss()
        
    
    def terug(self, _):
        if not(DATA.get_status()[0]):
            m_app.screen_manager.current = "product"
        else:
            popup = Popup(title="Info")
            layout = GridLayout(cols=1)
            
            info_label = Label(text="Normaal is de bestelling al verzonden\nBewerken is niet toegelaten!",
                               height=Window.size[1]*.8,
                               size_hint_y=None,
                               font_size=30,
                               halign="center")
            info_label.bind(width=self._update_text_width)
            layout.add_widget(info_label)
            
            knop = Button(text="sluit",width=Window.size[0]*.75)
            knop.bind(on_press=popup.dismiss)
            layout.add_widget(knop)
            
            popup.add_widget(layout)                        
            popup.open()
         
        
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
        self.mode = 1
        self.mode_type = -1 #{-1: alles, 0: is eerste type in DATA.get_types()}
        
        topgrid = GridLayout(size_hint_y=0.1, cols=2, rows=1)
        #paginaNr:
        self.paginaNr_label = Label(
                text=f"Pagina {self.paginaNr+1}",
                size_hint_y=0.1,
                font_size=FS-2)
        topgrid.add_widget(self.paginaNr_label)
        
        knop = Button(text="SORT", size_hint_x=0.25, font_size=FS-2)
        knop.bind(on_press=self.type_sort)
        topgrid.add_widget(knop)
        self.add_widget(topgrid)
        
        #knopjes
        self.knopLayout = GridLayout(cols=COLS, padding=[10, 5], spacing=[15, 10])
        for _ in range(COLS*ROWS):
            self.prods_knoppen.append(Button(
                    text="", halign="center",
                    font_size=FS, markup=True,
                    background_normal = ''))
            self.prods_knoppen[-1].bind(on_press=self.klik, width=self._update_text_width)
            self.knopLayout.add_widget(self.prods_knoppen[-1])
            
        
        self.min_knop = Button(text="[b]-[/b]",
                               font_size=40, 
                               markup=True,
                               background_color = (0.5, 0.5, 0.5,1),
                               background_normal='',
                               size_hint_y=0.5)
        self.min_knop.bind(on_press=self.switch_mode)
        self.knopLayout.add_widget(self.min_knop)
        
        self.plus_knop = Button(text="[b]+[/b]",
                                font_size=40,
                                markup=True,
                                background_color=(0.8,0.8,0,1),
                                background_normal='',
                                size_hint_y=0.5)
        self.plus_knop.bind(on_press=self.switch_mode)
        self.knopLayout.add_widget(self.plus_knop)
        
        knop = Button(text="[b]<-[/b]",
                      font_size=40,
                      markup=True,
                      size_hint_y=0.5)
        knop.bind(on_press=self.switch_page)
        self.knopLayout.add_widget(knop)
        
        knop = Button(text="[b]->[/b]",
                      font_size=40,
                      markup=True,
                      size_hint_y=0.5)
        knop.bind(on_press=self.switch_page)
        self.knopLayout.add_widget(knop)
        
        self.add_widget(self.knopLayout)
        
        knop = Button(
                text="Huidige bestelling...",
                background_color=(0.1,0.7,0.3,1),
                background_normal='', #om donkere tint te vermijden
                size_hint_y=0.15,
                font_size=FS-2)
        knop.bind(on_press=self.zie_huidig)
        self.add_widget(knop)
            
        self.vul_in()          
        
        
    def zie_huidig(self, _):
        m_app.screen_manager.current = "bestelling"
        
    
    def reset(self):
        self.paginaNr = 0
        self.mode = 1 #{-1:-, 1:+}
        self.mode_type = -1 #all types
        self.paginaNr_label.text = "Pagina {}".format(self.paginaNr+1)

        self.vul_in()
        
        self.update_list = DATA.bestelling_list()
        Clock.schedule_once(self.refill, 0.5)
        
                
    def klik(self, instance, load_backup=False):
        if instance.text != "":
            DATA.bestelling_add_prod(instance.text, instance.id, self.mode)
            #temp
            m_app.bestelling_pagina.bestelling.verklein_bestelling() #volledig weg
            self.update_list = DATA.bestelling_list()
            Clock.schedule_once(self.refill, 0.5)
            #message = "{:<28}1".format(instance.text.strip())                
            self.vul_in()
        #TODO: remove or change
        elif load_backup:
            m_app.bestelling_pagina.bestelling.verklein_bestelling() #volledig weg
            self.update_list = DATA.bestelling_list()
            Clock.schedule_once(self.refill, 0.5)
            #message = "{:<28}1".format(instance.text.strip())                
            self.vul_in()

    
    def switch_mode(self, instance):
        if instance.text == "[b]+[/b]":
            self.mode = 1
            self.plus_knop.background_color = (0.8,0.8,0,1)
            self.min_knop.background_color = (0.5, 0.5, 0.5,1)
        else:
            self.mode = -1
            self.plus_knop.background_color = (0.5, 0.5, 0.5,1)
            self.min_knop.background_color = (0.8,0.8,0,1)
        
    
    def switch_page(self, instance):
        vorig = self.paginaNr
        if instance.text == "[b]->[/b]":
            self.paginaNr += 1 if (self.paginaNr+1<DATA.get_num_pages(self.mode_type)) else 0
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
        if self.mode_type == -1:
            data = DATA.get_sort_prod_aantal()
        else:
            data = DATA.get_prod_by_type_aantal(self.mode_type)
        if len(data)<self.paginaNr*COLS*ROWS:
            end = len(data)
        else:
            end = COLS*ROWS*(self.paginaNr+1)
        data = data[COLS*ROWS*self.paginaNr:end]
        
        for i, knop in enumerate(self.prods_knoppen):
            try:
                knop.text = "[b]{}[/b]".format(data[i][1])
                knop.id = data[i][0]
                knop.background_color = COLOURS.get(data[i][0], (0.5, 0.5, 0.5,1))
            except:
                knop.text = ""
                knop.background_color = (0.5, 0.5, 0.5,1)
    
    
    def refill(self, *_):
        if len(self.update_list):
            m_app.bestelling_pagina.bestelling.update_bestelling(self.update_list.pop(0))
            Clock.schedule_once(self.refill,0.01)
    

    #knoppen
    def _update_text_width(self, instance, _):
        instance.text_size = (instance.width * .9, None)
        
        
    #sorteren
    def type_sort(self, *_):
        self.tpopup = Popup(title="sorteren", width=Window.size[0]*0.4, size_hint_x=None)
        layout = GridLayout(cols=1)
        
        select_layout = GridLayout(cols=2)
        
        select_layout.add_widget(Label(text="alles", font_size=30))
        self._type_checkboxes = [CheckBox(group="select_type", size_hint_x=0.4, active=True)]
        select_layout.add_widget(self._type_checkboxes[-1])
        
        for type in DATA.get_types():
            select_layout.add_widget(Label(text=type, font_size=30))
            self._type_checkboxes.append(CheckBox(group="select_type", size_hint_x=0.4))
            select_layout.add_widget(self._type_checkboxes[-1])
        
        layout.add_widget(select_layout)
        
        
        knop = Button(text="select",width=Window.size[0]*.75, font_size=30, size_hint_y=0.25)
        knop.bind(on_press=self.type_selected)
        layout.add_widget(knop)
        
        self.tpopup.add_widget(layout)                        
        self.tpopup.open()
                
    
    def type_selected(self, *_):
        #get type
        for num, box in enumerate(self._type_checkboxes):
            if box.active:
                #de index verwijst naar het type
                self.mode_type = num - 1
                break
        #reset paginaNR
        self.paginaNr = 0
        self.paginaNr_label.text = "Pagina {}".format(self.paginaNr+1)
        self.vul_in()
        
        #close popup
        self.tpopup.dismiss()
        del self.tpopup
        


class BestellingErrorScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(
                text="Het ID klopt niet; deze rekening is reeds afgesloten.",
                font_size=FS-4,
                size_hint_y=0.2))
        
        lay_top = GridLayout(cols=2, rows=4, size_hint_y=0.85)
        
        info = DATA.get_info()
        
        lay_top.add_widget(Label(text="Naam:", size_hint_x=0.75, font_size=FS))
        self.naam = TextInput(multiline=False, font_size=FS-4, text=info["naam"])
        lay_top.add_widget(self.naam)
        
        lay_top.add_widget(Label(text="ID:", size_hint_x=0.75, font_size=FS))
        self.ID = TextInput(input_type='number', multiline=False, font_size=FS-4)
        lay_top.add_widget(self.ID)
        
        lay_top.add_widget(Label(text="Tafelnummer:", size_hint_x=0.75, font_size=FS))
        self.tafel = TextInput(input_type='number', multiline=False, font_size=FS-4, text=str(info["tafel"])) 
        lay_top.add_widget(self.tafel)
        
        lay_top.add_widget(Label(text="Verkoper:", size_hint_x=0.75, font_size=FS))
        self.verkoper = TextInput(text=DATA.get_verkoper(), multiline=False, font_size=FS-4)
        lay_top.add_widget(self.verkoper)
        
        self.add_widget(lay_top)
        
        knop = Button(text="Probeer opnieuw", font_size=FS, size_hint_y=0.3)
        knop.bind(on_press=self.resend)
        self.add_widget(knop)
        
        self.add_widget(Label(text="", size_hint_y=None, height=Window.size[1]*0.45))
        
    
    def resend(self, _):
        #check alle velden ingevuld
        verkoper = self.verkoper.text.strip()
        ID = self.ID.text.strip()
        naam = self.naam.text.strip()
        tafel = self.tafel.text.strip()
        
        if (ID == "")+(naam == "")+(tafel == "")+(verkoper == ""):
            #popup vul alle velden in
            popup = Popup(title="Info")
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
            return
        elif not(ID.isdigit()) or not(tafel.isdigit()):
            #popup gebruik nummers
            popup = Popup(title="Info")
            layout = GridLayout(cols=1)
            
            layout.add_widget(Label(text="ID en tafelnummer\nmoeten getallen zijn!",
                                    height=Window.size[1]*.8,
                                    size_hint_y=None,
                                    font_size=30))
            
            knop = Button(text="sluit",width=Window.size[0]*.75)
            knop.bind(on_press=popup.dismiss)
            layout.add_widget(knop)
            
            popup.add_widget(layout)                        
            popup.open()
            return
        
        DATA.change_creds(naam, ID, tafel, verkoper)
        
        m_app.bestelling_pagina.send_bestelling(None)
    
        
class KassaClientApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.best_closed = False
        self.connect_pages = False
        self.prod_page = False
    
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
        if self.connect_pages:
            return
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
        
        self.connect_pages = True
        
    
    def make_prod_page(self):
        if self.prod_page:
            return
        self.prod_pagina = ProductScreen()
        scherm = Screen(name="product")
        scherm.add_widget(self.prod_pagina)
        self.screen_manager.add_widget(scherm)
        
        self.prod_page = True
    
    
    def make_bestelling_closed(self):
        if not(self.best_closed):
            #bestelling closed error
            self.bestelling_closed_pagina = BestellingErrorScreen()
            scherm = Screen(name="closedbest")
            scherm.add_widget(self.bestelling_closed_pagina)
            self.screen_manager.add_widget(scherm)
            self.best_closed = True

    
    def goHome(self, *_):
        self.screen_manager.current = "login"
        
    
    #indien de applicatie per ongeluk gesloten wordt
    def on_stop(self):
        #als hij nog niet gestart is met een bestelling maar toch afsluit is dit niet nuttig!
        if not(DATA.is_started()):
            return
        
        self.dump_data()
    
    
    def on_pause(self):
        #als hij nog niet gestart is met een bestelling maar toch afsluit is dit niet nuttig!
        if not(DATA.is_started()):
            return
        
        self.dump_data()
        return True
    
    
    def dump_data(self):
        if os.path.isfile(BACKUP):
            os.remove(BACKUP)
        
        if DATA.get_status() == (True, True):
            return 
        #TODO: verwijder dit, was voor snel te scrollen
        data = DATA.dump_data()
        info = DATA.get_info()
        store = JsonStore(BACKUP)
        store.put("backup", data=data, info=info)
        store.put("viewer", url="http://jsonviewer.stack.hu/")
        

#datastructuur voor alle info
class Client_storage():
    def __init__(self):
        self._prod = {}
        self._prod_list = []
        self._prod_list_aantal = []
        self.verkoper = ""
        
        self._prod_typelist = {}
        self._prod_typelist_aantal = {}
        self.types = []
        
        #bevat alle info voor de server en de kassa
        self.bestelling = {}
        self.H = 0
        
        #info over de verzending
        self.verzonden = False
        self.bevestigd = False
        self.started = False
        
    
    #setters
    def set_prod(self, prod):
        #reset data
        self._prod = prod
        self._prod_list_aantal = []
        self._prod_list = []
        self._prod_typelist = {}
        self._prod_typelist_aantal = {}
        self.types = []

        for type in self._prod:
            self.types.append(type)
            self._prod_typelist[type] = []
            self._prod_typelist_aantal[type] = []
            for prod in self._prod[type]:
                self._prod_typelist[type].append([type, prod])
                self._prod_typelist_aantal[type].append([type, prod])
                self._prod_list.append([type, prod])
                self._prod_list_aantal.append([type, prod])
        
    
    def set_verkoper(self, verkoper):
        self.verkoper = verkoper
    
    
    def set_creds(self, naam, id, tafelnr, verkoper):
        if verkoper != self.verkoper:
            self.verkoper = verkoper
        self.bestelling.clear() #maak alles leeg
        self.bestelling["info"] = {"naam":naam, "id":id, "tafel":tafelnr, "verkoper":verkoper}
        self.bestelling["opm"] = ""
        self.bestelling["BST"] = {}
        
        #reset aantal
        self._prod_list_aantal = self._prod_list[:]
        for key in self._prod_typelist:
            self._prod_typelist_aantal[key] = self._prod_typelist[key][:]
        #self._prod_typelist_aantal = copy.deepcopy(self._prod_typelist)
        
        #status
        self.verzonden = False
        self.bevestigd = False
        self.started = True #dit zal anders key errors geven, of we slaan een nutteloze bestelling op
        
    
    def change_creds(self, naam, id, tafelnr, verkoper):
        if verkoper != self.verkoper:
            self.verkoper = verkoper
        self.bestelling["info"] = {"naam":naam, "id":id, "tafel":tafelnr, "verkoper":verkoper}


    def set_opm(self, opm):
        self.bestelling["opm"] = opm        
        
        
    def set_verzonden(self, value):
        self.verzonden = value
    
    
    def set_bevestigd(self, value):
        self.bevestigd = value
        
    
    #nodig voor dump data als je afsluit ofzo
    def set_hash(self, H):
        self.H = H
        
    
    def dump_data(self):
        return {"_prod": self._prod,            #eig niet nodig
                "_prod_list": self._prod_list,  #eig niet nodig
                "_prod_list_aantal": self._prod_list_aantal,
                "verkoper": self.verkoper,
                "_prod_typelist": self._prod_typelist, #eig niet nodig
                "_prod_typelist_aantal": self._prod_typelist_aantal,
                "types": self.types,            #eig niet nodig
                "bestelling": self.bestelling,
                "status":(self.verzonden, self.bevestigd),
                "hash": self.H
                }
    
    
    def load_data(self, data):
        #print("loaded\n", data)
        #self._prod = data["_prod"]
        #self._prod_list = data["_prod_list"]
        self._prod_list_aantal = data["_prod_list_aantal"]
        self.verkoper = data["verkoper"]
        #self._prod_typelist = data["_prod_typelist"]
        self._prod_typelist_aantal = data["_prod_typelist_aantal"]
        #self.types = data["types"]
        self.bestelling = data["bestelling"]
        self.status = data["status"]
        self.H = data["hash"]
    
        
    #getters
    def get_bestelling(self):
        keys = list(self.bestelling['BST'].keys()) #iter problem
        for _type in keys:
            if len(self.bestelling['BST'][_type]) == 0:
                del self.bestelling['BST'][_type]
        return self.bestelling
    
    
    def get_info(self):
        extra = {"verzonden":self.verzonden, "bevestigd":self.bevestigd}
        extra.update(self.bestelling["info"])
        return extra
    
    
    def get_prod(self):
        return self._prod_list
    
    
    def get_prod_by_type(self, type_index):
        _type = self.types[type_index]
        return self._prod_typelist[_type]
    
    
    def get_prod_by_type_aantal(self, type_index):
        _type = self.types[type_index]
        return sorted(self._prod_typelist_aantal[_type], key=lambda el: el[1])
    
    
    def get_sort_prod_aantal(self):
        return sorted(self._prod_list_aantal, key=lambda el: el[1])
    
    
    def get_sort_prod(self):
        return sorted(self._prod_list, key=lambda el: el[1])
        
    
    def get_types(self):
        return self.types
    
    
    def get_verkoper(self):
        return self.verkoper
    
    
    def get_opm(self):
        return self.bestelling["opm"]
    
    
    def check_prod(self, prod):
        return prod == self._prod
 
    
    def get_num_pages(self, type_index=-1):
        if type_index == -1:
            geh, rest = divmod(len(self._prod_list), COLS*ROWS)
        else:
            geh, rest = divmod(len(self.get_prod_by_type(type_index)), COLS*ROWS)
        return geh if (rest==0) else (geh + 1)
    
    
    def get_status(self):
        return (self.verzonden, self.bevestigd)
    
    
    def get_hash(self):
        return self.H
    
    
    #boolstatements
    def is_started(self):
        return self.started
    
    
    def is_empty(self):
        for _type in self.bestelling['BST']:
            if len(self.bestelling['BST'][_type]):
                return False
        return True


    def has_opm(self):
        return bool(self.get_opm().strip())
    
    #bestelling
    def bestelling_add_prod(self, prod, type, aantal):
        '''
            voegt een product toe aan de bestelling        
        '''
        if ":" in prod:
            prod = prod.split(":")[0][3:-1] #strip [b] + extra space
        else:
            prod = prod[3:-4] #strip [b] en [/b]
        
        if not(type in self.bestelling['BST']):
            if aantal < 0 :
                return
            self.bestelling['BST'][type] = {}
            self.bestelling['BST'][type][prod] = aantal  
        
        elif self.bestelling['BST'][type].get(prod, 0) + aantal >= 0:
            self.bestelling['BST'][type][prod] = self.bestelling['BST'][type].get(prod, 0) + aantal
        else:
            return
        
        if self.bestelling['BST'][type][prod]:
            self._prod_list_aantal[self._prod_list.index([type, prod])] = [type, "{} :{:>2}".format(prod, self.bestelling['BST'][type][prod])]
            self._prod_typelist_aantal[type][self._prod_typelist[type].index([type, prod])] = [type, "{}: {}".format(prod, self.bestelling['BST'][type][prod])]
        else:
            #aantal is nul dan laten we ':' weg
            self._prod_list_aantal[self._prod_list.index([type, prod])] = [type, prod]
            self._prod_typelist_aantal[type][self._prod_typelist[type].index([type, prod])] = [type, prod]
            #delete indien het aantal gelijk is aan 0
            del self.bestelling['BST'][type][prod]


    def bestelling_list(self):
        #info over de klant en de verkoper
        msg = ["ID:{:<13}T:{}".format(self.bestelling['info']['id'], self.bestelling['info']['tafel']),
               "N:{}".format(self.bestelling['info']['naam']),
               "V:{}".format(self.bestelling['info']['verkoper']),
               "*"*32]
            
        for type in self.bestelling['BST'].values():
            for key in type:
                msg.append("{:<28} {}".format(key, type[key]))
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
        #m_app.
    socket_client.disconnect()


if __name__ == "__main__":
    #DEBUG loggin
    if not(DEBUG):
        sys.stderr = open('output.txt', 'w')
        sys.stdout = sys.stderr
        print('\n'.join([str(l) for l in LoggerHistory.history]))
    
    DATA = Client_storage()
    m_app = KassaClientApp()
    m_app.run()
    