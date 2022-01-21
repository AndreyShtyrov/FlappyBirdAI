from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *


class BirdWidget(RelativeLayout):

    def __init__(self):
        super().__init__()
        self.bird_velocity = -2
        self.y_velocity = -2
        self.bird_acceleration = 15
        self.is_alive = True
        with self.canvas:
            Rectangle(source='bird.png', size=(30, 30))

    def calculate_current_bird_velocity(self):
        if self.bird_velocity <= self.y_velocity:
            self.bird_velocity = self.y_velocity
            return self.y_velocity
        self.bird_velocity -= 1
        return int(self.bird_velocity)

    def jump(self):
        self.bird_velocity += self.bird_acceleration

