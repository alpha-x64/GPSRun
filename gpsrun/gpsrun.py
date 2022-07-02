from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.properties import StringProperty
from objective_marker import ObjectiveMarker
from player_marker import PlayerMarker
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class FirstW(Screen):
    pass

class GpsRunMapView(MapView):

    player = PlayerMarker()
    objs = []

    def start_getting_objectives_in_fov(self):
        obj1 = ObjectiveMarker(lat=-38.74583646869399, lon=-72.61606852890573)
        obj2 = ObjectiveMarker(lat=-38.74615999999985, lon=-72.61512999999985)
        self.objs.append(obj1)
        self.objs.append(obj2)
        for o in self.objs:
            self.add_widget(o)
        
    def add_player(self):
        player = PlayerMarker()
        self.player = player
        self.add_widget(self.player)
        Clock.schedule_interval(self.move_player, 0.5)

    def move_player(self,*args):
        self.remove_widget(self.player)
        self.player.set_lat()
        self.player.set_lon()
        self.add_widget(self.player)

        for o in self.objs:
            if (self.is_player_in_objective(o)):
                print("Objetivo encontrado cerca")

    def is_player_in_objective(self, obj):
        lat = self.player.get_lat()
        lon = self.player.get_lon()
        r = self.player.radius
        
        point = Point(obj.get_lat(),obj.get_lon())
        polygon = Polygon([(lat-r,lon),(lat,lon+r),(lat+r,lon),(lat,lon-r)])

        return polygon.contains(point)

class GpsRun(Screen):

    app_lat = -38.746639244298464
    app_lon = -72.61560718899622

    cont = StringProperty("180")

    def timer(self, dt):
        self.cont = str(int(self.cont)-1)
        if self.cont == "0":
            self.obj.cancel()

    def switch(self, *args):
        self.parent.current = 'gameover'

    def add_objective(self, objective):

        self.add_widget(objective)

        pass

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