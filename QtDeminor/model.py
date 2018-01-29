'''
this module is an command version of the deminor game
You can use this module completely independent of the controller and the model
you can print the DeminorModel to se the current game state

---------------
 example usage
---------------

from QtDeminor.model import DeminorModel
from QtDeminor.core import FieldSize

deminor = DeminorModel()
deminor.set_size(FieldSize(20, 13))
deminor.set_bomb_number(25)
deminor.initialize()
deminor.start()
deminor.open_index(3, 3)
print(deminor)

'''


from QtDeminor.core import FieldIndexStates, FieldSize, DeminorStatus
from PyQt4 import QtCore
import random
import time


class DeminorModel(object):
    '''
    Model of the game
    '''

    SIZE = FieldSize(40, 25)
    BOMBS = (SIZE.height * SIZE.width) // 20

    def __init__(self):
        self._field_model = None
        self._current_status = DeminorStatus.READY_TO_START

    def initialize(self):
        self._field_model = FieldModel(self.SIZE)
        self._field_model.initialize()
        for field_index in self._field_model:
            field_index.opened.connect(self.index_opened)

    def reset(self):
        self.initialize()
        self._current_status = DeminorStatus.READY_TO_START

    def start(self):
        self._current_status = DeminorStatus.GAME_IN_PROGRESS
        self._field_model.set_random_bombs(self.BOMBS)

    def set_size(self, size):
        self.SIZE = size

    def size(self):
        return self.SIZE

    def set_bomb_number(self, value):
        assert value <= (self.SIZE.height * self.SIZE.width)
        self.BOMBS = value

    def open_index(self, row, col):
        assert self._current_status == DeminorStatus.GAME_IN_PROGRESS
        index = self._field_model.find_index(row, col)
        index.open()

    def index_opened(self, content):
        if content == FieldIndexStates.BOMB:
            self._current_status = DeminorStatus.GAME_OVER_DEFEAT
        if self._field_model.is_finished():
            self._current_status = DeminorStatus.GAME_OVER_VICTORY

    def indexes(self):
        return self._field_model.list()

    def set_next_mark(self, row, col):
        index = self._field_model.find_index(row, col)
        if index.is_closed():
            index.set_next_mark()

    def finish(self):
        self._current_status = DeminorStatus.GAME_OVER_VICTORY

    @property
    def current_status(self):
        return self._current_status

    def __repr__(self):
        self._field_model.view()
        return '<DeminorModel object>'


class FieldIndexModel(QtCore.QObject):
    '''
    Class represent emplacement in the field (board game)
    '''
    opened = QtCore.pyqtSignal(FieldIndexStates.CONTENT)
    requestAroundOpening = QtCore.pyqtSignal(
        int, int, FieldIndexStates.CONTENT)

    def __init__(self, row, column):
        super().__init__()
        super(QtCore.QObject, self).__init__()
        self._bomb_around_number = 0
        self._row = row
        self._column = column
        self._state = FieldIndexStates.CLOSED
        self._content = FieldIndexStates.EMPTY
        self._mark = FieldIndexStates.BASIC

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        self._mark = value

    def set_next_mark(self):
        '''
        if the index is close, he can marked as flag
        or by an interrogation point
        '''
        if self._mark == FieldIndexStates.BASIC:
            self._mark = FieldIndexStates.FLAG
        elif self._mark == FieldIndexStates.FLAG:
            self._mark = FieldIndexStates.INTERROGATION
        elif self._mark == FieldIndexStates.INTERROGATION:
            self._mark = FieldIndexStates.BASIC

    @property
    def bomb_around_number(self):
        return self._bomb_around_number

    def set_bomb_around_number(self, value):
        self._bomb_around_number = value

    def set_bomb(self):
        self.content = FieldIndexStates.BOMB

    def set_basic(self):
        self.mark = FieldIndexStates.BASIC

    def set_flag(self):
        self.mark = FieldIndexStates.FLAG

    def set_interrogation(self):
        self.mark = FieldIndexStats.INTERROGATION

    def is_closed(self):
        return self.state == FieldIndexStates.CLOSED

    def is_bomb(self):
        return self.content == FieldIndexStates.BOMB

    def is_flag(self):
        return self.mark != FieldIndexStates.BASIC

    def open(self, signal=True):
        self.state = FieldIndexStates.OPENED

        if self.content == FieldIndexStates.EMPTY:
            self.mark = FieldIndexStates.NUMBER

        self.opened.emit(self.content)
        if self.bomb_around_number == 0 and signal:
            self.requestAroundOpening.emit(
                self.row, self.column, self.content)

    def __str__(self):
        if self.state == FieldIndexStates.CLOSED:
            return '.'
        else:
            if self.content == FieldIndexStates.BOMB:
                return 'B'
            else:
                return str(self.bomb_around_number)

    def __repr__(self):
        return '<FieldIndexModel <row={} col={} content={} bombs around={}>'.format(
            self.row, self.column, self.content, self.bomb_around_number)

    def __eq__(self, index):
        if not isinstance(index, FieldIndexModel):
            return False
        return self.row == index.row and self.column == index.column


class FieldModel(QtCore.QObject):
    '''
    Class represent the board game as matrix
    '''

    def __init__(self, size=FieldSize()):
        super().__init__()
        self._size = size
        self._indexes = [[]]
        self._bombs_number = None

    def column_count(self):
        return self._size.width

    def row_count(self):
        return self._size.height

    def initialize(self):
        '''
        create all indexes containend in the field
        '''
        self._indexes = [
            [FieldIndexModel(row, column)
             for column in range(self.column_count())]
            for row in range(self.row_count())]

        for index in self:
            index.requestAroundOpening.connect(self._index_opened)

    def find_index(self, row, col):
        '''
        return the field index object requested
        '''
        return self._indexes[row][col]

    def set_random_bombs(self, number):
        '''
        place the bombs
        :index: index who don't place the bomb (first index opened)
        :number: number of bombs to place
        '''
        self._bombs_number = number
        indexes = []

        for row in self._indexes:
            indexes += row

        for n in range(number):
            index = random.choice(indexes)
            indexes.remove(index)
            self._indexes[index.row][index.column].set_bomb()

        self._set_bombs_number_around()

    def _around_indexes(self, index):
        '''
        return the 8 index around an index
        '''
        row_cols = [
            [index.row - 1, index.column - 1],
            [index.row - 1, index.column],
            [index.row - 1, index.column + 1],
            [index.row, index.column - 1],
            [index.row, index.column + 1],
            [index.row + 1, index.column - 1],
            [index.row + 1, index.column],
            [index.row + 1, index.column + 1]]

        return [
            self.find_index(*row_col) for row_col in row_cols
            if FieldIndexModel(*row_col) in self]

    def _filtered_around_indexes(self, indexes, bomb_around_is_nul=True):
        filtered_indexes = []
        if bomb_around_is_nul:
            for index in indexes:
                filtered_indexes += [
                    i for i in self._around_indexes(index)
                    if not i.is_bomb() and i.is_closed()
                    and not i in filtered_indexes
                    if i.bomb_around_number == 0]
        else:
            for index in indexes:
                filtered_indexes += [
                    i for i in self._around_indexes(index)
                    if not i.is_bomb() and i.is_closed()
                    and not i in filtered_indexes]
        return filtered_indexes

    def _set_bombs_number_around(self):
        '''
        calcul the number of bomb around every field index
        '''
        for index in self:
            indexes = self._around_indexes(index)
            index.set_bomb_around_number(sum([
                True for i in indexes if i.is_bomb()]))

    def _index_opened(self, row, col, content):
        '''
        open the index in cascade
        '''
        if content == FieldIndexStates.BOMB:
            return

        # open in cascade
        indexes = [
            index for index in self._around_indexes(FieldIndexModel(row, col))
            if not index.is_bomb() if index.is_closed()]
        opened = []
        while indexes != []:
            for index in indexes:
                index.open(signal=False)
                opened.append(index)
            indexes = self._filtered_around_indexes(indexes)

        # limit
        for index in self._filtered_around_indexes(opened, bomb_around_is_nul=False):
            index.open(signal=False)

    def is_finished(self):
        '''
        query if the all the index doesn't containing bomb are opened
        '''
        return len([index for index in self.list() if index.is_closed()]) == self._bombs_number

    def list(self):
        '''
        get qll indexes in a list, not in a matrix
        '''
        indexes = []
        for row in self._indexes:
            indexes += row
        return indexes

    def view(self):
        '''
        nice print
        '''
        for row in self._indexes:
            print([str(index) for index in row])

    def __repr__(self):
        return '<FieldModel {} {}>'.format(self._size.height, self._size.width)

    def __iter__(self):
        return self.list().__iter__()
