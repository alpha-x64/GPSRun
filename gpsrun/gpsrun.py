from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy_garden.mapview import MapView
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty
from plyer import gps


class FirstW(Screen):
    pass

class GpsRun(Screen):

    app_lat = -38.74719680168039
    app_lon = -72.6168759153446

    cont = StringProperty("180")

    def timer(self, dt):
        self.cont = str(int(self.cont)-1)
        if self.cont == "0":
            self.obj.cancel()

    def switch(self, *args):
        self.parent.current = 'gameover'

    def on_enter(self, *args):
        Clock.schedule_once(self.switch, 180)
        self.obj = Clock.schedule_interval(self.timer, 1)





class GameOver(Screen):
    pass

class WinW(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('game.kv')
sm = ScreenManager()

sm.add_widget(FirstW(name='first'))
sm.add_widget(GpsRun(name='gpsrun'))
sm.add_widget(GameOver(name='gameover'))
sm.add_widget(WinW(name='win'))

class GRApp(App):
    def build(self):
        return sm
    

    

if __name__ == "__main__":
    GRApp().run()