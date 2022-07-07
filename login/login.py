# import all the relevant classes
import os
from random import randint
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.video import Video
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db
from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy_garden.mapview import MapMarkerPopup

path = os.path.dirname(os.path.abspath(__file__))
Base = declarative_base()

class User(Base):
    __tablename__ = 'mysite_user'
    id = Column(Integer, primary_key =  True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    score = Column(Integer)

host = 'bruselas.ceisufro.cl'
port = '3306'

# class to call the popup function
class PopupWindow(Widget):
    def btn(self):
        popFun()
  
# class to build GUI for a popup window
class P(FloatLayout):
    pass
  
# function that displays the content
def popFun():
    show = P()
    window = Popup(title = "popup", content = show,
                   size_hint = (None, None), size = (300, 300))
    window.open()
  
# class to accept user info and validate it
class loginWindow(Screen):
    user = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def validate(self):

        def read_data():
            sqlEngine = db.create_engine('mysql+pymysql://python:python@'+ host +':' + port + '/proyecto_gpsrun', pool_recycle=3600)
            dbConnection = sqlEngine.connect()

            metadata = db.MetaData()
            data = db.Table('mysite_user', metadata, autoload=True, autoload_with=sqlEngine)
            query = db.select([data]) 
            ResultProxy = dbConnection.execute(query)
            ResultSet = ResultProxy.fetchall()
            dbConnection.close()

            return ResultSet

        data = read_data()
        matching_creds = False

        for i in range(len(data)):
            if self.user.text == data[i][1] and self.pwd.text == data[i][3]:
                matching_creds = True
                
        if matching_creds:
            # switching the current screen to display validation result
            sm.current = 'logdata'

            # reset TextInput widget
            self.user.text = ""
            self.pwd.text = ""
        else:
            popFun()

    def get_path(self):
        return path + "/intro.mp4"
            
# class to accept sign up info  
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):

        def read_data():
            sqlEngine = db.create_engine('mysql+pymysql://python:python@'+ host +':' + port+ '/proyecto_gpsrun', pool_recycle=3600)
            dbConnection = sqlEngine.connect()
            Session = sessionmaker(bind = sqlEngine)
            session = Session()
            result = session.query(User).all()
            dbConnection.close()

            return result

        data = read_data()

        if self.name2.text != "":

            isUserUnique = True

            for row in data:
                if self.name2.text == row.username:
                    isUserUnique = False
                    break

            if isUserUnique:

                tablename = 'mysite_user'
                sqlEngine = db.create_engine('mysql+pymysql://python:python@'+ host +':' + port + '/proyecto_gpsrun', pool_recycle=3600)
                dbConnection = sqlEngine.connect()
                new_user = User(username = self.name2.text,email = self.email.text,password = self.pwd.text,score = 0)

                Session = sessionmaker(bind = sqlEngine)
                session = Session()

                try:
                    session.add(new_user)
                    session.commit()
                except ValueError as vx:
                    print(vx)
                except Exception as ex:
                    print(ex)
                else:
                    print("Table %s created successfully.");
                finally:
                    dbConnection.close()

                sm.current = 'login'
                self.name2.text = ""
                self.email.text = ""
                self.pwd.text = ""
            else:
                
                popFun()
        else:
            
            # if values are empty or invalid show pop up
            popFun()
        
# class to display validation result
class logDataWindow(Screen):
    pass

class GpsRunMapView(MapView):
    pass

class FirstW(Screen):
    pass

class Tutorial(Screen):
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
        

class GameOver(Screen):
    pass

class Win(Screen):
    puntaje = StringProperty("5")
    

class WindowManager(ScreenManager):
    pass


# class for managing screens
class windowManager(ScreenManager):
    pass

# kv file
kv = Builder.load_file(path + '/login.kv')
sm = windowManager()

# adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(logDataWindow(name='logdata'))
sm.add_widget(FirstW(name='first'))
sm.add_widget(Tutorial(name='tutorial'))
sm.add_widget(GpsRun(name='gpsrun'))
sm.add_widget(GameOver(name='gameover'))
sm.add_widget(Win(name='win'))

# class that builds gui
class loginMain(App):
    def build(self):
        return sm
  
# driver function
if __name__=="__main__":
    loginMain().run()
