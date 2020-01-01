from PyQt5 import QtWidgets, QtGui, QtCore
import time
import random


class MineSweeperController():

    def __init__(self, model, view, size, number_of_bombs):
        self.model = model
        self.model.set_size(size)
        self.model.set_bomb_number(number_of_bombs)
        self.model.initialize()
        self.model.start()

        self.view = view
        self.view.set_model(self.model)
        self.view.openIndexRequested.connect(self.model.open_index)
        self.view.setNextMarkRequested.connect(self.model.set_next_mark)

    def show(self):
        self.view.show()


class MineSweeperStatus(object):
    '''
    MineSweeper game status
    '''
    READY_TO_START = 0
    GAME_IN_PROGRESS = 1
    GAME_OVER_DEFEAT = 2
    GAME_OVER_VICTORY = 3


class FieldIndexStates(object):
    '''
    all description of field indexes
    '''
    class STATE(int):
        pass

    CLOSED = STATE(False)
    OPENED = STATE(True)

    class CONTENT(str):
        '''
        content of the index
        '''
        pass

    EMPTY = CONTENT('empty')
    BOMB = CONTENT('bomb')

    class MARK(str):
        '''
        for display a closed index
        '''
        pass

    BASIC = MARK('basic')
    FLAG = MARK('flag')
    NUMBER = MARK('number')
    INTERROGATION = MARK('interrogation')


class FieldSize(object):
    '''
    class represent the size of the board
    '''

    def __init__(self, height=10, width=10):
        self._height = height
        self._width = width

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width


def get_flag_polygon(rect):
    '''
    return a QPolygone triangle representing
    the fabric part of the MineSweeper Flag
    '''
    polygon_top = QtCore.QPoint(
        rect.left() + rect.width() // 3, rect.top() + (rect.height() // 12))
    polygon_bot = QtCore.QPoint(
        rect.left() + (rect.width() // 3), rect.top() + rect.height() // 3)
    polygon_right = QtCore.QPoint(
        rect.left() + rect.width() - rect.width() // 12,
        rect.top() + rect.height() // 2 - (rect.height() // 3))
    return QtGui.QPolygon([polygon_top, polygon_bot, polygon_right])


def get_flag_line(rect):
    '''
    return a QtCore.QLine representing the woodstick of the MineSweeper Flag
    '''
    point_1 = QtCore.QPoint(
        rect.left() + rect.width() // 3, rect.top() + (rect.height() // 10))
    point_2 = QtCore.QPoint(
        rect.left() + rect.width() // 3, rect.top() + rect.height() - ((rect.height() // 10)))
    return QtCore.QLine(point_1, point_2)


def shrink_rect(rect, value):
    '''
    return a QtCore.QRect() shrinked from the value
    '''
    return QtCore.QRect(
        rect.left() + value,
        rect.top() + value,
        rect.width() - (value * 2),
        rect.height() - (value * 2))


def get_cross_lines(rect):
    '''
    return two diagonals QtCore.QLine from a QtCore.QRect
    '''
    line_1 = QtCore.QLine(
        QtCore.QPoint(rect.left(), rect.top()),
        QtCore.QPoint(rect.left() + rect.width(), rect.top() + rect.height()))
    line_2 = QtCore.QLine(
        QtCore.QPoint(rect.left(), rect.top() + rect.height()),
        QtCore.QPoint(rect.left() + rect.width(), rect.top()))
    return line_1, line_2


class MineSweeperModel(object):
    '''
    Model of the game
    '''

    SIZE = FieldSize(40, 25)
    BOMBS = (SIZE.height * SIZE.width) // 20

    def __init__(self):
        self._field_model = None
        self._current_status = MineSweeperStatus.READY_TO_START

    def initialize(self):
        self._field_model = FieldModel(self.SIZE)
        self._field_model.initialize()
        for field_index in self._field_model:
            field_index.opened.connect(self.index_opened)

    def reset(self):
        self.initialize()
        self._current_status = MineSweeperStatus.READY_TO_START

    def start(self):
        self._current_status = MineSweeperStatus.GAME_IN_PROGRESS
        self._field_model.set_random_bombs(self.BOMBS)

    def set_size(self, size):
        self.SIZE = size

    def size(self):
        return self.SIZE

    def set_bomb_number(self, value):
        assert value <= (self.SIZE.height * self.SIZE.width)
        self.BOMBS = value

    def open_index(self, row, col):
        assert self._current_status == MineSweeperStatus.GAME_IN_PROGRESS
        index = self._field_model.find_index(row, col)
        index.open()

    def index_opened(self, content):
        if content == FieldIndexStates.BOMB:
            self._current_status = MineSweeperStatus.GAME_OVER_DEFEAT
        if self._field_model.is_finished():
            self._current_status = MineSweeperStatus.GAME_OVER_VICTORY

    def indexes(self):
        return self._field_model.list()

    def set_next_mark(self, row, col):
        index = self._field_model.find_index(row, col)
        if index.is_closed():
            index.set_next_mark()

    def finish(self):
        self._current_status = MineSweeperStatus.GAME_OVER_VICTORY

    @property
    def current_status(self):
        return self._current_status

    def __repr__(self):
        self._field_model.view()
        return '<MineSweeperModel object>'


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
        self.mark = FieldIndexStates.INTERROGATION

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
        get all indexes in a list, not in a matrix
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



class MineSweeperFieldView(QtWidgets.QWidget):
    openIndexRequested = QtCore.pyqtSignal(int, int)
    setNextMarkRequested = QtCore.pyqtSignal(int, int)

    SQUARES_SIZE = QtCore.QSize(20, 20)
    SQUARES_MEDIUM_SIZE = (SQUARES_SIZE.width() + SQUARES_SIZE.height()) // 2

    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Tool)
        self._model = None
        self._rects = []
        self._mouse_hover = False
        self._rect_hover = None
        self.setMouseTracking(True)

    def set_model(self, model):
        self._model = model

        model_size = self._model.size()

        self.setFixedSize(
            model_size.height * self.SQUARES_SIZE.height(),
            model_size.width * self.SQUARES_SIZE.width())

        for index in self._model.indexes():
            rect = QtCore.QRect(
                index.row * self.SQUARES_SIZE.width(),
                index.column * self.SQUARES_SIZE.height(),
                self.SQUARES_SIZE.width(),
                self.SQUARES_SIZE.height())
            rect.index = index
            self._rects.append(rect)

    def enterEvent(self, _):
        self._mouse_hover = True
        self.repaint()

    def leaveEvent(self, _):
        self._mouse_hover = False
        self.repaint()

    def mouseMoveEvent(self, event):
        for rect in self._rects:
            if rect.contains(event.pos()):
                self._rect_hover = rect
                self.repaint()
                return
        self._rect_hover = None

    def mouseReleaseEvent(self, event):
        if self._rect_hover:
            index = self._rect_hover.index
            if event.button() == QtCore.Qt.LeftButton:
                self.openIndexRequested.emit(index.row, index.column)
            if event.button() == QtCore.Qt.RightButton:
                self.setNextMarkRequested.emit(index.row, index.column)
        self.repaint()

    def paintEvent(self, _):
        if self._model is None:
            return

        painter = QtGui.QPainter()
        painter.begin(self)
        if self._model.current_status == MineSweeperStatus.GAME_IN_PROGRESS:
            self.paint(painter)
        elif self._model.current_status == MineSweeperStatus.GAME_OVER_DEFEAT:
            self.paint_game_over(painter)
        elif self._model.current_status == MineSweeperStatus.GAME_OVER_VICTORY:
            self.paint_victory(painter)
        painter.end()

    def paint_victory(self, painter):
        self.paint(painter)

        painter.setBrush(QtGui.QColor(150, 150, 150, 75))
        painter.drawRect(self.rect())

        pen = QtGui.QPen(QtGui.QColor(180, 50, 30, 150))
        painter.setPen(pen)

        font = QtGui.QFont('verdana')
        font.setPointSize(self.rect().width() // 25)
        font.setBold(True)
        painter.setFont(font)

        painter.drawText(
            self.rect(),
            QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter,
            'VICTORY')

    def paint_game_over(self, painter):
        self.paint(painter)

        for rect in self._rects:

            pen = QtGui.QPen()
            pen.setColor(QtGui.QColor(75, 90, 120))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.setBrush(QtGui.QColor(0, 0, 0, 0))

            index = rect.index
            if index.is_bomb():
                if index.mark != FieldIndexStates.FLAG:
                    painter.setBrush(QtGui.QColor(0, 0, 0))
                    painter.drawRoundedRect(
                        shrink_rect(rect, self.SQUARES_MEDIUM_SIZE // 5), 600, 600)

            elif index.mark == FieldIndexStates.FLAG:
                pen.setColor(QtGui.QColor('red'))
                pen.setWidth(3)
                painter.setPen(pen)
                for line in get_cross_lines(shrink_rect(rect, self.SQUARES_MEDIUM_SIZE // 7)):
                    painter.drawLine(line)

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.setBrush(self.palette().color(QtGui.QPalette.Background))
        painter.drawRect(self.rect())

        font = QtGui.QFont('verdana')
        font.setPointSize(self.SQUARES_MEDIUM_SIZE // 2)
        font.setBold(True)
        painter.setFont(font)

        for rect in self._rects:

            pen = QtGui.QPen()
            pen.setColor(QtGui.QColor(75, 90, 120))
            pen.setWidth(1)
            painter.setPen(pen)

            index = rect.index
            if index.is_closed() is False:
                painter.setBrush(QtGui.QColor(200, 200, 200))
                painter.drawRect(rect)
                if index.bomb_around_number:
                    painter.drawText(
                        rect,
                        QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter,
                        str(index.bomb_around_number))
                continue

            painter.setBrush(QtGui.QColor(150, 150, 150))
            painter.drawRect(rect)

            if index.mark == FieldIndexStates.FLAG:
                drawrect = shrink_rect(rect, self.SQUARES_MEDIUM_SIZE // 10)
                pen.setWidth(0)
                painter.setBrush(QtGui.QColor('red'))
                painter.setPen(pen)
                painter.drawPolygon(get_flag_polygon(drawrect))
                pen.setWidth(1)
                painter.setBrush(QtGui.QColor('grey'))
                painter.setPen(pen)
                painter.drawLine(get_flag_line(drawrect))
            elif index.mark == FieldIndexStates.INTERROGATION:
                flags = QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter
                painter.drawText(rect, flags, '?')

        # paint the hover index
        if self._rect_hover is not None:
            pen.setColor(QtGui.QColor(100, 100, 100))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(QtGui.QColor(0, 0, 0, 0))
            painter.drawRect(
                shrink_rect(self._rect_hover, self.SQUARES_MEDIUM_SIZE // 50))

    def set_square_size(self, height, width):
        self.SQUARES_SIZE = QtCore.QSize(height, width)


def start_minesweeper(size, number_of_bombs):
    '''
    function to start a minesweeper controller with options
    '''
    app = QtWidgets.QApplication([])
    controller = MineSweeperController(
        model=MineSweeperModel(),
        view=MineSweeperFieldView(),
        size=size,
        number_of_bombs=number_of_bombs)
    controller.show()
    app.exec_()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('height', type=int)
    parser.add_argument('width', type=int)
    parser.add_argument('bombs', type=int)
    arguments = parser.parse_args()
    total_field = arguments.height * arguments.width
    if arguments.bombs > (total_field / 5):
        raise ValueError("too many bombs are set for the grid")
    start_minesweeper(FieldSize(arguments.width, arguments.height), arguments.bombs)