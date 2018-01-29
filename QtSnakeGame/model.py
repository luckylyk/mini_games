from PyQt4 import QtCore
from core import Direction, FieldSquareState, Options
import random


class FieldModel(QtCore.QObject):
    '''
    this class represent the field playground
    '''
    valuesChanged = QtCore.pyqtSignal()

    def __init__(self, sizes=(50, 50)):
        super().__init__()
        self._sizes = sizes
        self._values = []
        self._item_index = None
        self._indexes = self._generate_all_indexes()
        self.reinitialize()

    @property
    def indexes(self):
        return self._indexes

    def reinitialize(self):
        ''' Reinitialize the grid '''
        self._values = [
            [FieldSquareState.empty for _ in range(self._sizes[1])]
            for _ in range(self._sizes[0])]

    def set_item_index(self, index):
        ''' set the item position '''
        self._item_index = index

    def get_value(self, row, column):
        ''' get value from a field index '''
        if self._values is None:
            return None
        return self._values[row][column]

    def set_values(self, snake=[]):
        ''' set all index values from snake and current item index '''
        self.reinitialize()

        if self._item_index is not None:
            row, col = self._item_index.row, self._item_index.column
            self._values[row][col] = FieldSquareState.item

        for index in snake:
            self._values[index.row][index.column] = FieldSquareState.snake

        self.valuesChanged.emit()

    def get_empty_positions(self):
        ''' get all indexes with state empty '''
        indexes = []
        for row in range(self.row_count()):
            for column in range(self.column_count()):
                if self.get_value(row, column) == FieldSquareState.empty:
                    indexes.append(FieldIndexItemModel(row, column))
        return indexes

    def row_count(self):
        return self._sizes[0]

    def column_count(self):
        return self._sizes[1]

    def _generate_all_indexes(self):
        ''' generate all item for the iteration '''
        indexes = []
        for row in range(self._sizes[0]):
            for col in range(self._sizes[1]):
                indexes.append(FieldIndexItemModel(row, col))
        return indexes


class FieldIndexItemModel(object):
    '''
    this class represent a index from the Field playground grid
    '''

    def __init__(self, row=0, column=0):
        self._row = row
        self._column = column

    @property
    def row(self):
        return int(self._row)

    @property
    def column(self):
        return int(self._column)

    def __eq__(self, item):
        if not isinstance(item, FieldIndexItemModel):
            return False
        return self._row == item.row and self._column == item.column

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return str(('FieldIndexItemModel', self.row, self.column))


class SnakeModel(QtCore.QObject):
    '''
    this class represent the snake
    it contain all body indexes and the snake moving algorythm
    ::origin is the starting pose
    '''
    moved = QtCore.pyqtSignal(list)

    def __init__(self, origin=FieldIndexItemModel(0, 0)):
        super().__init__()
        self._origin = origin
        self._indexes = [origin]
        self._direction = Direction.left
        self._direction_locked = False

    def __iter__(self):
        return self._indexes.__iter__()

    @property
    def head_index(self):
        return self._indexes[0]

    @property
    def body_indexes(self):
        return self._indexes[1:]

    def set_direction(self, value):
        ''' 
        the direction can changed one time per move
        180 degree movement is forbidden
        '''
        if abs(self._direction - value) == 2 or self._direction_locked:
            return
        self._direction = value
        self._direction_locked = True

    def next(self, grow=False):
        ''' change all indexes from the current direction '''
        # force grow if snake is small
        if len(self._indexes) <= 1:
            grow = True

        snake_head_index = [self._get_new_head_index()]
        snake_body_indexes = self._indexes[:-1] if not grow else self._indexes
        self._indexes = snake_head_index + snake_body_indexes

        self._direction_locked = False
        self.moved.emit(self._indexes)

    def reset(self):
        self._indexes = [self._origin]

    def _get_new_head_index(self):

        old_snake_head_index = self._indexes[0]

        if self._direction == Direction.left:
            new_snake_head_index = FieldIndexItemModel(
                old_snake_head_index.row, old_snake_head_index.column - 1)

        if self._direction == Direction.up:
            new_snake_head_index = FieldIndexItemModel(
                old_snake_head_index.row - 1, old_snake_head_index.column)

        if self._direction == Direction.right:
            new_snake_head_index = FieldIndexItemModel(
                old_snake_head_index.row, old_snake_head_index.column + 1)

        if self._direction == Direction.down:
            new_snake_head_index = FieldIndexItemModel(
                old_snake_head_index.row + 1, old_snake_head_index.column)

        return new_snake_head_index
