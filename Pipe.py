from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *


class PipWidget(RelativeLayout):

    def __init__(self, height_shift=0):
        super().__init__()
        self.height_shift = height_shift
        with self.canvas:
            Rectangle(source='up_pipe.png', size=(70, 300), pos=(0, 450))
            Rectangle(source='down_pipe.png', size=(70, 300), pos=(0, 0))


