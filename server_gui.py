from functools import partial
from collections import deque

#kivy
import kivy
from kivy.app import App
#achtergrond
from kivy.graphics import Color, Rectangle

#uix
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from kivy.core.window import Window
from kivy.clock import Clock

#zelfgeschreven
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
        self.history = LijstLabel(height=Window.size[1]*0.5, size_hint_y=None)
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
        
        
        
        #leeglabel
        self.add_widget(Label())
        
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
        self.button_grid = GridLayout(
                spacing=[10,15],
                cols=global_vars.kassa_cols,
                rows=global_vars.kassa_rows)
        for i in range(1,global_vars.kassa_cols * global_vars.kassa_rows+1):
            self.button_grid.add_widget(Button(text=''))
        
        self.add_widget(self.button_grid)
        


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
        self.db_io = None #database.InitProduct(global_vars.db)
        
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
                height=30)
        info_grid.add_widget(self.add_naam)
        
        info_grid.add_widget(Label(text="prijs:", font_size=17))
        self.add_prijs = TextInput(
                multiline=False, 
                font_size=17,
                size_hint_y=None,
                height=30)
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
                height=30)
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
                height=30)
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
                height=30)
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
                height=30)
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
            #TODO: maak een popup "vul alle velden in"
            self.makePopup("Vul alle velden in !")
        elif not func.is_number(aprijs):
            #TODO: maak een popup met ongeldig getal (gebruik '.')
            self.makePopup("Vul een geldige prijs in! Voor een komma moet je een punt gebruiken!")
        else:
            try:
                #TODO: remove
                db_io = database.InitProduct(global_vars.db)
                azicht = global_vars.zichtbaar_int.index(azicht)
                ret = database.AddProduct(db_io, atype, anaam, float(aprijs), azicht)
                if  ret == 0:
                    #popup succes
                    self.makePopup("Product met naam %s en prijs €%s toegevoegd." %(anaam,aprijs),
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
            db_io = database.InitProduct(global_vars.db)
            bzicht = global_vars.zichtbaar_int.index(bzicht)
            ret =  database.editProduct(db_io, bnaam, btype, float(bprijs), bzicht)
            if ret == 0:
                self.makePopup("Product met naam %s bewerkt." %(bnaam,),
                                   "Succes!")
                self.lijst_bar.reload_from_db()
                self.bewerk_naam.text = ""
                self.bewerk_prijs = ""
                self.bewerk_type = "-"
                self.bewerk_zichtbaar = "Ja"
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
            db_io = database.InitProduct(global_vars.db)
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
            db_io = database.InitProduct(global_vars.db)
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
        db_io = database.InitProduct(global_vars.db)
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
        
        
class scherm2(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="scherm2"))

#gui
class ServerGui(App):
    def build(self):
        self.screen_manager = ScreenManager(transition=FadeTransition())
        
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
        
        return self.screen_manager


if __name__ == "__main__":
    #fullscreen
    #Window.fullscreen = "auto"
    Window.maximize()
    gui = ServerGui()
    gui.run()