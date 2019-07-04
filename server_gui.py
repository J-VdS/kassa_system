import kivy
from kivy.app import App
#achtergrond
from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window
from kivy.config import Config

#fullscreen
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'fullscreen', 'auto')

kivy.require("1.10.1")

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
        
        #navigatiebar
        self.navbar = NavigatieBar()
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.hoofdbar = HoofdBar()
        self.add_widget(self.hoofdbar)
        
        
    
        
class ProductScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        #navigatiebar
        self.navbar = NavigatieBar(huidig="product")
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.productbar = ProductBar()
        self.add_widget(self.productbar)
        
        #producten, scrollable label --> zal mss een layout moeten worden
        #self.add_widget(Label())
#bars
class NavigatieBar(BoxLayout):
    def __init__(self, huidig="hoofd", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 5
        self.size_hint_y =  0.1
        self.padding = [10, 10] #padding horiz, padding width
        
        self.home_knop = Button(
                text="HOME",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "hoofd") else (1,1,1,1)
                )
        self.home_knop.bind(on_press=self.switch)
        self.add_widget(self.home_knop)
        
        self.product_knop = Button(
                text="PRODUCTEN",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "product") else (1,1,1,1)
                )
        self.product_knop.bind(on_press=self.switch)
        self.add_widget(self.product_knop)
        
        self.connect_knop = Button(
                text="CONNECTIES",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "connect") else (1,1,1,1)
                )
        self.connect_knop.bind(on_press=self.switch)
        self.add_widget(self.connect_knop)
        
        self.settings_knop = Button(
                text="SETTINGS",
                font_size=20,
                background_color = (1,0,0,1) if (huidig == "setting") else (1,1,1,1)
                )
        self.settings_knop.bind(on_press=self.switch)
        self.add_widget(self.settings_knop)
        
        
    def switch(self, instance):
        print(instance.text)
        try:
            gui.screen_manager.current = instance.text
        except:
            gui.screen_manager.current = "HOME"
        
        
class HoofdBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="links"))
        self.add_widget(Label(text="rechts"))


class ProductBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 5
        self.padding = [10, 10] #padding horiz, padding width
        
        self.add_widget(self._add_product_blok())
        self.add_widget(self._bewerk_product_blok())
        self.add_widget(self._zichtbaar_verwijder_blok())
        
        
    def _add_product_blok(self):
        grid = GridLayout(cols=1)
        grid.add_widget(Label(
                text="Voeg een product toe",
                size_hint_y=0.2, #check
                font_size=20
                ))
        info_grid = GridLayout(cols=2)
        
        info_grid.add_widget(Label(text="type:"))
        self.add_type = Spinner(
                text="-",
                values=("drank", "gerecht", "dessert", "divers", "pensen")
                )
        info_grid.add_widget(self.add_type)
        
        info_grid.add_widget(Label(text="naam:"))
        self.add_naam = TextInput(multiline=False)
        info_grid.add_widget(self.add_naam)
        
        info_grid.add_widget(Label(text="prijs"))
        self.add_prijs = TextInput(multiline=False)
        info_grid.add_widget(self.add_prijs)
        
        info_grid.add_widget(Label(text="zichtbaar"))
        self.add_zichtbaar = Spinner(
                text="Ja",
                values=("Ja", "Enkel voor kassa", "Nee")
                )
        info_grid.add_widget(self.add_zichtbaar)
        
        grid.add_widget(info_grid)
        knop = Button(text="toevoegen", font_size=20)
        #knop.bind(on_press=) #TODO
        grid.add_widget(knop)
        return grid
    
    
    def _bewerk_product_blok(self):
        grid = GridLayout(cols=1)
        grid.add_widget(Label(
                text="Bewerk een product",
                size_hint_y=0.15, #check
                font_size=20
                ))
        label = Label(
                text="Je kan een product bewerken door de naam van het product in te geven.Indien je de naam wil bewerken maak je best een nieuw product aan en verwijder je het andere.",
                split_str=' ',
                size_hint_y = 0.2,
                valign='top',
                halign='left'
                ))
        grid.add_widget(label)
        
        info_grid = GridLayout(cols=2)
        
        info_grid.add_widget(Label(text="naam:"))
        self.bewerk_naam = TextInput(multiline=False)
        info_grid.add_widget(self.bewerk_naam)
        
        info_grid.add_widget(Label(text="type:"))
        self.bewerk_type = Spinner(
                text="-",
                values=("drank", "gerecht", "dessert", "divers", "pensen")
               )
        info_grid.add_widget(self.bewerk_type)
        
        info_grid.add_widget(Label(text="prijs"))
        self.bewerk_prijs = TextInput(multiline=False)
        info_grid.add_widget(self.bewerk_prijs)
        
        info_grid.add_widget(Label(text="zichtbaar"))
        self.bewerk_zichtbaar = Spinner(
                text="Ja",
                values=("Ja", "Enkel voor kassa", "Nee")
                )
        info_grid.add_widget(self.bewerk_zichtbaar)
        
        grid.add_widget(info_grid)
        
        knop = Button(text="aanpassen", font_size=20)
        #knop.bind(on_press=) #TODO
        grid.add_widget(knop)
        return grid    
        
    
    def _zichtbaar_verwijder_blok(self):
        grid = GridLayout(cols=1)
        ''' verwijderblok '''
        grid.add_widget(Label(
                text="Verwijder",
                size_hint_y=0.1, #check
                font_size=20
                ))
        verwijder_grid = GridLayout(cols=2)
        verwijder_grid.add_widget(Label(text="naam:"))
        self.verwijder_naam = TextInput(multiline=False)
        verwijder_grid.add_widget(self.verwijder_naam)
        
        grid.add_widget(verwijder_grid)
        
        knop = Button(text="verwijder", font_size=20)
        #knop.bind(on_press=) #TODO
        grid.add_widget(knop)

        #zichtbaarheid
        grid.add_widget(Label(
                text="Zichtbaarheid",
                size_hint_y=0.15,
                font_size=20
                ))
        zichtbaar_grid = GridLayout(cols=2)
        zichtbaar_grid.add_widget(Label(text="naam:"))
        self.zichtbaar_grid = TextInput(multiline=False)
        zichtbaar_grid.add_widget(self.zichtbaar_grid)
        
        zichtbaar_grid.add_widget(Label(text="zichtbaar"))
        self.zichtbaar_zichtbaar = Spinner(
                text="Ja",
                values=("Ja", "Enkel voor kassa", "Nee")
                )
        zichtbaar_grid.add_widget(self.zichtbaar_zichtbaar)
        
        grid.add_widget(zichtbaar_grid)                
        
        knop = Button(text="zichtbaarheid\naanpassen", font_size=20)
        #knop.bind(on_press=) #TODO
        grid.add_widget(knop)
        
        return grid   
    
        
 #random       
class scherm1(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        
        return self.screen_manager


if __name__ == "__main__":
    #fullscreen
    #Window.fullscreen = "auto"
    gui = ServerGui()
    gui.run()