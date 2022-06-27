from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy_garden.mapview import MapView


class FirstW(Screen):
    pass

class GpsW(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('gps.kv')
sm = ScreenManager()

sm.add_widget(FirstW(name='first'))
sm.add_widget(GpsW(name='gps'))

class GpsApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    GpsApp().run()