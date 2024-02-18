import json
import hashlib
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
import requests
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.relativelayout import MDRelativeLayout
import sqlite3
from kivy.core.text import LabelBase
from kivymd.toast import toast
Window.size = (520, 900)
API = '6c39b074-59ea-4ce3-8924-c1b26f5e9137'

def md5sum(value):
    return hashlib.md5(value.encode()).hexdigest()

with sqlite3.connect('userbase.db') as user:
    db = user.cursor()
    table = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        login TEXT, 
        password TEXT,
        name TEXT,
        email TEXT
    )
    """
    db.executescript(table)

with sqlite3.connect('cursbase.db') as user:
    db = user.cursor()
    table = """
    CREATE TABLE IF NOT EXISTS curs(
        id PRIMARY KEY,
        name TEXT,
        desc TEXT,
        star TEXT,
        owner TEXT
    )
    """
    db.executescript(table)

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
class Content(MDBoxLayout):
    pass

class Sckill(MDApp):
    dialog = None
    def screen(self, screen_name):
        self.root.current = screen_name

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.material_style = "M3"
        return Builder.load_file("kivy.kv")

    def registration(self):
        login = self.root.ids.login_registration.text
        password = self.root.ids.password_registration.text
        name = self.root.ids.name_registration.text
        gmail = self.root.ids.gmail_registration.text
        try:
            db = sqlite3.connect("userbase.db")
            cursor = db.cursor()

            db.create_function("md5", 1, md5sum)

            cursor.execute("SELECT login FROM users WHERE login = ?", [login])

            if cursor.fetchone() is None:
                values = [login, password, name, gmail]
                cursor.execute("INSERT INTO users(login, password, name, email) VALUES(?,md5(?),?,?)", values)
                toast("Aкаунт создан")
                self.screen('sig_in')
                db.commit()
            else:
                toast("Tакой логин уже есть")

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            db.close()

    def sig_in(self):
        login = self.root.ids.login_sigin.text
        password = self.root.ids.password_sigin.text
        try:
            db = sqlite3.connect("userbase.db")
            cursor = db.cursor()
            db.create_function("md5", 1, md5sum)
            cursor.execute("SELECT login FROM users WHERE login = ?", [login])
            if cursor.fetchone() is None:
                toast("Такого логина не существует")
            else:
                cursor.execute("SELECT login FROM users WHERE login = ? AND password = md5(?)", [login, password])
                if cursor.fetchone() is None:
                    toast("Пороль не верный")
                else:
                    toast("Вы вошли")
                    self.screen("main_screen")
        except sqlite3.Error as e:
            print('Error, e')
        finally:
            cursor.close()
            db.close()

    def settings_profile(self, what):
        if what == "name":
            what_text = "Новое имя"
            what_label = "Изменения имени:"
            if not self.dialog:
                self.dialog = MDDialog(
                    title=f"{what_label}",
                    type="custom",
                    content_cls=Content(),
                    # MDTextField(
                    #     id=("text_modified"),
                    #     hint_text=f"{what_text}"
                    # ),
                    buttons=[
                        MDFlatButton(
                            text="Отмена",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=lambda x: self.dialog_close("dialog"),
                        ),
                        MDFlatButton(
                            text="Изменить",
                            theme_text_color="Custom",
                            text_color=self.theme_cls.primary_color,
                            on_release=lambda x: self.settings_profile_output(f"{what}"),
                        ),
                    ],
                )
            self.dialog.open()

    def settings_profile_output(self, what):

        try:
            db = sqlite3.connect("userbase.db")
            cursor = db.cursor()

            db.create_function("md5", 1, md5sum)

            cursor.execute("SELECT login FROM users WHERE login = ?", [login])

            if cursor.fetchone() is None:
                values = [login, password, name, gmail]
                cursor.execute("INSERT INTO users(login, password, name, email) VALUES(?,?,?,?)", values)
                toast("Aкаунт создан")
                self.screen('sig_in')
                db.commit()
            else:
                toast("Tакой логин уже есть")

        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            db.close()

    def dialog_close(self, a):
        eval(f"self.{a}.dismiss()")

    def create_curs(self):
        owner = self.root.ids.login_sigin.text
        name = self.root.ids.name_curs_create.text
        desc = self.root.ids.desc_curs_create.text
        try:
            db = sqlite3.connect("cursbase.db")
            cursor = db.cursor()
            values = [name, desc, owner]
            cursor.execute("INSERT INTO users(name, desc, owner) VALUES(?,,?,?)", values)
            three_results = cursor.fetchall()
            print(three_results)
        except sqlite3.Error as e:
            print('Error, e')
        finally:
            cursor.close()
            db.close()

    def search(self):
        search_line = self.root.ids.search_line.text
        try:
            db = sqlite3.connect("cursbase.db")
            cursor = db.cursor()
            cursor.execute(f'''SELECT * FROM curs LIKE '%{search_line}%';''')
            three_results = cursor.fetchall()
            print(three_results)
        except sqlite3.Error as e:
            print('Error, e')
        finally:
            cursor.close()
            db.close()
Sckill().run()