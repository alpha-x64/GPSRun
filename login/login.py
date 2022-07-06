# import all the relevant classes
import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.video import Video
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import sqlalchemy as db

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
            sqlEngine = db.create_engine('mysql+pymysql://python:python@'+ host +':' + port + '/mysqldatabase', pool_recycle=3600)
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
        return path + "/intro.mp4
            
# class to accept sign up info  
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def signupbtn(self):

        def read_data():
            sqlEngine = db.create_engine('mysql+pymysql://python:python@'+ host +':' + port+ '/mysqldatabase', pool_recycle=3600)
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
                sqlEngine = db.create_engine('mysql+pymysql://python:python@'+ host +':' + port + '/mysqldatabase', pool_recycle=3600)
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

# class that builds gui
class loginMain(App):
    def build(self):
        return sm
  
# driver function
if __name__=="__main__":
    loginMain().run()
