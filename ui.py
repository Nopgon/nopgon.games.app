from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import core

class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        box = BoxLayout(orientation="vertical", padding=30, spacing=15)

        box.add_widget(Label(text="NOPGON MINI GAME", font_size=32))
        self.input = TextInput(hint_text="아이디 입력", multiline=False)

        box.add_widget(self.input)

        btn = Button(text="로그인")
        btn.bind(on_press=self.do_login)
        box.add_widget(btn)

        self.add_widget(box)

    def do_login(self, btn):
        if self.input.text.strip():
            core.login(self.input.text.strip())
            self.manager.current = "menu"

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.box = BoxLayout(orientation="vertical", padding=20, spacing=10)
        self.add_widget(self.box)

    def on_enter(self):
        self.box.clear_widgets()
        self.box.add_widget(Label(text="게임 선택", font_size=28))

        for text, screen in [
            ("반응속도", "reaction"),
            ("두더지", "mole"),
            ("숫자 클릭", "number"),
            ("기억력", "memory"),
            ("랭킹", "ranking")
        ]:
            b = Button(text=text, height=60, size_hint_y=None)
            b.bind(on_press=lambda x, s=screen: setattr(self.manager, "current", s))
            self.box.add_widget(b)

        for diff in ["easy", "normal", "hard"]:
            b = Button(text=f"난이도: {diff}")
            b.bind(on_press=lambda x, d=diff: core.CURRENT_USER.update({"difficulty": d}))
            self.box.add_widget(b)

class RankingScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        box = BoxLayout(orientation="vertical", padding=20)
        box.add_widget(Label(text="전체 랭킹", font_size=28))

        for game in ["reaction", "mole", "number", "memory"]:
            box.add_widget(Label(text=f"[ {game} ]"))
            for i, (u, s) in enumerate(core.get_ranking(game)[:10], 1):
                box.add_widget(Label(text=f"{i}. {u} : {s}"))

        back = Button(text="메뉴로")
        back.bind(on_press=lambda x: setattr(self.manager, "current", "menu"))
        box.add_widget(back)

        self.add_widget(box)
