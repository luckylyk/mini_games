from model import FieldModel, SnakeModel, FieldIndexItemModel
from core import Direction, Options
from view import FieldView
import time
import random


class SnakeGame(object):

    def __init__(self):
        super().__init__()

        self.init_game_states()

        # init objects
        self._field_model = FieldModel(Options.field_size)
        self._field_view = FieldView()
        self._field_view.set_model(self._field_model)
        self._field_view.set_message(self.message)
        self._snake = SnakeModel(
            origin=FieldIndexItemModel(
                self._field_model.row_count() / 2,
                self._field_model.column_count() / 2))
        self._field_model.set_values(snake=self._snake)
        self._item_index = None

        # connect
        self._snake.moved.connect(self._field_model.set_values)
        self._field_model.valuesChanged.connect(self._field_view.repaint)
        self._field_view.pauseRequested.connect(self.switch_pause)
        self._field_view.timeSequenceFinished.connect(self.next)
        self._field_view.restartGameRequested.connect(self.restart)
        self._field_view.directionPressed.connect(
            self._snake.set_direction)

    def init_game_states(self):
        self.pause = True
        self.snake_is_dead = False
        self.message = 'Welcome to Snake'
        self.score = 0

    def show(self, title=''):
        self._field_view.adjust_geometry()
        self._field_view.center()
        self._field_view.setWindowTitle(title)
        self._field_view.show()

    def switch_pause(self):
        if self.snake_is_dead:
            return
        self.pause = not self.pause
        self._field_view.set_message(self.message)
        self._field_view.set_message_visible(self.pause)
        self._field_view.repaint()

    def start(self):
        self._field_view.start(Options.speed)
        self._item_index = random.choice(
            self._field_model.get_empty_positions())
        self._field_model.set_item_index(self._item_index)
        self.message = 'pause'

    def restart(self):
        self.init_game_states()
        self._snake.reset()
        self._field_view.set_message(self.message)
        self._field_view.repaint()
        self.start()

    def next(self):
        ''' its every step of the game, activated by the timerEvent '''
        if self.pause:
            return

        # check if the snake is eating an item
        if self._snake.head_index == self._item_index:
            self._item_index = random.choice(
                self._field_model.get_empty_positions())
            self._field_model.set_item_index(self._item_index)
            self.score += 1
            grow = True
        else:
            grow = False

        # check if the snake is eating himself
        if self._snake.head_index in self._snake.body_indexes:
            return self.game_over(
                'Game Over\n'
                'don\'t eat yourself !\n'
                'Score is {}'.format(self.score))

        # check if the snake is out of the field
        if self._snake.head_index not in self._field_model.indexes:
            return self.game_over(
                'Game Over\n'
                'out of field !\n'
                'Score is {}'.format(self.score))

        self._snake.next(grow)

    def game_over(self, message):
        self.message = message
        self.switch_pause()
        self.snake_is_dead = True
 
