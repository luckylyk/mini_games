import random

DEFAULT_SPEED = 5


class Ball(object):
    def __init__(self, position=None):
        self.direction = random.randint(0, 360)
        self.speed = DEFAULT_SPEED
        self.position = position

    def __iter__(self):
        pass