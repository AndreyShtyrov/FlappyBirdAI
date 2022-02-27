from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *


class PipWidget(RelativeLayout):

    def __init__(self, height_shift=0):
        super().__init__()
        self.height_shift = height_shift
        with self.canvas:
            self.up_pipe = Rectangle(source='up_pipe.png', size=(90, 800), pos=(0, 470))
            self.down_pipe = Rectangle(source='down_pipe.png', size=(90, 800), pos=(0, -470))

    def get_right_point(self):
        return self.to_parent(*self.up_pipe.size)[0]

    def check_collide(self, four_points: list):
        left_border = self.pos[0]
        if four_points[0][0] < left_border:
            return False, 0
        right_border = self.to_parent(*self.up_pipe.size)[0]
        for point in four_points:
             if left_border < point[0] < right_border:
                down_border = self.height_shift - 100 + self.down_pipe.size[1] + self.down_pipe.pos[1]
                up_border = self.up_pipe.pos[1] - 100 + self.height_shift
                if point[1] < down_border or point[1] > up_border:
                    return True, min([abs(point[1] - down_border), abs(point[1] - up_border)])
        return False, 0
