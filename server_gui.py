from functools import partial #instead of lamda functions
from collections import deque
import threading
import os
import pickle

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
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition#, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

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
        self.connectbar = ConnectBar(height=150, size_hint_y=None)
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
        
        settings_knop = Button(
                text="SETTINGS",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "setting") else (1,1,1,1)
                )
        settings_knop.bind(on_press=self.switch)
        self.add_widget(settings_knop)
        
        
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
        print(self.paginaNr)
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
        else:
            try:
                #TODO: remove
                db_io = database.OpenIO(global_vars.db)
                azicht = global_vars.zichtbaar_int.index(azicht)
                ret = database.AddProduct(db_io, atype, anaam, float(aprijs), azicht)
                if  ret == 0:
                    #popup succes
                    self.makePopup("Product met naam: %s en prijs: €%s toegevoegd." %(anaam,aprijs),
                                   "Succes!")
                    #print ook bij op het scherm
                    self.lijst_bar.add_queue(func.to_dict(atype, anaam, aprijs, azicht))
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
        else:
            #TODO: remove
            db_io = database.OpenIO(global_vars.db)
            bzicht = global_vars.zichtbaar_int.index(bzicht)
            ret =  database.editProduct(db_io, bnaam, btype, float(bprijs), bzicht)
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
                                   gui.hoofdscherm.hoofdbar.update_rekeningen),
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
        top = GridLayout(cols=5, rows=1, height=50, size_hint_y=None)
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
        top.add_widget(Label(text="Print types",font_size=25))
        knop = Button(text="?", width=50, size_hint_x=None, font_size=25)
        knop.bind(on_press=self.help_popup)
        top.add_widget(knop)
        self.add_widget(top)
        
        #dymisch opgevuld
        self.onder = GridLayout(cols=4)
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
        
        knop = Button(text="selecteer types", height = self.ROW_HEIGHT, size_hint_y=None, font_size=20)
        knop.bind(on_press=self.select_type)
        self.onder.add_widget(knop)
        
        knop = Button(text="+", height = self.ROW_HEIGHT, size_hint_y=None, font_size=22, width=50, size_hint_x=None)
        knop.bind(on_press=self.toevoegen)
        self.onder.add_widget(knop)
        
        #variabele dat alle printers opslaat
        self.printers = [] #[ip, poort, (types,)] ID van de knop is de index van deze lijst
        self.print_widgets = []
        self.checkboxes = {}
        
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
        else:
            POORT = str(POORT)
        
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
                    text=POORT,
                    height = self.ROW_HEIGHT,
                    size_hint_y=None,
                    font_size=20,
                    color=(0,0,0,1))]
        
        
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
                _, _, knop1, knop2 = i
                knop1.id = str(int(knop1.id)-1)
                knop2.id = str(int(knop2.id)-1)        
        
        widgets = self.print_widgets.pop(ID)
        for wid in widgets:
            self.onder.remove_widget(wid)
        del widgets
        del self.printers[ID]
        socket_server.PRINTERS = self.printers
        
        self.store_data(global_vars.printer_file)
    
    
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
        
        self._bewerk = False
        
        #huidige pagina
        self.paginaNr = 0
        self.ID_label = Label(
                text="ID: ",
                size_hint_x = 0.4, 
                size_hint_y = None,
                font_size = 20,
                height = 35,
                markup = True)
        self.add_widget(self.ID_label)

        self.pagina_label = Label(
                text="Pagina 1",
                size_hint_y = None,
                height = 35,
                font_size = 16)
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
        
        knopLayout = GridLayout(cols=5, rows=1, size_hint_y=None, height=50)
        
        for text in ["UP", "DOWN", "[b]+[/b]", "[b]-[/b]", "DEL"]:
            knop = Button(text=text, font_size=20, markup=True)
            knop.bind(on_press=self.edit_knop)
            knopLayout.add_widget(knop)
        leftLayout.add_widget(knopLayout)
        self.add_widget(leftLayout)
        
        
        #product knoppen
        self.product_knoppen = []
        self.product_grid = GridLayout(cols=global_vars.product_cols)
        for _ in range(global_vars.product_rows*global_vars.product_cols):
            self.product_knoppen.append(Button(text=""))
            self.product_knoppen[-1].bind(on_press=self.klikProduct)
            self.product_grid.add_widget(self.product_knoppen[-1])
        self.add_widget(self.product_grid)
        
        #actie knoppen
        self.actie_grid = GridLayout(cols=1, size_hint_x=0.2)
        for _ in range(global_vars.product_rows-2):
            knop = Button(text=" ")
            knop.bind(on_press=self.actie)
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
        #doe enkel iets als self._bewerk aanstaat!
        if not(self._bewerk):
            self.makePopup(global_vars.bewerk_NT)
            return
        if instance.text.strip() == "":
            return
        gui.DATA.bestelling_add_prod(instance.text, 1)
        self.bestel_label.verklein_bestelling() #volledig weg
        self.update_list = gui.DATA.bestelling_list()
        Clock.schedule_once(self.refill, 0.5)
    
    
    def reset(self):
        self.paginaNr = 0
        self.pagina_label.text = "Pagina 1"
        self._bewerk = False
        self.bewerk_knop.text = "BEWERK"
        self.bewerk_knop.background_color = (1,1,1,1)
        
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
        self.ID_label.text = "[b]ID: %s[/b]" % (ID)
    
    #bestellabelfuncties    
    #vult het label
    def refill(self, *_):
        if len(self.update_list):
            self.bestel_label.update_bestelling(self.update_list.pop(0))
            Clock.schedule_once(self.refill,0.01)
            
            
    def edit_knop(self, instance):
        if not(self._bewerk):
            self.makePopup(global_vars.bewerk_NT)
            return 
        cmd = instance.text
        if cmd == "[b]-[/b]":
            pass
        elif cmd == "[b]+[/b]":
            pass
        elif cmd == "DEL":
            pass
        elif cmd == "UP":
            pass
        else:
            #cmd == "DOWN":
            pass
    
    
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
            self._bewerk = True
            self.makePopup(global_vars.bewerk_start)
            self.bewerk_knop.text = "OPSLAAN"
            self.bewerk_knop.background_color = (0.96,0.25,0.25,1)
            
            
        elif knop == "OPSLAAN":
            #zet een variabele dat toelaat om te bewerken weer op False en pas de bestelling in de db aan
            self._bewerk = False
            self.makePopup(global_vars.bewerk_opslaan)
            self.bewerk_knop.text = "BEWERK"
            self.bewerk_knop.background_color = (1,1,1,1)
            
        
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
        self.bar_width = 5
        
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
        self.prijs.text += '\n' + str(product.get('prijs','***'))
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
        

   
#random - testing
class scherm1(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols=1
        
        self.navbar = NavigatieBar(huidig="setting")
        self.add_widget(self.navbar)
        self.add_widget(Label(text="scherm1"))
        
    
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

        self.test = scherm1()
        scherm = Screen(name="SETTINGS")
        scherm.add_widget(self.test)
        self.screen_manager.add_widget(scherm)
        
        self.rekeningscherm = BestelScherm()
        scherm = Screen(name="BESTEL")
        scherm.add_widget(self.rekeningscherm)
        self.screen_manager.add_widget(scherm)
        
        return self.screen_manager
    
    
    def on_start(self):
        self.DATA = func.Client_storage()
    
    
    def on_stop(self):
        #mss sluit de overige db_io, socket connections
        try:
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