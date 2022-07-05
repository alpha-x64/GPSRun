from turtle import pos
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
#from objective_marker import ObjectiveMarker
#from player_marker import PlayerMarker
#from shapely.geometry import Point
#from shapely.geometry.polygon import Polygon


class FirstW(Screen):
    pass

class Tutorial(Screen):
    pass

#class GpsRunMapView(MapView):

    #player = PlayerMarker()
    #objs = []

    #def start_getting_objectives_in_fov(self):
    #    obj1 = ObjectiveMarker(lat=-38.74583646869393, lon=-72.61606852890574)
    #    obj2 = ObjectiveMarker(lat=-38.74615999999981, lon=-72.61512999999981)
    #    self.objs.append(obj1)
    #    self.objs.append(obj2)
    #    for o in self.objs:
    #        self.add_widget(o)
        
    #def add_player(self):
    #    player = PlayerMarker()
    #    self.player = player
    #    self.add_widget(self.player)
    #    Clock.schedule_interval(self.move_player, 0.5)

    #def move_player(self,*args):
    #    self.remove_widget(self.player)
    #    self.player.set_lat()
    #    self.player.set_lon()
    #    self.add_widget(self.player)

    #    for o in self.objs:
    #        if (self.is_player_in_objective(o)):
    #            print("Objetivo encontrado cerca")

    #def is_player_in_objective(self, obj):
    #    lat = self.player.get_lat()
    #    lon = self.player.get_lon()
    #    r = self.player.radius
        
    #    point = Point(obj.get_lat(),obj.get_lon())
    #    polygon = Polygon([(lat-r,lon),(lat,lon+r),(lat+r,lon),(lat,lon-r)])

    #    return polygon.contains(point)

class GpsRun(Screen):

    app_lat = NumericProperty(-38.74719680168039)
    app_lon = NumericProperty(-72.6168759153446)

    cont = StringProperty("10")

    def timer(self, dt):
        self.cont = str(int(self.cont)-1)
        if self.cont == "0":
            self.time.cancel()
            self.parent.current = 'gameover'
  

    #def add_objective(self, objective):
    #     self.add_widget(objective)
    #         pass
    
 
    def on_enter(self, *args):
        self.cont = "10"
        self.time = Clock.schedule_interval(self.timer, 1)

    def on_leave(self, *args):
        self.time.cancel()
        
    

class GameOver(Screen):
    pass

class Win(Screen):
    puntaje = StringProperty("5")
    

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('game.kv')
sm = ScreenManager()

sm.add_widget(FirstW(name='first'))
sm.add_widget(Tutorial(name='tutorial'))
sm.add_widget(GpsRun(name='gpsrun'))
sm.add_widget(GameOver(name='gameover'))
sm.add_widget(Win(name='win'))

class GRApp(App):
    def build(self):
        return sm
    
if __name__ == "__main__":
    GRApp().run()