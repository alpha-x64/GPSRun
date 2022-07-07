import os
from random import randint
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy_garden.mapview import MapMarkerPopup

path = os.path.dirname(os.path.abspath(__file__))


class GpsRunMapView(MapView):
    pass

class GpsRun(Screen):

    partida = 0
    lugar = "gim"
    riddle = StringProperty()
    cont = StringProperty("15")

    getting_objectives_timer = None
    objs = []

    mapvw = GpsRunMapView()
    app_lat = -38.746639244298464
    app_lon = -72.61560718899622
    app_zoom = 18


    def timer(self, dt):
        self.cont = str(int(self.cont)-1)
        if self.cont == "0":
            self.time.cancel()
            self.parent.current = 'gameover'

    def switch(self, *args):
        self.parent.current = 'gameover'
        self.time.cancel()

    def on_enter(self, *args):
        self.partida = randint(1,3)
        print(self.partida)

        if self.partida == 1:
            self.lugar = "gim"
            self.riddle = "Hay que cruzar la calle y termina con o"
        elif self.partida == 2:
            self.lugar = "cas"
            self.riddle = "Tiene dos pisos y en el primero se puede comprar"
        elif self.partida == 3:
            self.lugar = "bib"
            self.riddle = "Hay que usar tarjeta para entrar"
        
        print(self.lugar)

        mapvw = GpsRunMapView()
        mapvw.lat = self.app_lat
        mapvw.lon = self.app_lon
        mapvw.zoom = self.app_zoom
        mapvw.snap_to_zoom = False
        mapvw.set_zoom_at(mapvw.zoom, mapvw.x, mapvw.y)
        mapvw.center_on(self.app_lat, self.app_lon)
        self.start_getting_objectives_in_fov()
        self.mapvw = mapvw

        layout = self.children[0].tab_list[0]
        layout.add_widget(self.mapvw)

        self.cont = "15"
        self.time = Clock.schedule_interval(self.timer, 1)

    def start_getting_objectives_in_fov(self):

        try:
            self.getting_objectives_timer.cancel()
        except:
            pass

        self.getting_objectives_timer = Clock.schedule_once(self.get_objectives_in_fov, 1)

    def get_objectives_in_fov(self, *args):
        bib = ObjectiveMarker(lat=-38.74838393048031, lon=-72.6175605760204, loc="bib")
        cas = ObjectiveMarker(lat=-38.74697557147709, lon=-72.6164032028276, loc="cas")
        gim = ObjectiveMarker(lat=-38.7478060516660, lon=-72.6180152104433, loc="gim")
        self.objs.append(bib)
        self.objs.append(cas)
        self.objs.append(gim)
        for o in self.objs:
            o.set_app(self)
            self.mapvw.add_marker(o)

    def chosen_loc(self, loc):
        print(loc + " activado")
        if (loc == self.lugar):
            print("ganaste!!")
            self.parent.current = 'win'
            # agrega puntaje y blahblahbasdasf
    
    def on_leave(self, *args):
        self.time.cancel()
        self.objs.clear()


class ObjectiveMarker(MapMarkerPopup):

    app = GpsRun()

    source = path + "/imagenes/marker.png"
    loc = StringProperty()

    def set_app(self, app):
        self.app = app

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_loc(self):
        return self.loc

    def on_release(self ,*args):
        return self.app.chosen_loc(self.loc)

    def on_press(self):
        pass


class Tutorial(Screen):
    pass

class FirstW(Screen):
    pass

class GameOver(Screen):
    pass

class Win(Screen):
    puntaje = StringProperty("5")

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file(path + '/game.kv')
sm = ScreenManager()

sm.add_widget(FirstW(name='first'))
sm.add_widget(GpsRun(name='gpsrun'))
sm.add_widget(GameOver(name='gameover'))
sm.add_widget(Win(name='win'))
sm.add_widget(Tutorial(name='tutorial'))

class GRApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    GRApp().run()
