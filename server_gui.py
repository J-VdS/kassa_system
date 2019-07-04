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
from kivy.uix.scrollview import ScrollView

from kivy.core.window import Window
from kivy.clock import Clock

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
#label
#https://pythonprogramming.net/finishing-chat-application-kivy-application-python-tutorial/
#https://kivy.org/doc/stable/api-kivy.uix.scrollview.html
"""class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=4, spacing=5, size_hint_y=None)
        #opl voor de scrollfunctie, anders werkte deze niet
        self.layout.bind(minimum_height=self.layout.setter('height'))
       
        self.naam = Label(
                text="[b][u]NAAM[/b][/u]",
                size_hint_y=None,
                markup=True,
                font_size=15,
                height=20)
        self.type = Label(
                text="[b][u]TYPE[/b][/u]",
                size_hint_y=None,
                markup=True,
                font_size=15,
                height=20)
        self.prijs =  Label(
                text="[b][u]PRIJS[/b][/u]",
                size_hint_y=None,
                markup=True,
                font_size=15,
                height=20)
        self.zichtbaarheid =  Label(
                text="[b][u]ZICHTBAARHEID[/b][/u]",
                size_hint_y=None,
                markup=True,
                font_size=15,
                height=20)

        self.layout.add_widget(self.naam)
        self.layout.add_widget(self.type)
        self.layout.add_widget(self.prijs)
        self.layout.add_widget(self.zichtbaarheid)
        
        self.add_product()
        
    #werkt nog niet
    def add_product(self, product={'naam':'test'}):
        #product = {naam:..., type:..., prijs:..., zichtbaar:...}
        #self.producten.text += '\n' + product

        '''
        self.naam.text += '\n' + product.get('naam', '***')
        self.type.text += '\n' + product.get('type', '***')
        self.prijs.text += '\n' + str(product.get('prijs', '***'))
        self.zichtbaarheid.text += '\n' + product.get('zichtbaar', '***')
        
        
        self.layout.height = self.naam.texture_size[1] + 15
        
        for element in [self.naam, self.type, self.prijs, self.zichtbaarheid]:
            element.height = element.texture_size[1]
            element.text_size = (element.width * 0.98, None)
        '''
"""
class ScrollableLabel(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ScrollView does not allow us to add more than one widget, so we need to trick it
        # by creating a layout and placing two widgets inside it
        # Layout is going to have one collumn and and size_hint_y set to None,
        # so height wo't default to any size (we are going to set it on our own)
        self.layout = GridLayout(cols=2, size_hint_y=None)
        self.add_widget(self.layout)

        # Now we need two wodgets - Label for chat history and 'artificial' widget below
        # so we can scroll to it every new message and keep new messages visible
        # We want to enable markup, so we can set colors for example
        self.chat_history = Label(size_hint_y=None, markup=True, halign="center")
        self.chat_history2 = Label(size_hint_y=None, markup=True, halign="center") #test

        # We add them to our layout
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.chat_history2)
        
        
    # Methos called externally to add new message to the chat history
    def update_chat_history(self, message):

        # First add new line and message itself
        self.chat_history.text += '\n' + message
        self.chat_history2.text += '\n' + message
    

        # Set layout height to whatever height of chat history text is + 15 pixels
        # (adds a bit of space at teh bottom)
        # Set chat history label to whatever height of chat history text is
        # Set width of chat history text to 98 of the label width (adds small margins)
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history2.height = self.chat_history2.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)
        self.chat_history2.text_size = (self.chat_history2.width * 0.98, None)
        
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
        self.rows = 3

        #navigatiebar
        self.navbar = NavigatieBar(huidig="product")
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.productbar = ProductBar()
        self.add_widget(self.productbar)
        
        #producten, scrollable label --> zal mss een layout moeten worden
        self.history = ScrollableLabel(height=Window.size[1]*0.4, size_hint_y=None)
        self.add_widget(self.history)
#bars
class NavigatieBar(BoxLayout):
    def __init__(self, huidig="hoofd", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 5
        self.size_hint_y =  0.2
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
        grid = GridLayout(cols=1, spacing=[5,10])
        grid.add_widget(Label(
                text="Voeg een product toe",
                size_hint_y=0.2, #check
                font_size=20
                ))
        info_grid = GridLayout(cols=2)
        
        info_grid.add_widget(Label(text="type:"))
        self.add_type = Spinner(
                text="-",
                values=("drank", "gerecht", "dessert", "divers", "pensen"),
                )
        info_grid.add_widget(self.add_type)
        
        info_grid.add_widget(Label(text="naam:"))
        self.add_naam = TextInput(multiline=False)
        info_grid.add_widget(self.add_naam)
        
        info_grid.add_widget(Label(text="prijs:"))
        self.add_prijs = TextInput(multiline=False)
        info_grid.add_widget(self.add_prijs)
        
        info_grid.add_widget(Label(text="zichtbaar?"))
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
        grid = GridLayout(cols=1, spacing=[5,10])
        grid.add_widget(Label(
                text="Bewerk een product",
                size_hint_y=0.2, #check
                font_size=20
                ))
        label = Label(
                text="Je kan een product bewerken door de naam van het product in te geven.Indien je de naam wil bewerken maak je best een nieuw product aan en verwijder je het andere.",
                size_hint_y = 0.2,
                valign='top',
                halign='left'
                )
        label.bind(width=self.update_text_width)
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
        
        info_grid.add_widget(Label(text="prijs:"))
        self.bewerk_prijs = TextInput(multiline=False)
        info_grid.add_widget(self.bewerk_prijs)
        
        info_grid.add_widget(Label(text="zichtbaar?"))
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
        grid = GridLayout(cols=1, spacing=[5,10])
        ''' verwijderblok '''
        grid.add_widget(Label(
                text="Verwijder",
                size_hint_y=0.2, #check
                font_size=20
                ))
        label = Label(
                text="Je kan een product enkel verwijderen via naam. [color=#ff0000]Dit kan je niet ongedaan maken.[/color]",
                size_hint_y=0.2,
                valign='top',
                halign='left',
                markup=True
                )
        label.bind(width=self.update_text_width)
        grid.add_widget(label)
        verwijder_grid = GridLayout(cols=2)
        verwijder_grid.add_widget(Label(text="naam:"))
        self.verwijder_naam = TextInput(multiline=False)
        verwijder_grid.add_widget(self.verwijder_naam)
        
        grid.add_widget(verwijder_grid)
        
        knop = Button(text="verwijder", font_size=20, size_hint_y=0.4)
        knop.bind(on_press=self.test) #TODO
        grid.add_widget(knop)

        #zichtbaarheid
        grid.add_widget(Label(
                text="Zichtbaarheid",
                size_hint_max_y=0.2,
                font_size=20
                ))
        zichtbaar_grid = GridLayout(cols=2)
        zichtbaar_grid.add_widget(Label(text="naam:"))
        self.zichtbaar_grid = TextInput(multiline=False)
        zichtbaar_grid.add_widget(self.zichtbaar_grid)
        
        zichtbaar_grid.add_widget(Label(text="zichtbaar?"))
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

    
    def update_text_width(self, obj, _):
        '''
            Dit is noodzakelijk voor automatische multiline
        '''
        obj.text_size = (obj.width * .9, None)
    
    
    def test(self, _):
        gui.productscherm.history.update_chat_history(self.verwijder_naam.text)
        
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
    Window.maximize()
    gui = ServerGui()
    gui.run()