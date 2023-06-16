from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.snackbar import BaseSnackbar
import random
from kivy.config import Config
from kivymd.color_definitions import colors
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
import json

# تحويل بيانات اللاعب إلى JSON وحفظها في الملف
# CustomSnackbar
class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")
    md_bg_color = 255 , 0 , 12
# Beginning to define the size of the application
width, height = Window.size # application body
class App(MDApp):
    def build(self):
        self.store = JsonStore('data.json')
        self.score = self.store.get('score')['value'] if self.store.exists('score') else 0
        self.progressbar = self.store.get('progressbar')['value'] if self.store.exists('progressbar') else 0
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Yellow"
        self.theme_cls.primary_hue = "800"
        self.title = "Mental Concept"
        kv = Builder.load_file("kivy.kv")
        return kv
    # Start Screen
    # def change_screen_splash(self):
    #     app = App.get_running_app()
    #     app.root.current = "Secondwindow"
    #     sound = SoundLoader.load('sound/startscreen.mp3')
    #     if sound:
    #         sound.play()
    def on_start(self):
        self.root.ids.score_lable.text = f"{self.score}"
        self.root.ids.progressbar.value = int(self.progressbar)
        # self.root.ids.score_image.source = path
    def home_screen(self):
        app = App.get_running_app()
        app.root.current = "Secondwindow"
    #Start counting
    def start_counting(self):
        if self.counter_tow >= 2 and self.counter_one >= 0.5 and self.root.ids.counter_label_three.text == "+" or self.root.ids.counter_label_three.text == "-":
            sound = SoundLoader.load('sound/startcount.wav')
            if sound:
                sound.play()
            app = App.get_running_app()
            app.root.current = "start_count"
            self.root.ids.number_label.text = " "
            Clock.schedule_once(lambda dt: self.count_numbers(), 1)
        else:
            Clock.schedule_once(lambda dt: self.show_warning())
            
    # Settings Counting
    def count_numbers(self):
        self.numbers = []
        self.numbers1 = []
        self.numbers2 = []
        self.sum2 = 0
        self.positive_numbers = list(range(10))
        self.negative_numbers = list(range(-1, -3, -1))
        for i in range(self.counter_tow):
            Clock.schedule_once(lambda dt, i=i: self.update_number(i), self.counter_one * i)
            Clock.schedule_once(lambda dt: self.sound(), self.counter_one * i)
            if (i+1) == self.counter_tow :
                Clock.schedule_once(lambda dt: self.change_screen(), self.counter_one * (i+1))

    #update Number $ Checksum
    # def check_sum(self, dt, sum):
    #     self.root.ids.number_label.text = f"{sum}"
    def update_number(self, i):
        global num1, num2
        positive_sum = sum(self.numbers1)
        negative_sum = sum(self.numbers2)
        
        if i % 2 == 0:
            num1 = random.choice(self.positive_numbers)
            self.numbers1.append(num1)
            self.root.ids.number_label.text = str(num1)
        else:
            num2 = random.choice(self.negative_numbers)
            self.numbers2.append(num2)
            self.root.ids.number_label.text = str(num2)
                
        self.number_o = f"{positive_sum} + ({negative_sum}) = {positive_sum + negative_sum}"
        print(self.number_o)
    # print(self.number_o)    
    def sound(self):
        sound = SoundLoader.load('sound/tic.wav')
        if sound:
            sound.play()
            
    def change_screen(self):
        sound = SoundLoader.load('sound/tac.wav')
        if sound:
            sound.play()
        app = App.get_running_app()
        app.root.current = "user_input"
        self.root.ids.result.text = ""
        # self.numbers.clear()
        
    # Check answer
    def result_number(self):
        if self.root.ids.result.text == "" :
            Clock.schedule_once(lambda dt: self.show_warning_number())
        else:
            self.number = int(self.root.ids.result.text)
            if self.number == self.number_o:
                if self.counter_tow >= 5:
                    self.progressbar += 100
                    self.score += 100
                    self.root.ids.score_lable.text = f"{self.score}"
                    self.root.ids.slogan.text = "keep a top"
                    self.root.ids.progressbar.value = self.progressbar
                    self.store.put('progressbar', value=self.progressbar)
                    self.store.put('score', value=self.score)
                else:
                    self.progressbar += 2
                    self.score += 2
                    self.root.ids.score_lable.text = f"{str(self.score)}"
                    self.root.ids.progressbar.value = self.progressbar
                    self.root.ids.slogan.text = "Keep going"
                    self.store.put('score', value=self.score)
                    self.store.put('progressbar', value=self.progressbar)
                    
                if self.progressbar and self.score >= 100 :
                    self.progress = 1
                    self.score = 1
                    self.store.put('score', value=self.progress)
                    self.store.put('score', value=self.score)
                    self.root.ids.progressbar.value = self.progress
                    self.root.ids.score_lable.text = f"{self.score}"
                    # self.root.ids.score_lable.text = f"{self.score}"
                    sound = SoundLoader.load('sound/extrabonus.wav')
                    if sound:
                        sound.play()
                    app = App.get_running_app()
                    app.root.current = "score_window"
                    path = "image/Golden2.png"
                    self.root.ids.score_image.source = path
                    self.root.ids.score_lable.text = f"{self.score}"
                    self.root.ids.lable_score.text = f"Score is {self.score}"
                    # self.store.put('image', source=path)

                # elif self.progressbar and self.score >= 200:
                #     sound = SoundLoader.load('sound/extrabonus.wav')
                #     if sound:
                #         sound.play()
                #     app = App.get_running_app()
                #     app.root.current = "score_window"
                #     self.root.ids.score_image.source = "image/Golden3.png"
                #     self.root.ids.progressbar.value = 1
                #     self.root.ids.score_lable.text = f"{self.score}"
                #     self.root.ids.lable_score.text = f"Score is {self.score}"
                else:
                    sound = SoundLoader.load('sound/success.mp3')
                    if sound:
                        sound.play()
                    app = App.get_running_app()
                    app.root.current = "happy_window"

            else:
                sound = SoundLoader.load('sound/los.wav')
                if sound:
                    sound.play()
                app = App.get_running_app()
                app.root.current = "sad"
                # if self.progressbar and self.score >= 0:
                #     self.progressbar -= 1
                #     self.score -= 1
                # else:
                #     pass
                # self.root.ids.score_lable.text = f"{str(self.score)}"
                # self.root.ids.progressbar.value = self.progressbar
                # self.root.ids.correct_answer.text = f"The correct answer is [{self.o_number}] !"
                # self.root.ids.correct_answer_information.text = f"result = [{self.o_number}]"
                # self.root.ids.correct_answer_label.text = f"{(self.number_o)}"
    # =====================================================================
    #                               application buttons
    # =====================================================================
    # Button 1
    counter_one = NumericProperty(0)
    def increment_counter_one(self):
        self.counter_one += 0.5
        self.update_counter_label_one()
    def decrement_counter_one(self):
        if self.counter_one >=1:
            self.counter_one -= 0.5
        else:
            exit
        self.update_counter_label_one()
    def update_counter_label_one(self):
        self.root.ids.counter_label_one.text = str(self.counter_one)

    # Button 2
    counter_tow = NumericProperty(0)
    def increment_counter_tow(self):
        self.counter_tow += 1
        self.update_counter_label_tow()
    def decrement_counter_tow(self):
        if self.counter_tow >=1:
            self.counter_tow -= 1
        else:
            exit
        self.update_counter_label_tow()
    def update_counter_label_tow(self):
        self.root.ids.counter_label_tow.text = str(self.counter_tow)

    #Button 3
    counter_three = StringProperty()
    def increment_counter_three(self):
        self.root.ids.counter_label_three.text = "+"
        # self.update_counter_label_three()
    def decrement_counter_three(self):
        self.root.ids.counter_label_three.text = "-"
    def update_counter_label_three(self):
        self.root.ids.counter_label_three.text = str(self.counter_three)

    # Score
    score = NumericProperty(0)

    # progressbar
    progressbar = NumericProperty(0)
    
# Warning Message
    def show_warning(self):
        snackbar = CustomSnackbar(
            text="Please complete the settings !",
            font_size=15,
            icon="information",
            snackbar_x="10dp",
            snackbar_y="8dp",
            radius = [25, 25, 10, 5],
            shadow_color="#F45050",
            shadow_softness= 0,
        )
        snackbar.size_hint_x = (
            Window.width - (snackbar.snackbar_x * 2)
        ) / Window.width
        snackbar.open()
    def show_warning_number(self):
        snackbar = CustomSnackbar(
            text="Please Enter Result !",
            font_size=15,
            icon="information",
            snackbar_x="10dp",
            snackbar_y="8dp",
            radius = [25, 25, 10, 5],
            shadow_color="#F45050",
            shadow_softness= 0,
        )
        snackbar.size_hint_x = (
            Window.width - (snackbar.snackbar_x * 2)
        ) / Window.width
        snackbar.open()

App().run()