from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.mapview import MapView

class MapViewExample(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Gps(MDApp):
    def build(self):
        return MapViewExample()

if __name__ == '__main__':
    Gps().run()