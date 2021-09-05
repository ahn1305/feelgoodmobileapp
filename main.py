__version__ = "1.10.1"

# import necessary

from os import uname
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager,Screen
import json, glob, random
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior



# connecting the kv file to main.py
Builder.load_file('design.kv')

# empty class 
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def forgot_password(self):
        self.manager.current = "forgot_password"
    
    def login(self,luname,lpword):
        with open("users.json") as file:
            users = json.load(file)

        if luname in users and users[luname]['password'] == lpword:
            self.manager.current = "login_screen_success"
            self.ids.lusername.text = ""
            self.ids.lpassword.text = ""
           
        else:
            self.ids.login_wrong.text = "Wrong username or password"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def sign_in(self):
        self.manager.current = "login_screen"
    def add_user(self,uname,pword,s_code):
        with open ("users.json") as file:
            users = json.load(file)

                
        if self.ids.username.text == "" or self.ids.password.text == "" or self.ids.code.text == "":
            self.ids.empty_signup.text = "Enter valid data"
        elif self.ids.username.text in users:
            self.ids.empty_signup.text = "Username already exists"
        elif self.ids.code.text in [users[i]['code'] for i in users.keys()]:
            self.ids.empty_signup.text = "Try a different code please !!"
        elif self.ids.code.text.isalnum() != True:
            self.ids.empty_signup.text = "use only alphabets and numbers"
        else:
            users[uname] = {'username': uname, 
                            "password": pword,
                            "code": s_code,
                            "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                            } 
            
            with open("users.json","w") as file:
                json.dump(users, file)
        
            self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def go_to_login(self):

        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def ask_question(self):
        text = "How do you feel?"
        return text
   
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        self.ids.feeling.text = ""
    
    def get_quote(self,feel):
        feel = feel.lower()
        available_feelings =  glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior,HoverBehavior, Image):
    pass

class ForgotPassword(Screen):
    def get_pwd(self,fname,s_code):
        usr = fname
        cod = s_code

        with open("users.json") as file:
            users = json.load(file)
        
        if usr in users and users[usr]['code'] == s_code:
            self.ids.f_text.text = "your password is: "+str(users[usr]['password'])
        else:
            self.ids.f_text.text = "Enter some data or enter valid data"

# initializing root widget here
class MainApp(App):
    def __init__(self,*args, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.previous_screen = "" 
    def build(self):
        return RootWidget()

# calling the class

if __name__ == "__main__":
    MainApp().run()