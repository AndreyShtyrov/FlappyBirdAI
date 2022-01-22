from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *


class BirdWidget(RelativeLayout):

    def __init__(self, size=(40, 40)):
        super().__init__(size=(40, 40))
        self.bird_velocity = -2
        self.y_velocity = -2
        self.bird_acceleration = 15
        self.is_alive = True
        with self.canvas:
            self.image = Rectangle(source='bird.png', size=(40, 40))

    def calculate_current_bird_velocity(self):
        if self.bird_velocity <= self.y_velocity:
            self.bird_velocity = self.y_velocity
            return self.y_velocity
        self.bird_velocity -= 1
        return int(self.bird_velocity)

    def jump(self):
        self.bird_velocity += self.bird_acceleration

    def move(self, pos: tuple):
        self.pos = pos

    def get_four_points(self):
        center = self.pos
        size = self.image.size
        result = []
        result.append((center[0] + size[0], center[1] + size[1]))
        result.append((center[0] + size[0], center[1]))
        result.append((center[0], center[1] + size[1]))
        result.append((center[0], center[1]))
        return result




