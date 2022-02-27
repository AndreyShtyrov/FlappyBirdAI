from random import randint

from kivy.uix.relativelayout import RelativeLayout
from Bird import BirdWidget
from Pipe import PipWidget
import numpy as np


class GameMode():

    def __init__(self, draw_tool: RelativeLayout):
        self.score = 0
        self.draw_tool = draw_tool
        self.pipes = []
        self.x_speed_multiplier = 2
        self.is_loose = False
        self.horizon_shift = 0
        self.bird = BirdWidget()
        self.draw_tool.add_widget(self.bird)
        self.bird.pos = (200, 300)
        self.change_text_delegate = None
        self.x_pos_pipe_creation = 1600

    def get_vector_to_learn(self):
        result = []
        result.append(self.x_speed_multiplier)
        bird_pos = self.bird.pos
        result.append(bird_pos[1]/self.draw_tool.size[1])
        for pip in self.pipes:
            pos = pip.pos
            if pos[0] - bird_pos[0] > 0:
                result.append((pos[0] - bird_pos[0])/self.draw_tool.size[0])
                result.append(pos[1] / self.draw_tool.size[1])
                break
        return np.array(result)

    def main_loop(self, dt):
        if self.is_loose:
            return False
        if not self.bird.is_alive:
            self.is_loose = True
            self.draw_tool.remove_widget(self.bird)
            for pip in self.pipes:
                self.draw_tool.remove_widget(pip)
            self.pipes.clear()
            return False
        self.score += 1
        self.create_pipe(dt)

        old_pos = self.bird.pos
        new_pos = (old_pos[0], old_pos[1] + self.bird.calculate_current_bird_velocity())
        if self.draw_tool.size[1] > new_pos[1] >= 0:
            self.bird.move(new_pos)
        else:
            if self.draw_tool.size[1] > 300:
                self.bird.is_alive = False
                return
        for pipe in self.pipes:
            old_pos = pipe.pos
            pipe.pos = (old_pos[0] - 1 * self.x_speed_multiplier, old_pos[1])
        if len(self.pipes) == 0:
            return
        first_pipe = self.pipes[0]
        if first_pipe.pos[0] < -100:
            self.draw_tool.remove_widget(first_pipe)
            self.pipes.remove(first_pipe)
        self.check_collision()

    def create_pipe(self, dt):
        if len(self.pipes) == 0:
            height_shift = randint(-100, 100)
            new_pipe = PipWidget(height_shift)
            self.draw_tool.add_widget(new_pipe)
            new_pipe.pos = self.x_pos_pipe_creation, -100 + height_shift
            self.pipes.append(new_pipe)
            self.horizon_shift = randint(0, 300)
            return
        last_pipe = self.pipes[-1]
        if abs(last_pipe.pos[0] - self.x_pos_pipe_creation) > 150 + self.horizon_shift:
            height_shift = randint(-100, 100)
            new_pipe = PipWidget(height_shift)
            self.draw_tool.add_widget(new_pipe)
            new_pipe.pos = self.x_pos_pipe_creation, -100 + height_shift
            self.pipes.append(new_pipe)
            self.horizon_shift = randint(0, 300)

    def check_collision(self):
        four_bird_points = self.bird.get_four_points()
        for pipe in self.pipes:
            is_crushed, how_close_to_path = pipe.check_collide(four_bird_points)
            if is_crushed:
                self.bird.is_alive = False
                self.score += min(1/(how_close_to_path/100), 10)

