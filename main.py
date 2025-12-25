from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random, json, os
from core import reset_game

RANK_FILE = "ranking.json"

def save_score(game, score):
    data = []
    if os.path.exists(RANK_FILE):
        with open(RANK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    data.append({"game": game, "score": score})
    data = sorted(data, key=lambda x: x["score"], reverse=True)
    with open(RANK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

class BaseGame(Screen):
    def end_game(self, name):
        save_score(name, self.score)
        self.manager.current = "menu"

# 1. 반응속도
class ReactionGame(BaseGame):
    def on_enter(self):
        reset_game(self)
        self.clear_widgets()

        layout = BoxLayout(orientation="vertical")
        self.info = Label(text="초록색 되면 클릭")
        self.btn = Button(text="대기중", disabled=True)

        self.btn.bind(on_press=self.hit)

        layout.add_widget(self.info)
        layout.add_widget(self.btn)
        self.add_widget(layout)

        Clock.schedule_once(self.activate, random.uniform(1, 3))

    def activate(self, dt):
        self.btn.disabled = False
        self.btn.text = "클릭!"

    def hit(self, instance):
        self.score += 1
        self.end_game("반응속도")

# 2. 두더지
class MoleGame(BaseGame):
    def on_enter(self):
        reset_game(self)
        self.clear_widgets()

        layout = BoxLayout()
        self.btn = Button(text="두더지!")
        self.btn.bind(on_press=self.hit)
        layout.add_widget(self.btn)
        self.add_widget(layout)

        Clock.schedule_interval(self.tick, 1)

    def hit(self, instance):
        self.score += 1

    def tick(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            Clock.unschedule(self.tick)
            self.end_game("두더지")

# 3. 숫자 클릭
class NumberGame(BaseGame):
    def on_enter(self):
        reset_game(self)
        self.clear_widgets()

        self.target = random.randint(1, 5)
        layout = BoxLayout()

        for i in range(1, 6):
            b = Button(text=str(i))
            b.bind(on_press=self.click)
            layout.add_widget(b)

        self.add_widget(layout)

    def click(self, btn):
        if int(btn.text) == self.target:
            self.score += 1
        self.end_game("숫자")

# 4. 기억력
class MemoryGame(BaseGame):
    def on_enter(self):
        reset_game(self)
        self.clear_widgets()

        self.answer = random.randint(1, 3)
        self.label = Label(text=f"기억: {self.answer}")
        self.add_widget(self.label)

        Clock.schedule_once(self.hide, 2)

    def hide(self, dt):
        self.clear_widgets()
        layout = BoxLayout()
        for i in range(1, 4):
            b = Button(text=str(i))
            b.bind(on_press=self.select)
            layout.add_widget(b)
        self.add_widget(layout)

    def select(self, btn):
        if int(btn.text) == self.answer:
            self.score += 1
        self.end_game("기억력")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

class GameApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(ReactionGame(name="reaction"))
        sm.add_widget(MoleGame(name="mole"))
        sm.add_widget(NumberGame(name="number"))
        sm.add_widget(MemoryGame(name="memory"))

        # 임시 시작 화면 (첫 화면)
        sm.current = "reaction"
        return sm

if __name__ == "__main__":
    GameApp().run()

