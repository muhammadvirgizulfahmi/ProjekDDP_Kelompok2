from kivy import *
from kivy.app import *
from kivy.uix.screenmanager import *
from kivy.uix.boxlayout import *
from kivy.uix.label import *
from kivy.uix.textinput import *
from kivy.uix.button import *
from kivy.uix.popup import *
from sqlite3 import *

class navigasi(Screen):
    def __init__(self, **kwargs):
        super(navigasi, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=10)
        
        registration_button = Button(text="Registration", font_size=18, on_press=self.go_to_registration)
        login_button = Button(text="Login", font_size=18, on_press=self.go_to_login)
        layout.add_widget(registration_button)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def go_to_registration(self, instance):
        self.manager.current = 'registration'

    def go_to_login(self, instance):
        self.manager.current = 'login'

class register(Screen):
    def __init__(self, **kwargs):
        super(register, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=30, spacing=10)

        head_label = Label(text="Python User Registration app", font_size=26, bold=True, height=40)

        user_label = Label(text="UserID:", font_size=18)
        self.user_input = TextInput(multiline=False, font_size=18)
        name_label = Label(text="Name:", font_size=18)
        self.name_input = TextInput(multiline=False, font_size=18)
        email_label = Label(text="Email:", font_size=18)
        self.email_input = TextInput(multiline=False, font_size=18)
        password_label = Label(text="Password:", font_size=18)
        self.password_input = TextInput(multiline=False, font_size=18, password=True)
        confirm_label = Label(text="Confirm Password:", font_size=18)
        self.confirm_input = TextInput(multiline=False, font_size=18, password=True)
        submit_button = Button(text="Register", font_size=18, on_press=self.data_register)
        login_button = Button(text="Have account? Login here", font_size=18, on_press=self.go_to_login)

        layout.add_widget(head_label)
        layout.add_widget(user_label)
        layout.add_widget(self.user_input)
        layout.add_widget(name_label)
        layout.add_widget(self.name_input)
        layout.add_widget(email_label)
        layout.add_widget(self.email_input)
        layout.add_widget(password_label)
        layout.add_widget(self.password_input)
        layout.add_widget(confirm_label)
        layout.add_widget(self.confirm_input)
        layout.add_widget(submit_button)
        layout.add_widget(login_button)
        self.add_widget(layout)
    
    def data_register(self, instance):
        user = self.user_input.text
        name = self.name_input.text
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_input.text

        if user.strip() == "" or name.strip() == "" or email.strip() == "" or password.strip() == "" or confirm_password.strip() == "":
            message = "Please fill in all fields"
        elif password != confirm_password:
            message = "Password don't match"
        else:
            global conn, cursor
            conn = connect("db_member.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (user, name, email, password) VALUES (?, ?, ?, ?)", (user, name, email, password))
            conn.commit()
            message = "Registration Successful!"
            conn.close()
        popup = Popup(title="Registration Status", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def go_to_login(self, instance):
        self.manager.current = 'login'

class login(Screen):
    def __init__(self, **kwargs):
        super(login, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=30, spacing=10)

        head_label = Label(text="Python User Login interface", font_size=26, bold=True, height=40)
        user_label = Label(text="UserID:", font_size=18)
        self.user_input = TextInput(multiline=False, font_size=18)
        password_label = Label(text="Password:", font_size=18)
        self.password_input = TextInput(multiline=False, font_size=18, password=True)
        submit_button = Button(text="Login", font_size=18, on_press=self.data_login)
        register_button = Button(text="Don't have account? Register here", font_size=18, on_press=self.go_to_registration)

        layout.add_widget(head_label)
        layout.add_widget(user_label)
        layout.add_widget(self.user_input)
        layout.add_widget(password_label)
        layout.add_widget(self.password_input)
        layout.add_widget(submit_button)
        layout.add_widget(register_button)
        self.add_widget(layout)
    
    def data_login(self, instance):
        user = self.user_input.text
        password = self.password_input.text

        if password.strip() == "" or user.strip() == "":
            message = "Please fill in all fields"
        else:
            conn = connect("db_member.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user=? AND password=?", (user, password))
            existing_user = cursor.fetchone()
            if existing_user:
                message = "Login Successful!"
            else:
                message = "Invalid login credentials"
            conn.close()
        popup = Popup(title="Login Status", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def go_to_registration(self, instance):
        self.manager.current = 'registration'

class main(App):
    def build(self):
        self.title = "Register and Login form"
        screen_manager = ScreenManager()
        navigation_screen = navigasi(name='navigation')
        screen_manager.add_widget(navigation_screen)
        screen_manager.add_widget(login(name='login'))
        screen_manager.add_widget(register(name='registration'))
        
        screen_manager.current = 'navigation'
        return screen_manager

if __name__ == "__main__":
    main().run()