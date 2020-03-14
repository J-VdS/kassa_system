import threading
import os
import pickle
import datetime
from functools import partial #instead of lamda functions
from collections import deque

#kivy
import kivy
from kivy.app import App
#achtergrond
from kivy.graphics import Color, Rectangle

#uix
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition#, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
#fileviewer
from kivy.uix.filechooser import FileChooserListView


from kivy.core.window import Window
from kivy.clock import Clock

#zelfgeschreven
import socket_server
import database
import global_vars
import func

kivy.require("1.10.1")

'''
#logging
import sys
sys.stderr = open('output.txt', 'w')
sys.stdout = sys.stderr

from kivy.logger import LoggerHistory
print('\n'.join([str(l) for l in LoggerHistory.history]))
'''
'''
def __init__(self, *):
    #achtergrondkleur
        with self.canvas.before:
            #rgba
            Color(1, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

def _update_rect(self, instance, value):
        
        self.rect.pos = instance.pos
        self.rect.size = instance.size


'''
#schermen
class HoofdScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3
        
        #navigatiebar
        self.navbar = NavigatieBar()
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.hoofdbar = HoofdBar()
        self.add_widget(self.hoofdbar)
        
        #lable
        self.add_widget(Label(size_hint_y=0.1))
        
        
class ProductScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 3

        #navigatiebar
        self.navbar = NavigatieBar(huidig="product")
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.productbar = ProductBar()
        self.add_widget(self.productbar)
        
        #producten, scrollable label --> zal mss een layout moeten worden
        self.history = ProductLijstLabel(height=Window.size[1]*0.5, size_hint_y=None)
        self.add_widget(self.history)
        
        
        self.productbar.set_lijst_bar(self.history)
        
        
class ConnectScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        #navigatiebar
        self.navbar = NavigatieBar(huidig="connect")
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.connectbar = ConnectBar(size_hint_y=0.5)
        self.add_widget(self.connectbar)
        
        self.printer_bar = PrinterBar()
        self.add_widget(self.printer_bar)
        
        #leeglabel
        #self.add_widget(Label(size_hint_y=None, height=25))
        knop = Button(text="Alle printers afsluiten...", size_hint_y=None, height=30)
        knop.bind(on_press=self.kill_printers)
        self.add_widget(knop)
        
    
    def kill_printers(self, _=None):
        socket_server.sluit_printers()        
        
        
class BestelScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        #navigatiebar
        self.navbar = NavigatieBar(huidig=None)
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.bestelbar = BestelBar()
        self.add_widget(self.bestelbar)
        
        #lijstlabel links, midden al de knoppen met de producten en rechts speciale actie knoppen
        #interface voor aantal te wijzigen of te verwijderen
        
        
class StatsScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        #navigatiescherm
        self.navbar = NavigatieBar(huidig="stats")
        self.add_widget(self.navbar)
        
        #statistieken
        self.statbar = StatistiekBar()
        self.add_widget(self.statbar)
        
        #leeglabel
        #self.add_widget(Label(text=""))
        

class OptieScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=1
        
        self.navbar = NavigatieBar(huidig="setting")
        self.add_widget(self.navbar)
        self.add_widget(Label(text="scherm1"))
        

class BListScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        
        self.navbar = NavigatieBar(huidig="blist")
        self.add_widget(self.navbar)
        
        self.blist = BListBar()
        self.add_widget(self.blist)
        
    
    def save_log(self):
        self.blist.save_log()
    
    
    def add(self, info, statcolor=None):
        self.blist.update_list(info, statcolor)
        
        
#bars
class NavigatieBar(BoxLayout):
    def __init__(self, huidig="hoofd", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 5
        self.size_hint_y = None
        self.height = 75
        self.padding = [10, 10] #padding horiz, padding width
        
        home_knop = Button(
                text="HOME",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "hoofd") else (1,1,1,1)
                )
        home_knop.bind(on_press=self.switch)
        self.add_widget(home_knop)
        
        product_knop = Button(
                text="PRODUCTEN",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "product") else (1,1,1,1)
                )
        product_knop.bind(on_press=self.switch)
        self.add_widget(product_knop)
        
        connect_knop = Button(
                text="CONNECTIES",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "connect") else (1,1,1,1)
               )
        connect_knop.bind(on_press=self.switch)
        self.add_widget(connect_knop)
        
        connect_knop = Button(
                text="STATISTIEKEN",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "stats") else (1,1,1,1)
               )
        connect_knop.bind(on_press=self.switch)
        self.add_widget(connect_knop)
        
        bestellings_knop = Button(
                text="BESTELLINGEN",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "blist") else (1,1,1,1)
                )
        bestellings_knop.bind(on_press=self.switch)
        self.add_widget(bestellings_knop)
        
#        settings_knop = Button(
#                text="SETTINGS",
#                font_size=20,
#                background_color = (1,0,0,1) if (huidig == "setting") else (1,1,1,1)
#                )
#        settings_knop.bind(on_press=self.switch)
#        self.add_widget(settings_knop)
        
        
    def switch(self, instance):
        if gui.screen_manager.has_screen(instance.text):
            gui.screen_manager.current = instance.text
        else:
            gui.screen_manager.current = "HOME"
        
        
class HoofdBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        
        #eerste rij
        self.add_widget(Label(
                text="Actieve rekeningen:",
                size_hint_y=0.2,
                font_size=20))
        
        #tweede rij
        self.paginaNr = 0
        self.pagina_label = Label(
                text="Pagina 1",
                size_hint_y=None,
                height=35,
                font_size=16)
        self.add_widget(self.pagina_label)
        
        #derde rij
        self.buttons = []
        self.button_grid = GridLayout(
                spacing=[10,15],
                cols=global_vars.kassa_cols,
                rows=global_vars.kassa_rows)
        aantal_knoppen = global_vars.kassa_cols * global_vars.kassa_rows
        for i in range(aantal_knoppen):
            if i == (aantal_knoppen - global_vars.kassa_cols):
                knop = Button(text="<-", font_size=25, background_color=(0,1,0,1))
                knop.bind(on_press=self.switch_pagina)
                self.button_grid.add_widget(knop)
            elif i == (aantal_knoppen - 2):
                knop = Button(text="NIEUW...", font_size=25, background_color=(1,1,0,1))
                knop.bind(on_press=self.nieuw)
                self.button_grid.add_widget(knop)
            elif i == (aantal_knoppen - 1):
                knop = Button(text="->", font_size=25, background_color=(0,1,0,1))
                knop.bind(on_press=self.switch_pagina)
                self.button_grid.add_widget(knop)
            else:
                self.buttons.append(Button(text='', font_size=20))
                self.buttons[-1].bind(on_press=self.switch_rekening)
                self.button_grid.add_widget(self.buttons[-1])
                
        self.add_widget(self.button_grid)
        
        #db_io
        self.db_io = database.OpenIO(global_vars.db)
        
        #Clock.schedule_interval(self.update_rekeningen, 30)
        self.update_rekeningen(self.db_io)
    
    
    def switch_rekening(self, instance):
        if instance.text != "":
            bestelling = database.getBestelling(self.db_io, int(instance.text))
            if bestelling == -1:
                #TODO popup
                self.update_rekeningen(self.db_io)
                return
            
            #TODO vermijd de update elke keer
            gui.DATA.set_bestelling(bestelling)
            gui.DATA.set_info({"ID":int(instance.text)})
            gui.rekeningscherm.bestelbar.set_ID(instance.text)
            gui.DATA.set_prod(database.getAllProductKassa(self.db_io))
            
            gui.rekeningscherm.bestelbar.reset()
            gui.screen_manager.current = "BESTEL"
            print("Switch rekening:", instance.text)
        
        
        
    def switch_pagina(self, instance):
        data = list(database.getIDs(self.db_io))
        aantal_knoppen = len(self.buttons)
        geh, rest = divmod(len(data), aantal_knoppen)
        paginas = geh if (rest == 0) else (geh+1)
        #verander van pagina
        if instance.text == "->":
            self.paginaNr += (self.paginaNr+1 < paginas)
        else:
            #instance.text == "<-":
            self.paginaNr -= (self.paginaNr != 0)
        
        data = data[self.paginaNr*aantal_knoppen:]
        self.update_rekeningen(data=data)
        
        self.pagina_label.text = f"Pagina {self.paginaNr+1}"
        
        
    def update_rekeningen(self, db_io=None, data=None):
        #deze functie wordt meegegeven in de serverthread
        #TODO: meerdere pagina support
        if db_io:
            data = list(database.getIDs(db_io)) #[(1,),(3,)] - lijst van tuples met 1 element

        aantal_buttons = len(self.buttons)
        
        geh, rest = divmod(len(data), aantal_buttons)
        self.num_paginas = geh if (rest==0) else (geh + 1)
        
        for nr, knop in enumerate(self.buttons):
            try:
                knop.text = str(data[nr][0])
            except:
                knop.text = ""
                
                
    def nieuw(self, *_):
        self.popup = Popup(title="Nieuwe rekening", size=(600,400), size_hint=(None,None))
        alg_layout = GridLayout(cols=1)
        layout = GridLayout(cols=2)
        
        layout.add_widget(Label(text="Naam:", font_size=20))
        self.pnaam = TextInput(multiline=False, font_size=20)
        layout.add_widget(self.pnaam)
        
        layout.add_widget(Label(text="ID:", font_size=20))
        self.pID = TextInput(input_type='number', multiline=False, font_size=20)
        layout.add_widget(self.pID)
        
        #layout.add_widget(Label(text="Tafelnummer:", font_size=20))
        #self.ptafel = TextInput(input_type='number', multiline=False, font_size=20) 
        #layout.add_widget(self.ptafel)
        
        #layout.add_widget(Label(text="Verkoper:", font_size=20))
        #self.pverkoper = TextInput(text="kassa", multiline=False, font_size=20)
        #layout.add_widget(self.pverkoper)
        
        
        knop = Button(text="annuleren", size_hint_y=None, height=40)
        knop.bind(on_press=self.popup.dismiss)
        layout.add_widget(knop)
        
        knop = Button(text="toevoegen", size_hint_y=None, height=40)
        knop.bind(on_press=self.toevoegen)
        layout.add_widget(knop)
        alg_layout.add_widget(layout)
        
        self.perror = Label(text="", markup=True, size_hint_y=0.3, font_size=20)
        alg_layout.add_widget(self.perror)
        
        self.popup.add_widget(alg_layout)                        
        self.popup.open()
        
    
    def toevoegen(self, *_):
        ID = self.pID.text.strip()
        naam = self.pnaam.text.strip()
        if (ID == "") or (naam == ""):
            self.perror.text = "[color=#ff0000]Vul alle velden in![/color]"
            return
        elif not(ID.isdigit()):
            self.perror.text = "[color=#ff0000]ID moet een getal zijn![/color]"
            return
        
        db_io = database.OpenIO(global_vars.db)
        
        ret = database.addBestellingID(db_io, ID, naam)
        
        if ret == -1:
            self.perror.text = "[color=#ff0000]ID is al in gebruik![/color]"
            database.CloseIO(db_io)
        else:
            self.update_rekeningen(db_io)
            database.CloseIO(db_io)
            
            self.popup.dismiss()
        

class ProductBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 5
        self.padding = [10, 10] #padding horiz, padding width
        
        self.add_widget(self._add_product_blok())
        self.add_widget(self._bewerk_product_blok())
        self.add_widget(self._zichtbaar_verwijder_blok())
        
        #database_interactie
        self.db_io = None #database.(global_vars.db)
        
    def set_lijst_bar(self, disp):
        self.lijst_bar = disp
    
    
    def _add_product_blok(self):
        grid = GridLayout(cols=1, spacing=[5,15])
        grid.add_widget(Label(
                text="Voeg een product toe",
                height=35,
                size_hint_y=None, #check
                font_size=20))
        label = Label(
                text="Je kan een product toevoegen door respectievelijk het type, de naam, de prijs (vb 5.7 ) en de zichtbaarheid te kiezen. Producten met dezelfde naam zijn niet toegelaten.",
                size_hint_y = None,
                height = 40,
                valign='top',
                halign='left')
        label.bind(width=self.update_text_width)
        grid.add_widget(label)
        
        info_grid = GridLayout(cols=2, spacing=[5,5])
        
        info_grid.add_widget(Label(text="type:", font_size=17))
        self.add_type = Spinner(
                text="-",
                values=("drank", "gerecht", "dessert", "divers", "pensen"),
                font_size=15,
                size_hint_y=None,
                height=30)
        info_grid.add_widget(self.add_type)
        
        info_grid.add_widget(Label(text="naam:", font_size=17))
        self.add_naam = TextInput(
                multiline=False,
                font_size=17,
                size_hint_y=None,
                height=35)
        info_grid.add_widget(self.add_naam)
        
        info_grid.add_widget(Label(text="prijs:", font_size=17))
        self.add_prijs = TextInput(
                multiline=False, 
                font_size=17,
                size_hint_y=None,
                height=35)
        info_grid.add_widget(self.add_prijs)
        
        info_grid.add_widget(Label(text="zichtbaar?",font_size=17))
        self.add_zichtbaar = Spinner(
                text="Ja",
                values=("Ja", "Enkel voor kassa", "Nee"),
                font_size=15,
                size_hint_y=None,
                height=30)
        info_grid.add_widget(self.add_zichtbaar)
        
        grid.add_widget(info_grid)
        knop = Button(text="toevoegen", font_size=20, size_hint_y=None, height=35)
        knop.bind(on_press=self._add_product)
        grid.add_widget(knop)
        
        #leeg label
        grid.add_widget(Label(size_hint_y=0.25))
        
        return grid
    
    
    def _bewerk_product_blok(self):
        grid = GridLayout(cols=1, spacing=[5,15])
        grid.add_widget(Label(
                text="Bewerk een product",
                height=35,
                size_hint_y=None, #check
                font_size=20))
        label = Label(
                text="Je kan een product bewerken door de naam van het product in te geven.Indien je de naam wil bewerken maak je best een nieuw product aan en verwijder je het andere.",
                size_hint_y = None,
                height = 40,
                valign='top',
                halign='left')
        label.bind(width=self.update_text_width)
        grid.add_widget(label)
        
        info_grid = GridLayout(cols=2, spacing=[5,5])
        
        info_grid.add_widget(Label(text="naam:", font_size=17))
        self.bewerk_naam = TextInput(
                multiline=False,
                font_size=17,
                size_hint_y=None,
                height=35)
        info_grid.add_widget(self.bewerk_naam)
        
        info_grid.add_widget(Label(text="type:", font_size=17))
        self.bewerk_type = Spinner(
                text="-",
                values=("drank", "gerecht", "dessert", "divers", "pensen"),
                font_size=15,
                size_hint_y=None,
                height=30)
        info_grid.add_widget(self.bewerk_type)
        
        info_grid.add_widget(Label(text="prijs:", font_size=17))
        self.bewerk_prijs = TextInput(
                multiline=False,
                font_size=17,
                size_hint_y=None,
                height=35)
        info_grid.add_widget(self.bewerk_prijs)
        
        info_grid.add_widget(Label(text="zichtbaar?", font_size=17))
        self.bewerk_zichtbaar = Spinner(
                text="Ja",
                values=("Ja", "Enkel voor kassa", "Nee"),
                font_size=15,
                size_hint_y=None,
                height=30)
        info_grid.add_widget(self.bewerk_zichtbaar)
        
        grid.add_widget(info_grid)
        
        knop = Button(text="aanpassen", font_size=20, size_hint_y=None, height=35)
        knop.bind(on_press=self._bewerk_product)
        grid.add_widget(knop)
        
        #leeg label
        grid.add_widget(Label(size_hint_y=0.25))
        return grid    
        
    
    def _zichtbaar_verwijder_blok(self):
        grid = GridLayout(cols=1, spacing=[5,15])
        ''' verwijderblok '''
        grid.add_widget(Label(
                text="Verwijder",
                height=35,
                size_hint_y=None, #check
                font_size=20))
        label = Label(
                text="Je kan een product enkel verwijderen via naam. [color=#ff0000]Dit kan je niet ongedaan maken.[/color]",
                size_hint_y = None,
                height = 40,
                valign='top',
                halign='left',
                markup=True)
        label.bind(width=self.update_text_width)
        grid.add_widget(label)
        verwijder_grid = GridLayout(cols=2, spacing=[5,0])
        verwijder_grid.add_widget(Label(
                text="naam:",
                font_size=17,
                size_hint_y=None,
                height=30))
        self.verwijder_naam = TextInput(
                multiline=False,
                font_size=17,
                size_hint_y=None,
                height=35)
        verwijder_grid.add_widget(self.verwijder_naam)
        
        grid.add_widget(verwijder_grid)
        
        knop = Button(text="verwijder", font_size=20, size_hint_y=None, height=35)
        knop.bind(on_press=self._verwijder_product)
        grid.add_widget(knop)

        #zichtbaarheid
        grid.add_widget(Label(
                text="Zichtbaarheid",
                height=35,
                size_hint_y=None,
                font_size=20
                ))
        zichtbaar_grid = GridLayout(cols=2, spacing=[5,5])
        zichtbaar_grid.add_widget(Label(text="naam:", font_size=17))
        self.zichtbaar_naam = TextInput(
                multiline=False, 
                font_size=17,
                size_hint_y=None,
                height=35)
        zichtbaar_grid.add_widget(self.zichtbaar_naam)
        
        zichtbaar_grid.add_widget(Label(text="zichtbaar?", font_size=17))
        self.zichtbaar_zichtbaar = Spinner(
                text="Ja",
                values=("Ja", "Enkel voor kassa", "Nee"),
                font_size=15,
                size_hint_y=None,
                height=30
                )
        zichtbaar_grid.add_widget(self.zichtbaar_zichtbaar)
        
        grid.add_widget(zichtbaar_grid)                
        
        knop = Button(text="aanpassen", font_size=20, size_hint_y=None, height=35)
        knop.bind(on_press=self._zichtbaar_product)
        grid.add_widget(knop)
        #blank space
        grid.add_widget(Label(size_hint_y=0.2))
        
        return grid   

    
    def update_text_width(self, obj, _):
        '''
            Dit is noodzakelijk voor automatische multiline
        '''
        obj.text_size = (obj.width * .9, None)
    
    
    def _add_product(self, _):
        anaam = self.add_naam.text.strip().lower()
        atype = self.add_type.text
        aprijs = self.add_prijs.text.strip()
        azicht = self.add_zichtbaar.text       
        
        if (anaam == "")+(atype == "-")+(aprijs == ""):
            self.makePopup("Vul alle velden in !")
        elif not func.is_number(aprijs):
            self.makePopup("Vul een geldige prijs in! Voor een komma moet je een punt gebruiken!")
        elif len(anaam)>global_vars.product_name_max:
            self.makePopup("De naam %s is te lang (max 26 letters)"%(anaam))
        else:
            try:
                #TODO: remove
                db_io = database.OpenIO(global_vars.db)
                azicht = global_vars.zichtbaar_int.index(azicht)
                db_prijs = int(float(aprijs)*100)
                ret = database.AddProduct(db_io, atype, anaam, db_prijs, azicht)
                
                if  ret == 0:
                    #popup succes
                    self.makePopup("Product met naam: %s en prijs: €%.2f toegevoegd." %(anaam, db_prijs/100),
                                   "Succes!")
                    #print ook bij op het scherm
                    self.lijst_bar.add_queue(func.to_dict(atype, anaam, db_prijs, azicht))
                elif ret == -1:
                    self.makePopup("Er bestaat reeds een product met dezelfde naam!",
                                   "Naam Error")
                else:
                    print("error catch add methode")
                
            except Exception as e:
                #popup error
                print(e)
            finally:
                #reset de velden
                self.add_naam.text = ""
                self.add_type.text = "-"
                self.add_prijs.text = ""
                self.add_zichtbaar.text = "Ja"
                database.CloseIO(db_io)
                
    
    def _bewerk_product(self, _):
        bnaam = self.bewerk_naam.text.strip().lower()
        btype = self.bewerk_type.text
        bprijs = self.bewerk_prijs.text.strip()
        bzicht = self.bewerk_zichtbaar.text
        if (bnaam == "")+(btype == "-")+(bprijs == ""):
            self.makePopup("Vul alle velden in !")
        elif not func.is_number(bprijs):
            self.makePopup("Vul een geldige prijs in! Voor een komma moet je een punt gebruiken!")
        elif len(bnaam)>global_vars.product_name_max:
            self.makePopup("De naam {} is te lang (max {} letters)".format(bnaam, global_vars.product_name_max))
        else:
            #TODO: remove
            db_io = database.OpenIO(global_vars.db)
            bzicht = global_vars.zichtbaar_int.index(bzicht)
            ret =  database.editProduct(db_io, bnaam, btype, int(float(bprijs)*100), bzicht)
            if ret == 0:
                self.makePopup("Product met naam %s bewerkt." %(bnaam,),
                                   "Succes!")
                self.lijst_bar.reload_from_db()
                self.bewerk_naam.text = ""
                self.bewerk_prijs.text = ""
                self.bewerk_type.text = "-"
                self.bewerk_zichtbaar.text = "Ja"
            else:
                self.makePopup("Er bestaat geen product met deze naam!",
                               "Naam Error")
            database.CloseIO(db_io)
            
        
    def _verwijder_product(self, _):
        vnaam = self.verwijder_naam.text.strip()
        if (vnaam == ""):
            self.makePopup("Vul het naamveld in !")
        else:
            #TODO: remove
            db_io = database.OpenIO(global_vars.db)
            ret = database.deleteProduct(db_io, vnaam)
            if ret == 0:
                self.makePopup("Product met naam %s succesvol verwijdert." %(vnaam,),
                               "Succes!")
                self.lijst_bar.reload_from_db()
            else:
                self.makePopup("Er bestaat geen product met deze naam!",
                               "Naam Error")
            self.verwijder_naam.text = ""
            database.CloseIO(db_io)
    
    
    def _zichtbaar_product(self, _):
        znaam = self.zichtbaar_naam.text.strip().lower()
        zzicht = self.zichtbaar_zichtbaar.text
        if (znaam == ""):
            self.makePopup("Vul het naamveld in !")
        else:
            #TODO: remove
            zzicht = global_vars.zichtbaar_int.index(zzicht)
            db_io = database.OpenIO(global_vars.db)
            ret = database.zichtProduct(db_io, znaam, zzicht)
            if ret == 0:
                self.makePopup("Product met naam %s succesvol aangepast." %(znaam,),
                               "Succes!")
                self.lijst_bar.reload_from_db()
            else:
                self.makePopup("Er bestaat geen product met deze naam!",
                               "Naam Error")
            self.zichtbaar_naam.text = ""
            self.zichtbaar_zichtbaar.text = "Ja"
            database.CloseIO(db_io)
            
            
    def makePopup(self, text, title="Product Error"):
        popup = Popup(title=title, size=(400,400), size_hint=(None,None))
        layout = GridLayout(cols=1)
                
        label = Label(text=text, font_size=20, halign="center")                      
        label.bind(width=self.update_text_width)
        layout.add_widget(label)   
        
        knop = Button(text="sluit", size_hint_y=None, height=40)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()


class ConnectBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2

        #on/off switch
        self.add_widget(Label(
                text="Server: ",
                size_hint_y=None,
                height=50,
                font_size=22))
        self.server_status = Switch(active=False, size_hint_y=None, height=50)
        self.server_status.bind(active=self.switch_server)
        self.add_widget(self.server_status)
        
        #self.add_widget(Label(
        #        text="Wachtwoord: ",
        #        size_hint_y=None,
        #        height=50,
        #        font_size=22))
        #self.password_veld = TextInput(multiline=False, font_size=20, height=50, size_hint_y=None)
        #self.add_widget(self.password_veld)
        
        #aanvaard connecties
        self.add_widget(Label(
                text="Nieuwe connecties aanvaarden: ",
                size_hint_y=None,
                height=50,
                font_size=22))
        aanvaard_status = Switch(active=True, size_hint_y=None, height=50)
        aanvaard_status.bind(active=self.switch_aanvaard)
        self.add_widget(aanvaard_status)
        
        #huidig IP adres
        self.add_widget(Label(
                text="IP adres server:",
                size_hint_y=None,
                height=50,
                font_size=22))
        self.add_widget(Label(
                text=socket_server.get_host_ip(),
                size_hint_y=None,
                height=50,
                font_size=22))
        
        #server_info
        self.auto_off = False
        
        
    def switch_server(self, instance, value):
        if value:
            #launch server
            socket_server.RUN = True
            threading.Thread(target=socket_server.start_listening,
                             args=(global_vars.db, 
                                   self.switch_server_off,
                                   gui.hoofdscherm.hoofdbar.update_rekeningen,
                                   gui.blistscherm.blist.update_list),
                             daemon=True).start()
        else:
            
            #verander stop variabele
            socket_server.RUN = False
            if not(self.auto_off):
                #trigger shutdown
                socket_server.TriggerSD()
            else:
                self.auto_off = False
           
        
    def switch_server_off(self):
        self.auto_off = True
        self.server_status.active = False    
    
    
    def switch_aanvaard(self, instance, value):
        pass
    

class PrinterBar(GridLayout):
    IP_WIDTH = 800
    ROW_HEIGHT = 50
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        top = GridLayout(cols=6, rows=1, height=50, size_hint_y=None)
        with top.canvas.before:
            #rgba
            Color(1, 0.4, 0, 0.8)  # green; colors range from 0-1 instead of 0-255
            self._rect2 = Rectangle(size=top.size, pos=top.pos)
        top.bind(size=self._update_rect2, pos=self._update_rect2)

        top.add_widget(Label(
                text="IP printers",
                font_size=25,
                halign="center",
                size_hint_x=None,
                width=self.IP_WIDTH))
        top.add_widget(Label(text="poort",font_size=25))
        top.add_widget(Label(text="", size_hint_x=0.75))
        top.add_widget(Label(text="Print types",font_size=25))
        knop = Button(text="?", width=50, size_hint_x=None, font_size=25)
        knop.bind(on_press=self.help_popup)
        top.add_widget(knop)
        self.add_widget(top)
        
        #dymisch opgevuld
        self.onder = GridLayout(cols=5)
        with self.onder.canvas.before:
            #rgba
            Color(1, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self._rect = Rectangle(size=self.onder.size, pos=self.onder.pos)

        self.onder.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widget(self.onder)
        
        self.ip_veld = TextInput(size_hint=(None, None), width=self.IP_WIDTH, height=self.ROW_HEIGHT, multiline=False, font_size=20)
        self.onder.add_widget(self.ip_veld)
        
        self.poort_veld = TextInput(size_hint_y=None, height=self.ROW_HEIGHT, multiline=False, font_size=20)
        self.onder.add_widget(self.poort_veld)
        
        self.onder.add_widget(Label(text="", size_hint_x=0.75, size_hint_y=None, height=self.ROW_HEIGHT))
        
        knop = Button(text="selecteer types", height = self.ROW_HEIGHT, size_hint_y=None, font_size=20)
        knop.bind(on_press=self.select_type)
        self.onder.add_widget(knop)
        
        knop = Button(text="+", height = self.ROW_HEIGHT, size_hint_y=None, font_size=22, width=50, size_hint_x=None)
        knop.bind(on_press=self.toevoegen)
        self.onder.add_widget(knop)
        
        #variabele dat alle printers opslaat
        self.printers = [] #[ip, poort, (types,)] ID van de knop is de index van deze lijst
        self.print_widgets = []
        self.checkboxes = []
        
        if os.path.isfile(global_vars.printer_file):
            self.laad_data(global_vars.printer_file)
        
        
    def _update_rect(self, instance, value):
        self._rect.pos = instance.pos
        self._rect.size = instance.size
        
        
    def _update_rect2(self, instance, value):
        self._rect2.pos = instance.pos
        self._rect2.size = instance.size
        
        
    def _update_text_width(self, obj, _):
        '''
            Dit is noodzakelijk voor automatische multiline
        '''
        obj.text_size = (obj.width * .9, None)
    
    
    def help_popup(self, instance):
        popup = Popup(title="Printers - help", size=(640,480), size_hint=(None,None))
        layout = GridLayout(cols=1)
                
        label = Label(text=global_vars.help_connect, font_size=18, valign="center")                      
        label.bind(width=self._update_text_width)
        layout.add_widget(label)   
        
        knop = Button(text="sluit", size_hint_y=None, height=40)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()
        
        
    def error_popup(self, text):
        popup = Popup(title="Printers - error", size=(400,400), size_hint=(None,None))
        layout = GridLayout(cols=1)
                
        label = Label(text=text, font_size=18, valign="center")                      
        label.bind(width=self._update_text_width)
        layout.add_widget(label)   
        
        knop = Button(text="sluit", size_hint_y=None, height=40)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()
    
    
    def laad_data(self, path):
        with open(path, 'rb') as f:    
            printers = pickle.load(f)
        for i in printers:
            self.toevoegen(0, *i)
    
    
    def store_data(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.printers,f)
        
    
    def toevoegen(self, _, IP=None, POORT=None, types=None):
        if (IP==None)+(POORT==None)+(types==None):
            IP = self.ip_veld.text.strip()
            POORT = self.poort_veld.text.strip()
            types = []
            for key in self.checkboxes:
                if key.active:
                    types.append(self.checkboxes[key])
                    
            if IP == "" or POORT == "":
                self.error_popup("Vul alle velden in!")
                return
            elif not(POORT.isdigit()):
                self.error_popup("Een poort is een positief getal.")
                return
            elif types == []:
                self.error_popup("Selecteer minstens 1 type!")
                return
        
        ID = len(self.printers)
        self.printers.append((IP, int(POORT), types))
        socket_server.PRINTERS = self.printers
        widget_list = [
            Label(
                    text=IP,
                    width= self.IP_WIDTH,
                    size_hint_x=None,
                    height = self.ROW_HEIGHT,
                    size_hint_y=None,
                    font_size=20,
                    color=(0,0,0,1)),
            Label(
                    text=str(POORT),
                    height = self.ROW_HEIGHT,
                    size_hint_y=None,
                    font_size=20,
                    color=(0,0,0,1))]
        #testknop
        knop = Button(
                text="TEST",
                id=str(ID),
                height = self.ROW_HEIGHT,
                size_hint_y=None,
                size_hint_x=0.75,
                font_size=20)#,
                #background_normal='',
                #background_color=(0.5, 0.5, 0.5,1))
        knop.bind(on_press=self.test_printer)
        widget_list.append(knop)
        
        #pasop als er 1 wordt verwijdert moeten alle ID's worden aangepast
        knop = Button(text="bekijk types", id=str(ID), height = self.ROW_HEIGHT, size_hint_y=None, font_size=20)
        knop.bind(on_press=self.zie_type)
        widget_list.append(knop)
        knop = Button(text="X", id=str(ID), height = self.ROW_HEIGHT, size_hint_y=None, font_size=20, width=50, size_hint_x=None)
        knop.bind(on_press=self.verwijder)
        widget_list.append(knop)
        
        for wid in widget_list:
            self.onder.add_widget(wid)
        self.print_widgets.append(widget_list)
        
        #reset widgets
        self.ip_veld.text = ""
        self.poort_veld.text = ""
        #reset de popup, wss niet nodig
    
        self.store_data(global_vars.printer_file)
    
    
    def verwijder(self, instance):
        #TODO: sluit ook die printer indien die open staat !
        ID = int(instance.id)
        if ID != len(self.printers)-1:
            #for lus en ID van de knoppen aanpassen
            for i in self.print_widgets[ID+1:]:
                _, _, test, knop1, knop2 = i
                test.id = str(int(test.id)-1)
                knop1.id = str(int(knop1.id)-1)
                knop2.id = str(int(knop2.id)-1)        
        
        widgets = self.print_widgets.pop(ID)
        for wid in widgets:
            self.onder.remove_widget(wid)
        del widgets
        del self.printers[ID]
        socket_server.PRINTERS = self.printers
        
        self.store_data(global_vars.printer_file)
    
    
    def test_printer(self, instance):
        ID = int(instance.id)
        threading.Thread(target=socket_server.printer_test,
                         args=self.printers[ID][:2],
                         daemon=True).start()
        #socket_server.printer_test(*self.printers[ID][:2])
    
    
    def select_type(self, _):
        db_io = database.OpenIO(global_vars.db)
        types = database.getTypes(db_io) #((type,), (type,))
        database.CloseIO(db_io)
        
        popup = Popup(title="Typeselectie", size=(400,400), size_hint=(None,None))
        layout = GridLayout(cols=2)
        #label = Label(text=global_vars.connect_info_type, font_size=18, valign="center")                      
        #label.bind(width=self._update_text_width)
        #layout.add_widget(label)
        self.checkboxes = {} #{obj:type}
        for type in types:
            cb = CheckBox(size_hint_x=None, width=60)
            self.checkboxes[cb] = type[0]
            layout.add_widget(cb)
            layout.add_widget(Label(text=type[0], font_size=18))
        #rekening
        cb = CheckBox(size_hint_x=None, width=60)
        self.checkboxes[cb] = "rekening"
        layout.add_widget(cb)
        layout.add_widget(Label(text="rekening", font_size=18))
        
        
        layout.add_widget(Label(size_hint_x=None, width=60))
        knop = Button(text="sluit", size_hint_y=None, height=40)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()
        
    
    def zie_type(self, instance):
        ID = int(instance.id)
        
        popup = Popup(title="Typeselectie", size=(400,400), size_hint=(None,None))
        layout = GridLayout(cols=1)
        #label = Label(text=global_vars.connect_info_type, font_size=18, valign="center")                      
        #label.bind(width=self._update_text_width)
        #layout.add_widget(label)
        
        for type in self.printers[ID][2]:
            layout.add_widget(Label(text=type, font_size=18))
        
        layout.add_widget(Label(size_hint_x=None, width=60))
        knop = Button(text="sluit", size_hint_y=None, height=40)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()
        

#gebaseerd op de clientversie
class BestelBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 2
        self.spacing = [10,5]
       
        #huidige pagina
        self.paginaNr = 0
        self.ID_info = Button(
                text="Klantinfo:",
                size_hint_x = 0.4, 
                size_hint_y = None,
                font_size = 20,
                height = 35)
        self.ID_info.bind(on_press=self.show_info)
        self.add_widget(self.ID_info)

        self.pagina_label = Label(
                text="Pagina 1",
                size_hint_y = None,
                height = 35,
                font_size = 18)
        self.add_widget(self.pagina_label)

        self.add_widget(Label(
                text=" ",
                size_hint_x = 0.2,
                size_hint_y = None,
                height = 35))
        
        #huidige bestelling
        self.bestel_label = LijstLabel()
        leftLayout = GridLayout(cols=1, rows=3, size_hint_x=0.4)
        leftLayout.add_widget(self.bestel_label)
        self.totaal_label = Label(
                text="{:<25}€{:>6}".format("TOTAAL:", 0),
                size_hint_y=None,
                font_name="RobotoMono-Regular",
                height=35)
        leftLayout.add_widget(self.totaal_label)
        
        knopLayout = GridLayout(cols=3, rows=1, size_hint_y=None, height=50)
        
        self.edit_mode = 0 #{1:DEL, 2:+, 3:-}
        self.edit_knoppen = []
        for naam in ["DEL", "[b]+[/b]", "[b]-[/b]"]:
            self.edit_knoppen.append(Button(text=naam, font_size=20, markup=True))
            self.edit_knoppen[-1].bind(on_press=self.edit)
            knopLayout.add_widget(self.edit_knoppen[-1])
        
        
        
        leftLayout.add_widget(knopLayout)
        self.add_widget(leftLayout)
        
        
        #product knoppen
        self.product_knoppen = []
        self.product_grid = GridLayout(cols=global_vars.product_cols)
        for _ in range(global_vars.product_rows*global_vars.product_cols):
            self.product_knoppen.append(Button(text="", font_size=20, halign="center"))
            self.product_knoppen[-1].bind(on_press=self.klikProduct, width=self._update_text_width)
            self.product_grid.add_widget(self.product_knoppen[-1])
        self.add_widget(self.product_grid)
        
        #actie knoppen
        self.actie_grid = GridLayout(cols=1, size_hint_x=0.2)
        knop = Button(text="ALLE ORDERS", size_hint_y=0.5, font_size=20)
        knop.bind(on_press=self.view_orders)
        self.actie_grid.add_widget(knop)
        
        knop = Button(text="VERWIJDER ORDER", size_hint_y=0.5, font_size=20)
        knop.bind(on_press=self.delete_order)
        self.actie_grid.add_widget(knop)
        
        for _ in range(global_vars.product_rows-4):
            knop = Button(text=" ")
            knop.bind(on_press=self.actie)
            self.actie_grid.add_widget(knop)
        
        knop = Button(text="VERWIJDER", size_hint_y=0.5, font_size=22, background_color=(0,1,0.9,1))
        knop.bind(on_press=self.actie)
        self.actie_grid.add_widget(knop)
        
        knop = Button(text="AFREKENEN", size_hint_y=0.5, font_size=22, background_color=(1,1,0,1))
        knop.bind(on_press=self.afrekenen)
        self.actie_grid.add_widget(knop)
            
        knop = Button(text="HERLAAD", size_hint_y=0.5, font_size=22, background_color=(0,0.2,0.9,1))
        knop.bind(on_press=self.actie)
        self.actie_grid.add_widget(knop)
           
        self.bewerk_knop = Button(text="BERWERK", size_hint_y=0.5, font_size=22, background_color=(1,1,1,1))
        self.bewerk_knop.bind(on_press=self.actie)
        self.actie_grid.add_widget(self.bewerk_knop)

        
        #navigatieknoppen
        knop = Button(text="<-", size_hint_y=0.5, font_size=22, background_color=(0,1,0,1))
        knop.bind(on_press=self.switchPagina)
        self.actie_grid.add_widget(knop)
        
        knop = Button(text="->", size_hint_y=0.5, font_size=22, background_color=(0,1,0,1))
        knop.bind(on_press=self.switchPagina)
        self.actie_grid.add_widget(knop)
        
        self.add_widget(self.actie_grid)
        
        
    def klikProduct(self, instance):
        #TODO voeg toe aan een lokale bestelling, indien we het ook naar de printer willen sturen!
        #en de db aan moeten passen
        #doe enkel iets als self.edit_mode != 0 aanstaat!
        if self.edit_mode == 0:
            self.makePopup(global_vars.bewerk_NT)
            return
        if instance.text.strip() == "":
            return
        if self.edit_mode == 1:
            if gui.DATA.bestelling_del_prod(instance.text) == -1:
                self.makePopup(global_vars.product_del)
        else:
            div = -1 if (self.edit_mode == 3) else 1
            if gui.DATA.bestelling_add_prod(instance.text, div) == -1:
                self.makePopup(global_vars.product_min)
        
        self.bestel_label.verklein_bestelling() #volledig weg
        self.update_list = gui.DATA.bestelling_list()
        Clock.schedule_once(self.refill, 0.001)
    
    
    def reset(self):
        self.paginaNr = 0
        self.pagina_label.text = "Pagina 1"
        self.edit_mode = 0
        self.bewerk_knop.text = "BEWERK"
        self.bewerk_knop.background_color = (1,1,1,1)
        for knop in self.edit_knoppen:
            knop.background_color = (1,1,1,1)
        
        #verwijder de edit bestelling
        gui.DATA.edit_reset()
        
        self.vul_in()
        #maak het label leeg of populate het
        self.bestel_label.verklein_bestelling() #volledig weg
        #laadt de bestelgeschiedenis in 
        self.update_list = gui.DATA.bestelling_list()
        Clock.schedule_once(self.refill, 0.5)
        
        #vul totaal in
        self.totaal_label.text = "{:<25}€{:>6}".format("TOTAAL:", gui.DATA.bereken_prijs())
        
    
    def vul_in(self):
        data = gui.DATA.get_prod()
        COLS = global_vars.product_cols
        ROWS = global_vars.product_rows
        if len(data)<self.paginaNr*COLS*ROWS:
            end = len(data)
        else:
            end = COLS*ROWS*(self.paginaNr+1)
        data = data[COLS*ROWS*self.paginaNr:end]
        for i, knop in enumerate(self.product_knoppen):
            try:
                knop.text = data[i][1]
                knop.background_color = global_vars.COLOURS.get(data[i][0], (1,1,1,1))
            except:
                knop.text = ""
                knop.background_color = (1,1,1,1)
    
       
    def switchPagina(self, instance):
        if instance.text == "->":
            self.paginaNr += 1 if (self.paginaNr+1<gui.DATA.get_num_pages(global_vars.product_cols, global_vars.product_rows)) else 0
        else:
            self.paginaNr -= 1 if (self.paginaNr>0) else 0
        
        self.pagina_label.text = "Pagina " + str(self.paginaNr+1)
        self.vul_in()
        
        
    def set_ID(self, ID):
        self.ID_klant = ID
        #self.ID_label.text = "[b]ID: %s[/b]" % (ID)
    
    
    #bestellabelfuncties    
    #vult het label
    def refill(self, *_):
        if len(self.update_list):
            self.bestel_label.update_bestelling(self.update_list.pop(0))
            Clock.schedule_once(self.refill,0.001)
            
            
    def edit(self, instance):
        if self.edit_mode  == 0:
            self.makePopup(global_vars.bewerk_NT)
            return 
        
        cmd = instance.text
        if cmd == "DEL":
            self.edit_mode = 1
            self.edit_knoppen[0].background_color = (0,1,0,1)
            self.edit_knoppen[1].background_color = (1,1,1,1)
            self.edit_knoppen[2].background_color = (1,1,1,1)
        elif cmd == "[b]+[/b]":
            self.edit_mode = 2
            self.edit_knoppen[0].background_color = (1,1,1,1)
            self.edit_knoppen[1].background_color = (0,1,0,1)
            self.edit_knoppen[2].background_color = (1,1,1,1)
        elif cmd == "[b]-[/b]":
            self.edit_mode = 3
            self.edit_knoppen[0].background_color = (1,1,1,1)
            self.edit_knoppen[1].background_color = (1,1,1,1)
            self.edit_knoppen[2].background_color = (0,1,0,1)
       
    
    def actie(self, instance):
        knop = instance.text.strip()
        if knop == "":
            return
        elif knop == "HERLAAD":
            db_io = database.OpenIO(global_vars.db)
            bestelling = database.getBestelling(db_io, gui.DATA.get_info()["ID"])
            if bestelling == -1:
                #TODO popup
                #normaal zou dit nooit mogen voorvallen
                return
            
            gui.DATA.set_bestelling(bestelling)
            #gui.DATA.set_info({"ID":int(instance.text)})
            self.reset()

        elif knop == "BEWERK":
            #zet een variabele dat toelaat om te bewerken op True
            self.edit_mode = 2
            self.makePopup(global_vars.bewerk_start)
            self.bewerk_knop.text = "OPSLAAN"
            self.bewerk_knop.background_color = (0.96,0.25,0.25,1)
            
            #zet add mode aan
            self.edit_knoppen[1].background_color = (0,1,0,1)
            
            
        elif knop == "OPSLAAN":
            #zet een variabele dat toelaat om te bewerken weer op False en pas de bestelling in de db aan
            #TODO geef popup en laat de persoon akkoord gaan!
        
            self.makePopup(global_vars.bewerk_opslaan)
            #pas db aan
            db_io = database.OpenIO(global_vars.db)
            #volgende stap zou kunnen mislopen indien er juist een bestelling toekomt
            while socket_server.EDIT_ID == gui.DATA.get_info()["ID"]:
                #loop totdat het aan ons is
                pass
            socket_server.EDIT_ID = gui.DATA.get_info()["ID"]
            database.addBestelling(db_io, {"id":gui.DATA.get_info()["ID"]}, gui.DATA.get_edit())
            socket_server.EDIT_ID = None
            # order table bewerken
            msg = {
                    "bestelling":{
                            "info":{
                                "id":gui.DATA.get_info()["ID"],
                                "naam":"N/A",
                                "tafel":"N/A",
                                "verkoper":"KASSA",
                                },
                            "BST":gui.DATA.get_edit_order()
                            },
                    "hash": datetime.datetime.now().strftime("%M%S"),#random value
            }
            gui.blistscherm.add(database.addOrder(db_io, msg, ip_poort="KASSA:EDIT", status="EDIT"))
            
            
            gui.DATA.set_bestelling(database.getBestelling(db_io, gui.DATA.get_info()["ID"]))      
            database.CloseIO(db_io)
            
            #reset textvak
            self.reset()
            
            self.bewerk_knop.text = "BEWERK"
            self.bewerk_knop.background_color = (1,1,1,1)
            
            self.edit_mode = 0
            for knop in self.edit_knoppen:
                knop.background_color = (1,1,1,1)
                
            
        elif knop == "VERWIJDER":
            self.vpopup = Popup(title="Verwijderen", size=(400,400), size_hint=(None,None))
            layout = GridLayout(cols=1)
                    
            label = Label(text=global_vars.knop_verwijder, font_size=20)                      
            label.bind(width=self.update_text_width)
            layout.add_widget(label)   
            
            knoplayout = BoxLayout(orientation="horizontal")
        
            knop = Button(text="annuleer", size_hint_y=None, height=40)
            knop.bind(on_press=self.vpopup.dismiss)
            knoplayout.add_widget(knop)
            
            knop = Button(text="verwijder", size_hint_y=None, height=40)
            knop.bind(on_press=self.verwijder_bevestigd)
            knoplayout.add_widget(knop)
            
            layout.add_widget(knoplayout)
            
            self.vpopup.add_widget(layout)                        
            self.vpopup.open()
            
    
    def afrekenen(self, *_):
        if self.edit_mode != 0:
            self.makePopup(global_vars.knop_afrekenen)
            return 
        #bereken de prijs, en na betaling zet open of false en vul prijs veld in
        totaal = gui.DATA.bereken_prijs()
        
        self.afpopup = Popup(title="Afrekenen", size=(800,600), size_hint=(None,None))
        layout = GridLayout(cols=1)
        
        toplayout = GridLayout(cols=2, size_hint_y=None, height=325)
        toplayout.add_widget(Label(text="Te betalen:", font_size=20))
        
        toplayout.add_widget(Label(text="€ {}".format(totaal), font_size=20))
                
        toplayout.add_widget(Label(text="Onvangen: ", font_size=20))
        self.tonvangen = TextInput(text="0", multiline=False, font_size=20)
        toplayout.add_widget(self.tonvangen)
        
        knop = Button(text="Wisselgeld: ", font_size=20)
        knop.bind(on_press=self.bereken_wisselgeld)
        toplayout.add_widget(knop)
        
        self.twisselgeld = Label(text="---", font_size=20)
        toplayout.add_widget(self.twisselgeld)
        
#        toplayout.add_widget(Label(text="Fooi:", font_size=20))
#        self.tfooi = TextInput(text="0", multiline=False, font_size=20)
#        toplayout.add_widget(self.tfooi)
    
        
        toplayout.add_widget(Label(text="Betaalwijze:", font_size=20))
        self.betaalwijze_spinner = Spinner(
                text="---",
                values=global_vars.betaal_methodes,
                font_size=18)
        
        toplayout.add_widget(self.betaalwijze_spinner)
        
        layout.add_widget(toplayout)
        
        self.blabel = Label(font_size=22, markup=True, halign="center")
        self.blabel.bind(width=self._update_text_width)
        layout.add_widget(self.blabel)
        #TODO: naar printer sturen
        knop = Button(text="Ticket afdrukken", size_hint_y=0.75, font_size=20)
        knop.bind(on_press=self.print_ticket)
        layout.add_widget(knop)

        knoplayout = BoxLayout(orientation="horizontal")
    
        knop = Button(text="annuleer", size_hint_y=None, height=60)
        knop.bind(on_press=self.afpopup.dismiss)
        knoplayout.add_widget(knop)
        
        knop = Button(text="ontvangen", size_hint_y=None, height=60)
        knop.bind(on_press=self.afronden_bevestigd)
        knoplayout.add_widget(knop)
        
        layout.add_widget(knoplayout)
        
        self.afpopup.add_widget(layout)                        
        self.afpopup.open()
    
    
    def print_ticket(self, _):
        #run in een andere thread, of start een thread hier!
        ex_info, p_art = gui.DATA.get_info_ticket()
        ex_info["tijd"] = datetime.datetime.now().strftime("%d/%m/%y - %H:%M:%S")
        threading.Thread(target=socket_server.print_kasticket,
                         args=(gui.DATA.get_bestelling(),
                               ex_info,
                               p_art,
                               gui.DATA.bereken_prijs()),
                         daemon=True).start()
        
    
    def verwijder_bevestigd(self, *_):
        db_io = database.OpenIO(global_vars.db)
        database.delByID(db_io, self.ID_klant)
        
        #ga terug naar het hoofdscherm en update het scherm
        gui.hoofdscherm.hoofdbar.update_rekeningen(db_io)
        gui.screen_manager.current = "HOME"
        database.CloseIO(db_io)
        
        self.vpopup.dismiss()
        
    
    def bereken_wisselgeld(self, *_):
        totaal = gui.DATA.bereken_prijs()
        ontvangen = self.tonvangen.text.strip()
        if not(isinstance(totaal, float)) or not(func.is_number(ontvangen)):
            self.twisselgeld.text = "ERROR"
        else:
            #ERROR fix: https://docs.python.org/2/library/decimal.html
            self.twisselgeld.text = "{0:.2f}".format(float(ontvangen)-totaal) #analoog aan round(x, 2)
        

    def afronden_bevestigd(self, *_):
        betaalwijze = self.betaalwijze_spinner.text.strip()        
        if betaalwijze == "---":
            self.blabel.text="[color=#ff0000]Selecteer een betaal methode![/color]"
            return
#        elif not(func.is_number(self.tfooi.text)):
#            self.blabel.text = "[color=#ff0000]Fooi is geen getal![/color]"
#            return
        
#        fooi = float(self.tfooi.text)
        
#        if fooi < 0:
#            self.blabel.text = "[color=#ff0000]Een negatieve fooi kan niet![/color]"
#            return
        
        
        db_io = database.OpenIO(global_vars.db)
        totaal = gui.DATA.bereken_prijs_raw()
        
        if totaal == "ERROR":
            self.blabel.text="[color=#ff0000]De bestelling bevat een product waarvan we de prijs niet kennen.[/color]"
            database.CloseIO(db_io)
            return
        
        database.sluitById(db_io, self.ID_klant, totaal, betaalwijze) #totaal + fooi
        
        #ga terug naar het hoofdscherm en update het scherm
        gui.hoofdscherm.hoofdbar.update_rekeningen(db_io)
        gui.screen_manager.current = "HOME"
        database.CloseIO(db_io)
        self.afpopup.dismiss()
        
    
    def view_orders(self, _):
        pass
    
    
    def delete_order(self, _):
        pass
        
    #knoppen
    def _update_text_width(self, instance, _):
        instance.text_size = (instance.width * .9, None)
            
        
    #POPUP
    def makePopup(self, text):
        popup = Popup(title="Bewerken", size=(400,400), size_hint=(None,None))
        layout = GridLayout(cols=1)
                
        label = Label(text=text, font_size=20, valign="center")                      
        label.bind(width=self.update_text_width)
        layout.add_widget(label)   
        
        knop = Button(text="sluit", size_hint_y=None, height=40)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()
    
    
    def update_text_width(self, obj, _):
        '''
            Dit is noodzakelijk voor automatische multiline
        '''
        obj.text_size = (obj.width * .9, None)
    
    
    def show_info(self, *_):
        popup = Popup(title="Klantinfo", size=(400,400), size_hint=(None, None))
        layout = GridLayout(cols=1)
    
        
        db_io = database.OpenIO(global_vars.db)
        naam, betaald = database.getInfoByID(db_io, self.ID_klant)
        _tijd, _hash, _tafel = database.getOrderLastInfo(db_io, self.ID_klant)
        database.CloseIO(db_io)
        
        layout.add_widget(Label(text="ID:  {}".format(self.ID_klant), font_size=20))
        layout.add_widget(Label(text="Naam:  {}".format(naam), font_size=20))
        layout.add_widget(Label(text="Tafel: {}".format(_tafel), font_size=20))
        layout.add_widget(Label(text="Betaald: {}".format("Nee" if (betaald) else "JA"), font_size=20))
        layout.add_widget(Label(text="tijd: {}".format(_tijd), font_size=20))
        layout.add_widget(Label(text="hash: {}".format(_hash), font_size=20))

        
        layout.add_widget(Label(size_hint_y=2))
                
        knop = Button(text="sluit", size_hint_y=None, height=40)
        knop.bind(on_press=popup.dismiss)
        layout.add_widget(knop)
        
        popup.add_widget(layout)                        
        popup.open()
        
        
class StatistiekBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.rows = 1
        self.spacing = [15, 0]
        
        #modes
        self.mode_links = [None, None, 0] #start, end, open
        self.omzet_mode = [None, None]
        
        #update_lists
        self.update_list_links = []
        self.update_list_mid = []
        
        #linker kolom
        links = GridLayout(cols=1, rows=2, spacing=[0, 10])
        #bevat de mogelijkheden + herlaadknop
        linkstop = GridLayout(cols=1, size_hint_y=0.25) 
        knop = Button(text="selectie", font_size=20)
        knop.bind(on_press=self.lselectie)
        
        linkstop.add_widget(knop)
        knop = Button(text="herlaad", font_size=20)
        knop.bind(on_press=self.herlaad_links)
        linkstop.add_widget(knop)        
        
        self.lerror = Label(text="", font_size=20, markup=True)
        self.lerror.bind(width=self._update_text_width)
        linkstop.add_widget(self.lerror)
        
        links.add_widget(linkstop)
        self.links_scroll = LijstLabel() #momenteel in db
        self.update_list_links = ["{:^28}##".format("Product"), "-"*32]
        self.refill_left()
        links.add_widget(self.links_scroll)
        self.add_widget(links)
        
        #midden
        midden = GridLayout(cols=1, rows=2, spacing=[0, 10])
        #bevat de mogelijkheden + herlaadknop + import knop
        midtop = GridLayout(cols=1, size_hint_y=0.25)
        midtopa = GridLayout(cols=2)
        knop = Button(text="import .csv", font_size=20)
        knop.bind(on_press=self.import_csv_popup)
        midtopa.add_widget(knop)
        knop = Button(text="import .xlsx", font_size=20)
        knop.bind(on_press=self.import_xlsx_popup)
        midtopa.add_widget(knop)
        midtop.add_widget(midtopa)
        self.mid_status = Label(text="", font_size=20, markup=True, size_hint_y=0.58, halign="center")
        self.mid_status.bind(width=self._update_text_width)
        midtop.add_widget(self.mid_status)
    
        
        midden.add_widget(midtop)
        self.mid_scroll = LijstLabel() #import csv
        self.update_list_mid = ["{:^28}##".format("Product"), "-"*32]
        self.refill_mid()
        midden.add_widget(self.mid_scroll)
        self.add_widget(midden)
        
        rechts = GridLayout(cols=1, spacing=[0, 2])
        rechtstop = GridLayout(cols=2, size_hint_y=1.5, padding=[5, 5])
        with rechtstop.canvas.before:
            #rgba
            Color(0.4, 0.4, 0.4, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=rechtstop.size, pos=rechtstop.pos)

        rechtstop.bind(size=self._update_rect, pos=self._update_rect)
        
        knop = Button(
                text="selectie", 
                font_size=20,
                background_color=(0.05,0,0.80,1))
        knop.bind(on_press=self.omzet_selectie)
        rechtstop.add_widget(knop)
        knop = Button(
                text="herlaad",
                font_size=20,
                background_color=(0.05,0.8,0,1))
        knop.bind(on_press=self.omzet_herlaad)
        
        rechtstop.add_widget(knop)
        rechtstop.add_widget(Label(text="totale omzet:", font_name="RobotoMono-Regular", font_size=18))
        self.rmethodes = {"omzet":Label(text="€ {:>9}".format(0), font_name="RobotoMono-Regular", font_size=18)}
        rechtstop.add_widget(self.rmethodes["omzet"])
        
        for methode in global_vars.betaal_methodes:
            rechtstop.add_widget(Label(text='{}:'.format(methode), font_name="RobotoMono-Regular", font_size=18))
            self.rmethodes[methode] = Label(text="€ {:>9}".format(0), font_name="RobotoMono-Regular", font_size=18)
            rechtstop.add_widget(self.rmethodes[methode])
        
        
        rechts.add_widget(rechtstop)
        
        self.rerror = Label(text="", font_size=20, markup=True, size_hint_y=0.5)
        self.rerror.bind(width=self._update_text_width)
        rechts.add_widget(self.rerror)
        
        rechts.add_widget(Label(text=""))
        rechts_export = GridLayout(cols=2, rows=2)
        
        
        knop = Button(text="Export .csv", font_size=20)
        knop.bind(on_press=self.export_csv)
        rechts_export.add_widget(knop)
        
        knop = Button(text="Export .xlsx", font_size=20)
        knop.bind(on_press=self.export_xlsx)
        rechts_export.add_widget(knop)
        
        rechts_export.add_widget(Button())
        rechts_export.add_widget(Button())
        
        
        rechts.add_widget(rechts_export)
        self.add_widget(rechts)
        
        
    def lselectie(self, _):
        self.lpopup = Popup(title="selectie", size=(300, 300), size_hint=(None,None))
        layout = GridLayout(cols=1)
                
        toplayout = GridLayout(cols=2, rows=4)
        toplayout.add_widget(Label(text="Start ID:", font_size=20))
        self.lstart = TextInput(multiline=False, font_size=18)
        toplayout.add_widget(self.lstart)
        toplayout.add_widget(Label(text="Laatste ID:", font_size=20))
        self.lend = TextInput(multiline=False, font_size=18)
        toplayout.add_widget(self.lend)
        toplayout.add_widget(Label(text="Alle ID's", font_size=20))
        self.lalles = CheckBox()
        toplayout.add_widget(self.lalles)
        toplayout.add_widget(Label(text="status:", font_size=20))
        self.lstatus = Spinner(
                text="afgesloten",
                values=("afgesloten", "open"),
                font_size=18)
        toplayout.add_widget(self.lstatus)
        layout.add_widget(toplayout)
        
        knop = Button(text="herlaad", size_hint_y=None, height=40)
        knop.bind(on_press=self.lselectie_herlaad)
        layout.add_widget(knop)
        
        self.lpopup.add_widget(layout)                        
        self.lpopup.open()
        
    
    def lselectie_herlaad(self, _):
        self.links_scroll.verklein_bestelling()
        cb = self.lalles.active
        start_id = self.lstart.text.strip()
        end_id = self.lend.text.strip()
        status = (self.lstatus.text == "open") + 0
        if cb and (start_id != "" or end_id != ""):
            self.lerror.text = global_vars.selectie_beide
            self.lpopup.dismiss()
            return
        elif not(cb) and start_id == "" and end_id == "":
            self.lerror.text = global_vars.selectie_niets
            self.lpopup.dismiss()
            return
        elif not(start_id.isdigit()) and not(end_id.isdigit()) and not(cb):
            self.lerror.text = global_vars.selectie_nummer
            self.lpopup.dismiss()
            return
       
        
        self.lerror.text = ""

        db_io = database.OpenIO(global_vars.db)
        if cb:
            self.mode_links = [None, None, status]
            self.update_list_links = func.print_dict(database.getTotaalProd(db_io, status=status))
        elif start_id.isdigit() and end_id.isdigit():
            self.mode_links = [int(start_id), int(end_id), status]
            self.update_list_links = func.print_dict(database.getTotaalProd(db_io, int(start_id), int(end_id), status))
        elif start_id.isdigit() and end_id == "":
            self.mode_links = [int(start_id), None, status]
            self.update_list_links = func.print_dict(database.getTotaalProd(db_io, int(start_id), None, status))
        elif start_id ==  "" and end_id.isdigit():
            self.mode_links = [None, int(end_id), status]
            self.update_list_links = func.print_dict(database.getTotaalProd(db_io, None, int(end_id), status))
        else:
            self.lerror.text = global_vars.selectie_neg
        
        self.lpopup.dismiss()
        Clock.schedule_once(self.refill_left, 0.5)
        database.CloseIO(db_io)
        
        
    def herlaad_links(self, instance):
        db_io = database.OpenIO(global_vars.db)
        try:
            ret = func.print_dict(database.getTotaalProd(db_io, *self.mode_links)) #we krijgen een grote dict terug en veranderen het naar een lijst
            self.links_scroll.verklein_bestelling() #volledig weg
            #laadt de bestelgeschiedenis in 
            self.update_list_links = ret 
            Clock.schedule_once(self.refill_left, 0.5)
                
        except Exception as e:
            self.lerror.text = "Er liep iets mis..."
            print("ERR: ", e)
        finally:
            database.CloseIO(db_io)
            self.lerror.text = ""
    
    
    def refill_left(self, *_):
        #vult het linkselabel
        if len(self.update_list_links):
            self.links_scroll.update_bestelling(self.update_list_links.pop(0))
            Clock.schedule_once(self.refill_left, 0.001)

    
    def refill_mid(self, *_):
        if len(self.update_list_mid):
            self.mid_scroll.update_bestelling(self.update_list_mid.pop(0))
            Clock.schedule_once(self.refill_mid, 0.001)
     
        
    def import_csv_popup(self, _):
        self.ipopup = Popup(title="Importeren", size=(600,400), size_hint=(None,None))
        layout = GridLayout(cols=1)
                
        self.FS = FileChooserListView(size_hint_y=None, height=290)
        layout.add_widget(self.FS)
        
        knoplayout = BoxLayout(orientation="horizontal")
    
        knop = Button(text="annuleer", size_hint_y=None, height=40)
        knop.bind(on_press=self.ipopup.dismiss)
        knoplayout.add_widget(knop)
        
        knop = Button(text="importeren", size_hint_y=None, height=40, id="csv")
        knop.bind(on_press=self.import_data)
        knoplayout.add_widget(knop)
        
        layout.add_widget(knoplayout)
        
        self.ipopup.add_widget(layout)                        
        self.ipopup.open()
    
    
    def import_xlsx_popup(self, _):
        self.ipopup = Popup(title="Importeren", size=(600,400), size_hint=(None,None))
        layout = GridLayout(cols=1)
                
        self.FS = FileChooserListView(size_hint_y=None, height=290)
        layout.add_widget(self.FS)
        
        knoplayout = BoxLayout(orientation="horizontal")
    
        knop = Button(text="annuleer", size_hint_y=None, height=40)
        knop.bind(on_press=self.ipopup.dismiss)
        knoplayout.add_widget(knop)
        
        knop = Button(text="importeren", size_hint_y=None, height=40, id="xlsx")
        knop.bind(on_press=self.import_data)
        knoplayout.add_widget(knop)
        
        layout.add_widget(knoplayout)
        
        self.ipopup.add_widget(layout)                        
        self.ipopup.open()
        
        
    def import_data(self, instance):
        if not(self.FS.selection):
            self.mid_status.text = "[color=#ff0000]Selecteer een bestand![/color]"
            self.ipopup.dismiss()
            return
        file = self.FS.selection[0]
        ID = instance.id
        if file.split(".")[-1] != instance.id:
            self.mid_status.text = "[color=#ff0000]Dit is geen .{} bestand![/color]".format(ID)
            self.ipopup.dismiss()
            return
        if ID == "csv":
            ret_d = {}
            ret = database.importCSV(file, ret_d)
            if ret == 0:
                self.mid_status.text = file.split("\\")[-1]
                self.mid_scroll.verklein_bestelling()
                self.update_list_mid = func.print_dict(ret_d)
                Clock.schedule_once(self.refill_mid, 0.5)
            elif ret == -1:
                self.mid_status.text = "[color=#ff0000]Ongeldig bestand![/color]"
            else:
                self.mid.status.text = "[color=#ffff00]ERROR...[/color]"
        else:#XLSX
            ret_d = {}
            ret = database.importXLSX(file, ret_d)
            if ret == 0:
                self.mid_status.text = file.split("\\")[-1]
                self.mid_scroll.verklein_bestelling()
                self.update_list_mid = func.print_dict(ret_d)
                Clock.schedule_once(self.refill_mid, 0.5)
            elif ret == -1:
                self.mid_status.text = "[color=#ff0000]Ongeldig bestand![/color]"
            else:
                self.mid.status.text = "[color=#ffff00]ERROR...[/color]"
        
        self.ipopup.dismiss()
        
        
    def omzet_selectie(self, _):
        self.rpopup = Popup(title="selectie", size=(300, 300), size_hint=(None,None))
        layout = GridLayout(cols=1)
                
        toplayout = GridLayout(cols=2, rows=3)
        toplayout.add_widget(Label(text="Start ID:", font_size=20))
        self.rstart = TextInput(multiline=False, font_size=18)
        toplayout.add_widget(self.rstart)
        toplayout.add_widget(Label(text="Laatste ID:", font_size=20))
        self.rend = TextInput(multiline=False, font_size=18)
        toplayout.add_widget(self.rend)
        toplayout.add_widget(Label(text="Alle ID's", font_size=20))
        self.ralles = CheckBox(active=True)
        toplayout.add_widget(self.ralles)
        
        layout.add_widget(toplayout)
        knop = Button(text="herlaad", size_hint_y=None, height=40)
        knop.bind(on_press=self.omzet_selectie_herlaad)
        layout.add_widget(knop)
        
        self.rpopup.add_widget(layout)                        
        self.rpopup.open()
    
    
    def omzet_selectie_herlaad(self, _):
        cb = self.ralles.active
        start_id = self.rstart.text.strip()
        end_id = self.rend.text.strip()
        if cb and (start_id != "" or end_id != ""):
            self.rerror.text = global_vars.selectie_beide
            self.rpopup.dismiss()
            return
        elif not(cb) and start_id == "" and end_id == "":
            self.rerror.text = global_vars.selectie_niets
            self.rpopup.dismiss()
            return
        elif not(start_id.isdigit()) and not(end_id.isdigit()) and not(cb):
            self.rerror.text = global_vars.selectie_nummer
            self.rpopup.dismiss()
            return
        
        self.rerror.text = ""

        if cb:
            self.omzet_mode = [None, None]
        elif start_id.isdigit() and end_id.isdigit():
            self.omzet_mode = [int(start_id), int(end_id)]
        elif start_id.isdigit() and end_id == "":
            self.omzet_mode = [int(start_id), None]
        elif start_id ==  "" and end_id.isdigit():
            self.omzet_mode = [None, int(end_id)]
        else:
            self.rerror.text = global_vars.selectie_neg
            self.rpopup.dismiss()
            return
        self.omzet_herlaad(None)        
        self.rpopup.dismiss()
        
    
    def omzet_herlaad(self, _):
        db_io = database.OpenIO(global_vars.db)
        ret = database.getOmzet(db_io, *self.omzet_mode)
        for key in self.rmethodes:
            self.rmethodes[key].text = "€ {:>9}".format(round(ret.get(key,0),2))
        database.CloseIO(db_io)
        self.rerror.text = ""
            
    
    def export_csv(self, _):
        db_io = database.OpenIO(global_vars.db)
        try:
            database.exportCSV(db_io)
        except Exception as e:
            print("[CSV]Error: ", e)
        finally:
            database.CloseIO(db_io)
            
    
    def export_xlsx(self, _):
        db_io = database.OpenIO(global_vars.db)
        try:
            database.exportXLSX(db_io)
        except Exception as e:
            print("[XLSX]Error: ", e)
        finally:
            database.CloseIO(db_io)
            
    #resize
    def _update_text_width(self, obj, _):
        obj.text_size = (obj.width * .95, None)
    
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class BListBar(GridLayout):
    safe_dir = "logs"
    backup_best = ""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 2
        
        self.save_log_file = global_vars.save_log_file
        
        self.add_widget(Label(
                text="Bestellingen", 
                size_hint_y = None,
                height = 35,
                font_size = 18))
        
        self.add_widget(Label(
                text="Selecteer/zie een bestelling",
                size_hint_y = None,
                height = 35,
                font_size = 18))
        
        
        #scroll label
        listgrid = GridLayout(cols=1, rows=2, size_hint_x=1.8)
        listgrid.add_widget(Label(
                text="{:^12}\t\t{:^6}\t\t{:^8}\t\t{:^24}\t\t{:^14}\t\t{:^10}".format("TIJD", "ID", "HASH", "IP:POORT", "TYPES", "STATUS"),
                size_hint_y=None,
                height=50,
                font_name="RobotoMono-Regular"))
        
        self.blist = LijstLabel()
        self.blist.set_down_scrolling(False) #True
        listgrid.add_widget(self.blist)
        
        self.add_widget(listgrid)
        
        #selectie menu
        smaingrid = GridLayout(cols=1)
        sgrid = GridLayout(cols=2, rows=6, size_hint_y=1.2)
        
        sgrid.add_widget(Label(text="all checks", font_size=20))
        self.check_switch = Switch(active=False)
        self.check_switch.bind(active=self.check_switch_active)
        sgrid.add_widget(self.check_switch)
        
        sgrid.add_widget(Label(text="checkinterval", font_size=20))
        check_counter = Spinner(
            text=str(socket_server.CTRLCHECKCOUNTER), 
            values=('3', '5', '10', '15', '20', '50', '100'), 
            font_size=18)
        check_counter.bind(text=self.check_counter_select)
        sgrid.add_widget(check_counter)
        
        sgrid.add_widget(Label(text="ID: ", font_size=20))
        self.select_id = TextInput(multiline=False, font_size=18)
        sgrid.add_widget(self.select_id)
        
        sgrid.add_widget(Label(text="HASH: ", font_size=20))
        self.select_hash = TextInput(multiline=False, font_size=18)
        sgrid.add_widget(self.select_hash)
        
        knop = Button(text="opvragen", font_size=20)
        knop.bind(on_press=self.view_order)
        sgrid.add_widget(knop)
        
        knop = Button(text="resend", font_size=20)
        knop.bind(on_press=self.resend)
        sgrid.add_widget(knop)
        
        knop = Button(text="clear scherm", font_size=20)
        knop.bind(on_press=self.clear_best)
        sgrid.add_widget(knop)
        
        knop = Button(text="clear scherm + verwijder", font_size=17, id="del")
        knop.bind(on_press=self.clear_best)
        sgrid.add_widget(knop)
        
        
        
        smaingrid.add_widget(sgrid)
        self.select_error = Label(
                markup=True, 
                font_size=20,
                size_hint_y = None,
                height = 50)
        smaingrid.add_widget(self.select_error)
        
        smaingrid.add_widget(Label())
        
        log_grid = GridLayout(cols=2, rows=2, size_hint_y=0.5)
        knop = Button(text="open log", font_size=20)
        knop.bind(on_press=self.open_log)
        log_grid.add_widget(knop)
        knop = Button(text="opslaan", font_size=20)
        knop.bind(on_press=self.opslaan_log)
        log_grid.add_widget(knop)
        knop = Button(text="verwijder log", font_size=20)
        knop.bind(on_press=self.verwijder_log)
        log_grid.add_widget(knop)
        knop = Button(text="", font_size=20)
        #knop.bind()
        log_grid.add_widget(knop)

        
        smaingrid.add_widget(log_grid)
        self.log_info = Label(
                markup=True, 
                font_size=20,
                size_hint_y = None,
                height = 50)
        smaingrid.add_widget(self.log_info)
        
        self.add_widget(smaingrid)

        if not(os.path.isdir(self.safe_dir)):
            os.mkdir(self.safe_dir)
        
    #called when app closes
    def save_log(self, name=None):
        if self.backup_best == "" and self.blist.get_text().strip() == "":
            return -1
        if name is None:
            name = global_vars.save_log_file
            
        with open(os.path.join(self.safe_dir, name), 'w') as log_file:
            log_file.write("{}\n".format(datetime.datetime.now()))
            log_file.write(self.backup_best)
            log_file.write(self.blist.get_text())
        return 0


    def update_list(self, info, statcolor=None):
        if statcolor is None:
        #"TIJD", "ID", "HASH", "IP:POORT", "TYPES", "STATUS"
            lijn = "{:^12}\t\t{:^6}\t\t{:^8}\t\t{:^24}\t\t{:^14}\t\t{:^10}".format(*info)
        else:
            info.insert(-1, "[color={}]".format(statcolor))
            lijn = "{:^12}\t\t{:^6}\t\t{:^8}\t\t{:^24}\t\t{:^14}\t\t{}{:^10}[/color]".format(*info)
        self.blist.update_bestelling(lijn)
        
    
    def check_switch_active(self, _, value):
        socket_server.BEST_OK = value
        
    
    def check_counter_select(self, _, value):
        socket_server.CTRLCHECKCOUNTER = int(value)
        
    
    def view_order(self, _):
        _id = self.select_id.text.strip()
        _hash = self.select_hash.text.strip()
        if not(_id) or not(_hash):
            self.select_error.text = "[color=#ff0000]Vul het ID en hash veld in![/color]"
            return
        elif not(_id.isdigit()):
            self.select_error.text = "[color=#ff0000]Het ID veld moet een getal zijn![/color]"
            return
        elif self.select_error.text != "":
            self.select_error.text = ""
        
        #open een popup!
        db_io = database.OpenIO(global_vars.db)
        info = database.getOrder(db_io, int(_id), _hash)
        database.CloseIO(db_io)
        
        if isinstance(info, int):
            self.select_error.text = "[color=#ff0000]Er bestaat geen bestelling met deze combinatie.[/color]"
            return
        bst = info[0]
        
        self.order_popup = Popup(title="Order:", size_hint=(0.4, 0.8))
        
        main_grid = GridLayout(cols=1, padding=3, spacing=5)
        
        order_info = GridLayout(cols=1)
        for key in bst['info']:
            order_info.add_widget(Label(text="{}: {}".format(key, bst['info'][key]), font_size=20))
            
        order_info.add_widget(Label(text="besteld op: {}".format(info[2]), font_size=20))
        order_info.add_widget(Label(text="types: {}".format(info[1]), font_size=20))
        order_info.add_widget(Label(text="hash: {}".format(_hash), font_size=20))
        main_grid.add_widget(order_info)
        
        
        maxlen = global_vars.product_name_max
        
        self.update_list = [" {:*^{}} ".format("", maxlen)]
        
        for t in bst['BST']:
            self.update_list.append("[b][color=#20ab40]{:^{}}[/color][/b]".format(t, maxlen+5))
            type_dict = bst['BST'][t]
            for prod in type_dict:
                self.update_list.append("{:<{}}: {}".format(prod, maxlen, type_dict[prod]))
        
        self.aantal_prod = LijstLabel()
        main_grid.add_widget(self.aantal_prod)
        self.refill()
        
        popup_knoppen = GridLayout(cols=2, rows=1, size_hint_y=.25, spacing=3)
        knop = Button(text="resend", font_size=20, id="popup")
        knop.bind(on_press=self.resend)
        popup_knoppen.add_widget(knop)
        knop = Button(text="sluit", font_size=20)
        knop.bind(on_press=self.order_popup.dismiss)
        popup_knoppen.add_widget(knop)
        
        main_grid.add_widget(popup_knoppen)
        
        self.order_popup.add_widget(main_grid)
        self.order_popup.open()
        
        
    def refill(self, *_):
        if len(self.update_list):
            self.aantal_prod.update_bestelling(self.update_list.pop(0))
            Clock.schedule_once(self.refill,0.01)
            
    
    def resend(self, instance):
        if instance.id == "popup":
            self.order_popup.dismiss()
        _id = self.select_id.text.strip()
        _hash = self.select_hash.text.strip()
        if not(_id) or not(_hash):
            self.select_error.text = "[color=#ff0000]Vul het ID en hash veld in![/color]"
            return
        elif not(_id.isdigit()):
            self.select_error.text = "[color=#ff0000]Het ID veld moet een getal zijn![/color]"
            return
        elif self.select_error.text != "":
            self.select_error.text = ""
        
        db_io = database.OpenIO(global_vars.db)
        info = database.getOrder(db_io, int(_id), _hash)
        database.CloseIO(db_io)
        
        if isinstance(info, int):
            self.select_error.text = "[color=#ff0000]Er bestaat geen bestelling met deze combinatie.[/color]"
            return
        self.resend_bst = info
        bst = info[0]
        types = tuple(bst['BST'].keys())
        print(bst)
        
        self.resend_popup = Popup(title="Resend:", size_hint=(0.5, 0.7))
        
        main_grid = GridLayout(cols=1, padding=3)
        
        main_grid.add_widget(Label(text="naam: {}".format(bst['info']['naam']), font_size=18, size_hint_y=0.2))
        order_info = GridLayout(cols=2)
        
        for key in bst['info']:
            if key == 'naam':
                continue
            order_info.add_widget(Label(text="{}: {}".format(key, bst['info'][key]), font_size=18))
        
        order_info.add_widget(Label(text="besteld op: {}".format(info[2]), font_size=18))
        order_info.add_widget(Label(text="types: {}".format(info[1]), font_size=18))
        order_info.add_widget(Label(text="hash: {}".format(_hash), font_size=18))
        main_grid.add_widget(order_info)
        
        main_grid.add_widget(Label(text="[b]Selecteer printer:[/b]".format(bst['info']['naam']), font_size=22, size_hint_y=0.2, markup=True))
        
        printer_grid = GridLayout(cols=2, rows=3)
        printer_grid.add_widget(Label(text="IP:", font_size=18))
        self.resend_ip = TextInput(font_size=18, multiline=False)
        printer_grid.add_widget(self.resend_ip)
        printer_grid.add_widget(Label(text="poort:", font_size=18))
        self.resend_poort = TextInput(font_size=18, multiline=False)
        printer_grid.add_widget(self.resend_poort)
        
        printer_grid.add_widget(Label(text="type:", font_size=18))
        self.resend_type = Spinner(
            text="",
            values=types, 
            font_size=16)
        printer_grid.add_widget(self.resend_type)
        main_grid.add_widget(printer_grid)
        
        self.resend_info = Label(text=" ", font_size=18, size_hint_y=0.2, markup=True)
        main_grid.add_widget(self.resend_info)
        
        popup_knoppen = GridLayout(cols=2, rows=1, size_hint_y=.25, spacing=3)
        knop = Button(text="resend", font_size=20, id="popup")
        knop.bind(on_press=self.resend_bevestig)
        popup_knoppen.add_widget(knop)
        knop = Button(text="annuleer", font_size=20)
        knop.bind(on_press=self.resend_popup.dismiss)
        popup_knoppen.add_widget(knop)
        
        main_grid.add_widget(popup_knoppen)
    
        self.resend_popup.add_widget(main_grid)
        self.resend_popup.open()
        
    
    def resend_bevestig(self, _):
        _ip = self.resend_ip.text.strip()
        _poort = self.resend_poort.text.strip()
        _type = self.resend_type.text.strip()
        if not(_ip) or not(_poort):
            self.resend_info.text = "[color=#ff0000]Vul een ip en een poort in![/color]"
            return
        elif not(_poort.isdigit()):
            self.resend_info.text = "[color=#ff0000]Een poort is een getal![/color]"
            return
        elif _type == "":
            self.resend_info.text = "[color=#ffff00]Selecteer een type.[/color]"
            return

        #def printer_bestelling_resend(bestelling, h, order_list, ip, poort, _type):
        threading.Thread(target=socket_server.printer_bestelling_resend,
                         args=(self.resend_bst[0],
                               self.select_hash.text.strip(),
                               self.update_list, 
                               _ip, int(_poort),
                               _type),
                         daemon=True).start()
        self.resend_popup.dismiss()                 
        
    
    def clear_best(self, instance):
        if instance.id != "del":
            self.backup_best = self.blist.get_text()
        self.blist.verklein_bestelling()
        if self.select_error.text != "":
            self.select_error.text = ""
        
    
    def open_log(self, _):
        fp = os.path.join(self.safe_dir, global_vars.save_log_file)
        if not(os.path.isfile(fp)):
            self.log_info.text = "[color=#ffff00]Geen logfile gevonden.[/color]"
            return
        with open(fp, 'r') as log_file:
            data = log_file.readlines()
        self.blist.set_bestelling_all("".join(data[1:]))
        self.log_info.text = "[color=#00ff00]{} geopend en aan het inlezen.[/color]".format(fp)
        
    
    def opslaan_log(self, _):
        name = datetime.datetime.now().strftime("%d%m%y@%H-%M-%S_BST.log")
        ret = self.save_log(name)
        if ret == -1:
            self.log_info.text = "[color=#ffff00]Er is geen data om op te slaan.[/color]"
        elif ret == 0:
            fp = os.path.join(self.safe_dir, name)
            self.log_info.text = "[color=#00ff00]opgeslagen in: {}[/color]".format(fp)
            
    
    def verwijder_log(self, _):
        fp = os.path.join(self.safe_dir, global_vars.save_log_file)
        if not(os.path.isfile(fp)):
            self.log_info.text= "[color=#ffff00]Geen logfile gevonden.[/color]"
        else:
            os.remove(fp)
            self.log_info.text = "{} verwijdert.".format(fp)
            

#scrolllabel -> gekopieerd van client.py
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
        self.bar_width = 10
        
        self.layout = GridLayout(size_hint_y=None, cols=1)
        self.add_widget(self.layout)

        self.bestelling = Label(
                text="\n\n",
                markup=True,
                size_hint_y=None,
                color=(0,0,0,1),
                font_name="RobotoMono-Regular") #noodzakelijk voor spacing
        #oproepen via een andere functie/later is enige opl, op een zeer kleininterval
        #een andere optie is om het te samen te doen en eerste de volledigetekste te maken
        self.layout.add_widget(self.bestelling)
        
        #scroll
        self._dscrolling = False
        self.scroll_to_point = Label(size_hint_y=None, height=30)
        self.layout.add_widget(self.scroll_to_point)
        
        self.dq = deque()
        self.stopped_loop = True
            
    
    # Methos called externally to add new message to the chat history  
    def update_bestelling(self, lijn, _=None):
        #we kunnen geen nieuw label maken, dit zal voor problemen zorgen
        #ook kunnen we update_chat_history pas oproepen als het scherm getekent wordt

        #voeg bericht toe
        self.bestelling.text += lijn + '\n'
        
        # Set layout height to whatever height of self.naam text is + 15 pixels
        # (adds a bit of space at the bottom)
        # Set chat history label to whatever height of chat history text is
        self.layout.height = self.bestelling.texture_size[1] + global_vars.expand_size
        self.bestelling.height = self.bestelling.texture_size[1]
            #el.text_size = (el.width * 0.98, None) #kan later problemen geven
            
        if self._dscrolling:
            self.scroll_to(self.scroll_to_point)
            
    
    def set_bestelling_all(self, data):
        self.verklein_bestelling()
        for i in data.split("\n"):
            if not(i):
                continue
            self.add_queue(i)


    def verklein_bestelling(self, aantal=-1, _=None):
        if (aantal == -1):
            aantal = self.bestelling.text.count('\n')
        self.bestelling.text = "".join([i+'\n' for i in self.bestelling.text.split('\n')][:-aantal])

        self.layout.height = self.bestelling.texture_size[1] - global_vars.expand_size*aantal
        self.bestelling.height = self.bestelling.texture_size[1]
                    
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    
    def set_down_scrolling(self, value):
        self._dscrolling = value
        
    
    def get_text(self):
        return self.bestelling.text
    
    
    def add_queue(self, data):
        self.dq.append(data)
        if self.stopped_loop:
            self.stopped_loop = False
            Clock.schedule_once(self.add_loop_product, 0.5)
        
    
    def add_loop_product(self, *_):
        product = self.dq.popleft()
        Clock.schedule_once(partial(self.update_bestelling, product), 0.0001)
        if len(self.dq) != 0:
            Clock.schedule_once(self.add_loop_product, 0.01)
        else:
            self.stopped_loop = True
        

#gebruikt bij productscherm
class ProductLijstLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #witte achtergrond

        with self.canvas.before:
            #rgba
            Color(220/255, 220/255, 230/255, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        #Scrollview attributen
        self.bar_width = 10
        
        # ScrollView does not allow us to add more than one widget, so we need to trick it
        # by creating a layout and placing two widgets inside it
        # Layout is going to have one collumn and and size_hint_y set to None,
        # so height wo't default to any size (we are going to set it on our own)
        self.layout = GridLayout(size_hint_y=None, cols=4)
        self.add_widget(self.layout)

        # Now we need two wodgets - Label for chat history and 'artificial' widget below
        # so we can scroll to it every new message and keep new messages visible
        # We want to enable markup, so we can set colors for example
        
        self.naam = Label(size_hint_y=None, markup=True, halign="center", font_size=18, color=(0,0,0,1))
        self.type = Label(size_hint_y=None, markup=True, halign="center", font_size=18, color=(0,0,0,1))
        self.prijs = Label(size_hint_y=None, markup=True, halign="center", font_size=18, color=(0,0,0,1))
        self.zichtbaar = Label(size_hint_y=None, markup=True, halign="center", font_size=18, color=(0,0,0,1)) #test

        # We add them to our layout
        self.list = [self.naam, self.type, self.prijs, self.zichtbaar]

        for el in self.list:
            self.layout.add_widget(el)

            
        #oproepen via een andere functie/later is enige opl, op een zeer kleininterval
        #een andere optie is om het te samen te doen en eerste de volledigetekste te maken
        
        #data inladen
        Clock.schedule_once(self.update_from_db,1)
            
    # Methos called externally to add new message to the chat history  
    def update_chat_history(self, product, _):
        #we kunnen geen nieuw label maken, dit zal voor problemen zorgen
        #ook kunnen we update_chat_history pas oproepen als het scherm getekent wordt

        # First add new line and message itself
        self.naam.text += '\n' + product.get('naam','***')
        self.type.text += '\n' + product.get('type','***')
        prijs = product.get("prijs", "***")
        if isinstance(prijs, int):
            prijs = "{}.{}".format(str(prijs)[:-2], str(prijs)[-2:])
        self.prijs.text += '\n' + prijs
        if product.get('zichtbaar','***') == "[b][u]ZICHTBAAR:[/b][/u]":
            self.zichtbaar.text += '\n' + "[b][u]ZICHTBAAR:[/b][/u]"
        else:
            self.zichtbaar.text += '\n' + global_vars.zichtbaar_int[product.get('zichtbaar',2)]
    

        # Set layout height to whatever height of self.naam text is + 15 pixels
        # (adds a bit of space at the bottom)
        # Set chat history label to whatever height of chat history text is
        # Set width of chat history text to 98 of the label width (adds small margins)
        self.layout.height = self.naam.texture_size[1] + global_vars.expand_size
        for el in self.list:
            el.height = el.texture_size[1]
            #el.text_size = (el.width * 0.98, None) #kan later problemen geven
    
    
    def verklein_update_list(self, aantal=-1, _=None):
        if (aantal == -1):
            aantal = self.naam.text.count('\n')
        for el in self.list:
            el.text = "".join([i+'\n' for i in el.text.split('\n')][:-aantal])
            
        self.layout.height = self.naam.texture_size[1] - global_vars.expand_size*aantal
        for el in self.list:
            el.height = el.texture_size[1]
                    
    
    def add_update_list(self, _=None):
        #https://github.com/kivy/kivy/issues/1317
        product = self.dq.popleft()
        Clock.schedule_once(partial(self.update_chat_history, product), 0.0001)
        if len(self.dq) != 0:
            Clock.schedule_once(self.add_update_list, 0.01)
        else:
            self.stopped_loop = True
        
        
    def add_queue(self, product):
        self.dq.append(product)
        if self.stopped_loop:
            self.stopped_loop = False
            self.add_update_list()
            
    
    def extend_queue(self, product_queue):
        self.dq.extend(product_queue)
        if self.stopped_loop:
            self.stopped_loop = False
            self.add_update_list()
            
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    
    def update_from_db(self, _):
        self.stopped_loop = True
        self.dq = deque()
        self.dq.append(func.to_dict("[b][u]TYPE:[/b][/u]",
                                    "[b][u]NAAM:[/b][/u]",
                                    "[b][u]PRIJS:[/b][/u]",
                                    "[b][u]ZICHTBAAR:[/b][/u]"))
        db_io = database.OpenIO(global_vars.db)
        for i in database.getAllProduct(db_io):
            self.add_queue(func.to_dict(*i))
        database.CloseIO(db_io)
    
    
    def reload_from_db(self):
        Clock.schedule_once(partial(self.verklein_update_list,-1), 0.5) #all
        Clock.schedule_once(self.update_from_db, 1)
        
    
#gui
class ServerGui(App):
    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition()) #FadeTransition())
        
        self.hoofdscherm = HoofdScherm()
        scherm = Screen(name="HOME")
        scherm.add_widget(self.hoofdscherm)
        self.screen_manager.add_widget(scherm)

        self.productscherm = ProductScherm()
        scherm = Screen(name="PRODUCTEN")
        scherm.add_widget(self.productscherm)
        self.screen_manager.add_widget(scherm)
        
        self.connectscherm = ConnectScherm()
        scherm = Screen(name="CONNECTIES")
        scherm.add_widget(self.connectscherm)
        self.screen_manager.add_widget(scherm)

        self.test = OptieScherm()
        scherm = Screen(name="SETTINGS")
        scherm.add_widget(self.test)
        self.screen_manager.add_widget(scherm)
        
        self.statsscherm = StatsScherm()
        scherm = Screen(name="STATISTIEKEN")
        scherm.add_widget(self.statsscherm)
        self.screen_manager.add_widget(scherm)
        
        self.rekeningscherm = BestelScherm()
        scherm = Screen(name="BESTEL")
        scherm.add_widget(self.rekeningscherm)
        self.screen_manager.add_widget(scherm)
        
        self.blistscherm = BListScherm()
        scherm = Screen(name="BESTELLINGEN")
        scherm.add_widget(self.blistscherm)
        self.screen_manager.add_widget(scherm)
        
        return self.screen_manager
    
    
    def on_start(self):
        self.DATA = func.Client_storage()
    
    
    def on_stop(self):
        #mss sluit de overige db_io, socket connections
        try:
            gui.blistscherm.save_log()
            database.CloseIO(self.hoofdscherm.hoofdbar.db_io)
            gui.connectscherm.connectbar.switch_server_off()
            
            #altijd als laatste want meestal error
            gui.connectscherm.kill_printers()
        except Exception as e:
            print("[ERROR_EXIT]", e)
    


if __name__ == "__main__": 
    #maak de tabellen
    db_io = database.OpenIO(global_vars.db)
    database.InitTabels(db_io)
    database.CloseIO(db_io)    
    #fullscreen
    #Window.fullscreen = "auto"
    Window.maximize()
    gui = ServerGui()
    gui.run()