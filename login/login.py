# import all the relevant classes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.video import Video
from sqlalchemy import create_engine
import pymysql
import pandas as pd

dataFilePath = 'login/login.csv'
host = 'bruselas.ceisufro.cl'
netPort = '3306'

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

    def read_data():
        sqlEngine = create_engine('mysql+pymysql://python:python@'+ host +':' + netPort, pool_recycle=3600)
        dbConnection = sqlEngine.connect()
        frame = pd.read_sql("select * from mysqldatabase.mysite_user", dbConnection);
        pd.set_option('display.expand_frame_repr', False)

        dbConnection.close()

        return frame

    users = read_data()
    
    def validate(self):

        # validating if the email already exists 
        if self.user.text not in self.users['username'].unique():
            popFun()
        else:

            matching_creds  = (len(self.users[(self.users['username'] == self.user.text) & (self.users['password'].astype('str') == self.pwd.text)]) > 0)

            if matching_creds:
                # switching the current screen to display validation result
                sm.current = 'logdata'
    
                # reset TextInput widget
                self.user.text = ""
                self.pwd.text = ""
            else:
                popFun()  
  
# class to accept sign up info  
class signupWindow(Screen):
    name2 = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)

    def read_data():
        sqlEngine = create_engine('mysql+pymysql://python:python@'+ host +':' + netPort, pool_recycle=3600)
        dbConnection = sqlEngine.connect()
        frame = pd.read_sql("select * from mysqldatabase.mysite_user", dbConnection);
        pd.set_option('display.expand_frame_repr', False)
        
        dbConnection.close()

        return frame
    
    users = read_data()

    def signupbtn(self):
  
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text, 0]],
                            columns = ['username', 'email', 'password','score'])
        
        if self.name2.text != "":

            

            if self.name2.text not in self.users['username'].unique():

                tablename = 'mysite_user'

                # if name2 does not exist already then append to the csv file
                # change current screen to log in the user now 

                sqlEngine = create_engine('mysql+pymysql://python:python@'+ host +':' + netPort + '/mysqldatabase', pool_recycle=3600)
                dbConnection = sqlEngine.connect()

                try:
                    user.to_sql(tablename, con = sqlEngine, if_exists = 'append', index = False)
                except ValueError as vx:
                    print(vx)
                except Exception as ex:
                    print(ex)
                else:
                    print("Table %s created successfully."%tablename);
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
kv = Builder.load_file('login.kv')
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