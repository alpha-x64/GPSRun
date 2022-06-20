# import all the relevant classes
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import pandas as pd

dataFilePath = 'login/login.csv'

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

    users=pd.read_csv(dataFilePath)

    def validate(self):
  
        # validating if the email already exists 
        if self.user.text not in users['Name'].unique():
            popFun()
        else:

            matching_creds  = (len(users[(users['Name'] == self.user.text) & (users['Password'].astype('str') == self.pwd.text)]) > 0)

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
    def signupbtn(self):
  
        # creating a DataFrame of the info
        user = pd.DataFrame([[self.name2.text, self.email.text, self.pwd.text]],
                            columns = ['Name', 'Email', 'Password'])
        
        if self.name2.text != "":

            users=pd.read_csv(dataFilePath)

            if self.name2.text not in users['Name'].unique():
                
                # if name2 does not exist already then append to the csv file
                # change current screen to log in the user now 
                user.to_csv(dataFilePath, mode = 'a', header = False, index = False)
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
  
# reading all the data stored
users=pd.read_csv(dataFilePath)
  
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