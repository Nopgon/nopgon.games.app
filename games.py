from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random
import core

class BaseGame(Screen):
    def start(self, game_name):
        self.game_name = game_name
        self.score = 0
        self.time_left = core.TIME_BY_DIFF[core.CURRENT_USER["difficulty"]]
        Clock.schedule_interval(self.timer, 1)

    def timer(self, dt):
        self.time_left -= 1
        self.info.text = f"점수: {self.score}   남은시간: {self.time_left}"
        if self.time_left <= 0:
            Clock.unschedule(self.timer)
            core.save_score(self.game_name, self.score)
            self.manager.current = "menu"

class ReactionGame(BaseGame):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical")
        self.info = Label()
        self.btn = Button(text="대기중", disabled=True)
        box.add_widget(self.info)
        box.add_widget(self.btn)
        self.add_widget(box)

        self.start("reaction")
        Clock.schedule_once(self.ready, random.uniform(1, 3))

    def ready(self, dt):
        self.btn.text = "클릭"
        self.btn.disabled = False
        self.btn.bind(on_press=self.hit)

    def hit(self, btn):
        self.score += 1
        self.btn.disabled = True

class MoleGame(BaseGame):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout()
        self.info = Label()
        self.btn = Button(text="두더지")
        self.btn.bind(on_press=self.hit)
        box.add_widget(self.info)
        box.add_widget(self.btn)
        self.add_widget(box)
        self.start("mole")

    def hit(self, btn):
        self.score += 1

class NumberGame(BaseGame):
    def on_enter(self):
        self.clear_widgets()
        self.target = random.randint(1, 5)
        box = BoxLayout()
        self.info = Label()
        box.add_widget(self.info)
        for i in range(1, 6):
            b = Button(text=str(i))
            b.bind(on_press=self.click)
            box.add_widget(b)
        self.add_widget(box)
        self.start("number")

    def click(self, btn):
        if int(btn.text) == self.target:
            self.score += 1
            self.target = random.randint(1, 5)

class MemoryGame(BaseGame):
    def on_enter(self):
        self.clear_widgets()
        self.answer = random.randint(1, 3)
        self.info = Label(text=str(self.answer))
        self.add_widget(self.info)
        self.start("memory")
        Clock.schedule_once(self.hide, 2)

    def hide(self, dt):
        self.clear_widgets()
        box = BoxLayout()
        self.info = Label()
        box.add_widget(self.info)
        for i in range(1, 4):
            b = Button(text=str(i))
            b.bind(on_press=self.pick)
            box.add_widget(b)
        self.add_widget(box)

    def pick(self, btn):
        if int(btn.text) == self.answer:
            self.score += 1
        self.answer = random.randint(1, 3)
