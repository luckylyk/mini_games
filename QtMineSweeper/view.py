from PyQt4 import QtGui, QtCore
from graphic import get_flag_polygon, get_flag_line, shrink_rect, get_cross_lines
from core import FieldIndexStates
from QtMineSweeper.core import MineSweeperStatus


class MineSweeperFieldView(QtGui.QWidget):
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
                    painter.drawRoundRect(
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
            if index.is_closed():
                painter.setBrush(QtGui.QColor(150, 150, 150))
                painter.drawRect(rect)

                if index.mark == FieldIndexStates.FLAG:
                    pen.setWidth(0)
                    painter.setBrush(QtGui.QColor('red'))
                    painter.setPen(pen)
                    painter.drawPolygon(
                        get_flag_polygon(
                            shrink_rect(
                                rect,
                                self.SQUARES_MEDIUM_SIZE // 10)))
                    pen.setWidth(1)
                    painter.setBrush(QtGui.QColor('grey'))
                    painter.setPen(pen)
                    painter.drawLine(
                        get_flag_line(
                            shrink_rect(
                                rect,
                                self.SQUARES_MEDIUM_SIZE // 10)))

                elif index.mark == FieldIndexStates.INTERROGATION:
                    painter.drawText(
                        rect,
                        QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter,
                        '?')
            else:
                painter.setBrush(QtGui.QColor(200, 200, 200))
                painter.drawRect(rect)
                if index.bomb_around_number:
                    painter.drawText(
                        rect,
                        QtCore.Qt.AlignCenter | QtCore.Qt.AlignHCenter,
                        str(index.bomb_around_number))

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
