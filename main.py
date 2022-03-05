import kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from GameMode import GameMode
from kivy.core.window import Window
from genetic_optimization import GeneticArea
import numpy as np

kivy.require('1.9.0')


class DrawTool(RelativeLayout):

    def __init__(self):
        super().__init__()
        self.change_text_delegate = None
        Clock.schedule_interval(self.main_loop, 0.001)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.game_modes = []
        self.generation = 0
        self.collection_lenght = 40
        self.area = GeneticArea(self.collection_lenght)
        self.first_loop = True
        for _ in range(self.collection_lenght):
            self.game_modes.append(GameMode(self))
        self.pause = False

    def main_loop(self, dt):
        if self.pause:
            return
        print("start main loop")
        is_end_game = True
        for game_mode in self.game_modes:
            if not game_mode.is_loose:
                is_end_game = False
                break
        if is_end_game:
            self.game_over()
            return False
        if self.first_loop:
            self.change_text_delegate(self.generation)
            for game_mode in self.game_modes:
                game_mode.main_loop(dt)
            self.first_loop = False
            return
        for i, game_mode in enumerate(self.game_modes):
            if game_mode.is_loose:
                continue
            x = game_mode.get_vector_to_learn()
            y = self.area.make_decision(i, x.reshape((1, 4)))
            print(i, x, float(y[0][0]))
            if y > 0.8:
                game_mode.bird.jump()
            game_mode.main_loop(dt)
            self.area.individals[i].score = game_mode.score

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print("key pressed")
        if keycode[1] == 'spacebar':
            self.game_modes[0].bird.jump()
        if keycode[1] == "esc":
            exit()
        if keycode[1] == "tab":
            self.pause = not self.pause
        if keycode[1] == "shift":
            self.restart()

    def game_over(self):
        game_over = RelativeLayout(pos_hint={"x": -0.1, "top": 1.2})
        game_over.add_widget(Label(text='GameOver'))
        self.add_widget(game_over)
        self.first_loop = True
        self.restart()

    def restart(self):
        self.clear_widgets()
        self.generation += 1
        self.change_text_delegate(self.generation)
        self.pause = False
        self.area.make_select()
        Clock.schedule_interval(self.main_loop, 0.005)
        self.game_modes.clear()
        for _ in range(self.collection_lenght):
            self.game_modes.append(GameMode(self))

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        print(touch.pos)


class ScoreLabel(Label):

    def __init__(self):
        super().__init__()

    def change_text(self, value):
        self.text = "GEN: " + str(value)


class PicturesApp(App):

    def build(self):
        game_field = DrawTool()
        layout = BoxLayout(size_hint=(1, None), height=50)
        score_label = ScoreLabel()
        layout.add_widget(score_label)
        game_field.change_text_delegate = score_label.change_text
        root = BoxLayout(orientation='vertical')
        root.add_widget(layout)
        root.add_widget(game_field)
        self.root = root
        return root


if __name__ == '__main__':
    PicturesApp().run()