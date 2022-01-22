import kivy
kivy.require('1.9.0')

from kivy.config import Config

from random import randint
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from Bird import BirdWidget
from Pipe import PipWidget

from kivy.lang import Builder

from kivy.core.window import Window


class Picture(Scatter):


    source = StringProperty(None)


class DrawTool(RelativeLayout):

    def __init__(self):
        super().__init__()
        self.score = 0
        self.bird = BirdWidget()
        self.add_widget(self.bird)
        self.bird.pos = (200, 300)
        self.pipes = []
        self.change_text_delegate = None
        self.pause = False
        self.x_speed_multiplier = 2
        self.horizon_shift = 0
        Clock.schedule_interval(self.main_loop, 0.005)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.x_pos_pipe_creation = 1200

    def main_loop(self, dt):
        if self.pause:
            return
        print("start main loop")
        if not self.bird.is_alive:
            self.game_over()
            return False
        self.score += 1
        self.change_text_delegate(int(self.score // 100))
        self.create_pipe(dt)

        if self.score > 1000:
            self.x_speed_multiplier += 1
        print(dt)
        old_pos = self.bird.pos
        print(self.bird.is_alive)
        print(old_pos)
        if old_pos[1] >= 0:
            new_pos = (old_pos[0], old_pos[1] + self.bird.calculate_current_bird_velocity())
            self.bird.move(new_pos)
        for pipe in self.pipes:
            old_pos = pipe.pos
            pipe.pos = (old_pos[0] - 1 * self.x_speed_multiplier, old_pos[1])
        if len(self.pipes) == 0:
            return
        first_pipe = self.pipes[0]
        if first_pipe.pos[0] < -100:
            self.remove_widget(first_pipe)
            self.pipes.remove(first_pipe)
        self.check_colision()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print("key pressed")
        if keycode[1] == 'spacebar':
            self.bird.jump()
        if keycode[1] == "esc":
            exit()
        if keycode[1] == "tab":
            self.pause = not self.pause

    def create_pipe(self, dt):
        if len(self.pipes) == 0:
            height_shift = randint(-100, 100)
            new_pipe = PipWidget(height_shift)
            self.add_widget(new_pipe)
            new_pipe.pos = self.x_pos_pipe_creation, -100 + height_shift
            self.pipes.append(new_pipe)
            self.horizon_shift = randint(0, 300)
            return
        last_pipe = self.pipes[-1]
        if abs(last_pipe.pos[0] - self.x_pos_pipe_creation) > 150 + self.horizon_shift:
            height_shift = randint(-100, 100)
            new_pipe = PipWidget(height_shift)
            self.add_widget(new_pipe)
            new_pipe.pos = self.x_pos_pipe_creation, -100 + height_shift
            self.pipes.append(new_pipe)
            self.horizon_shift = randint(0, 300)

    def check_colision(self):
        four_bird_points = self.bird.get_four_points()
        for pipe in self.pipes:
            if pipe.check_collide(four_bird_points):
                self.bird.is_alive = False

    def game_over(self):
        game_over = RelativeLayout(pos_hint={"x": -0.1, "top": 1.2})
        game_over.add_widget(Label(text='GameOver'))
        self.add_widget(game_over)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        print(touch.pos)

class ScoreLabel(Label):

    def __init__(self):
        super().__init__()

    def change_text(self, value):
        self.text = "SCORE: " + str(value)


class PicturesApp(App):

    def build(self):
        game_field = DrawTool()
        layout = BoxLayout(size_hint=(1, None), height=50)
        score_label = ScoreLabel()
        layout.add_widget(score_label)
        game_field.change_text_delegate = score_label.change_text
        Window.clearcolor = (1, 1, 1, 1)
        root = BoxLayout(orientation='vertical')
        root.add_widget(layout)
        root.add_widget(game_field)
        return root


    def on_pause(self):
        return True


if __name__ == '__main__':
    PicturesApp().run()