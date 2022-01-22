import kivy
kivy.require('1.0.6')

from random import randint
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from Bird import BirdWidget
from Pipe import PipWidget
from kivy.lang import Builder



class Picture(Scatter):


    source = StringProperty(None)


class DrawTool(RelativeLayout):

    def __init__(self):
        super().__init__()
        self.bird = BirdWidget()
        self.add_widget(self.bird)
        self.bird.pos = (200, 300)
        self.pipes = []
        Clock.schedule_interval(self.main_loop, 0.005)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.x_pos_pipe_creation = 800

    def main_loop(self, dt):
        print("start main loop")
        if not self.bird.is_alive:
            return False
        self.create_pipe(dt)
        print(dt)
        old_pos = self.bird.pos
        print(self.bird.is_alive)
        print(old_pos)
        if old_pos[1] >= 0:
            new_pos = (old_pos[0], old_pos[1] + self.bird.calculate_current_bird_velocity())
            self.bird.pos = new_pos
        for pipe in self.pipes:
            old_pos = pipe.pos
            pipe.pos = (old_pos[0] - 2, old_pos[1])
        if len(self.pipes) == 0:
            return
        first_pipe = self.pipes[0]
        if first_pipe.pos[0] < 100:
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

    def create_pipe(self, dt):
        if len(self.pipes) == 0:
            height_shift = randint(-100, 100)
            new_pipe = PipWidget(height_shift)
            self.add_widget(new_pipe)
            new_pipe.pos = self.x_pos_pipe_creation, -100 + height_shift
            self.pipes.append(new_pipe)
            return
        last_pipe = self.pipes[-1]
        if abs(last_pipe.pos[0] - self.x_pos_pipe_creation) > 150:
            height_shift = randint(-100, 100)
            new_pipe = PipWidget(height_shift)
            self.add_widget(new_pipe)
            new_pipe.pos = self.x_pos_pipe_creation, -100 + height_shift
            self.pipes.append(new_pipe)

    def check_colision(self):
        bird_pos = self.bird.pos
        for pipe in self.pipes:
            pipe_pos = pipe.pos
            if pipe_pos[0] - 35 < bird_pos[0] < pipe_pos[0] + 35 + 30:
                if 350 + pipe.height_shift > bird_pos[1] + 30 and bird_pos[1] > 200 + pipe.height_shift:
                    return
                else:
                    self.game_over()
                    self.bird.is_alive = False

    def game_over(self):
        game_over = RelativeLayout(size=(200, 200), pos=(300, 300))
        game_over.add_widget(Label(text='GameOver', size=(200, 200)))
        self.add_widget(game_over)



class PicturesApp(App):

    def build(self):


        root = DrawTool()
        return root


    def on_pause(self):
        return True


if __name__ == '__main__':
    PicturesApp().run()