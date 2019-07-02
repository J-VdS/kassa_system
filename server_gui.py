import kivy
from kivy.app import App
#achtergrond
from kivy.graphics import Color, Rectangle

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window
from kivy.config import Config

#fullscreen
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'fullscreen', 'auto')

kivy.require("1.10.1")

#schermen
class HoofdScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
       
        '''
        #achtergrondkleur
        with self.canvas.before:
            #rgba
            Color(1, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
       '''
        
        #navigatiebar
        self.navbar = NavigatieBar()
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.hoofdbar = HoofdBar()
        self.add_widget(self.hoofdbar)
        
        
    def _update_rect(self, instance, value):
        ''' 
            achtergrondkleur
        '''
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
class ProductScherm(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
       
        '''
        #achtergrondkleur
        with self.canvas.before:
            #rgba
            Color(1, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)
       '''
        
        #navigatiebar
        self.navbar = NavigatieBar(huidig="product")
        self.add_widget(self.navbar)
        
        #hoofdscherm
        self.hoofdbar = ProductBar()
        self.add_widget(self.hoofdbar)
        
        
    def _update_rect(self, instance, value):
        ''' 
            achtergrondkleur
        '''
        self.rect.pos = instance.pos
        self.rect.size = instance.size

#bars
class NavigatieBar(BoxLayout):
    def __init__(self, huidig="hoofd", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 5
        self.size_hint = (1.0, 0.2)
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
        
        
    def switch(self, instance):
        print(instance.text)
        gui.screen_manager.current = instance.text  
        
        
class HoofdBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="links"))
        self.add_widget(Label(text="rechts"))


class ProductBar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="boven"))
        self.add_widget(Label(text="onder"))

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