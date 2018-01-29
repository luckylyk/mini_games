from PyQt4 import QtGui, QtCore
from core import Options, FieldSquareState, Direction


class FieldView(QtGui.QWidget):
    directionPressed = QtCore.pyqtSignal(int)
    pauseRequested = QtCore.pyqtSignal()
    timeSequenceFinished = QtCore.pyqtSignal()
    restartGameRequested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = None
        self._rects = []
        self._timer = QtCore.QBasicTimer()
        self._message = ''
        self._message_visible = True

    def set_model(self, model):
        self._model = model
        self._rects = self._get_rects()
        self.setGeometry(
            0, 0,
            Options.rect_size * self._model.column_count(),
            Options.rect_size * self._model.row_count())

    def set_message(self, message):
        self._message = message

    def set_message_visible(self, state):
        self._message_visible = state

    def start(self, value):
        self._timer.start(value, self)

    def _get_rects(self):
        size = Options.rect_size
        rects = []
        for row in range(self._model.row_count()):
            rects.append([
                QtCore.QRect(
                    size * row, size * column, size, size)
                for column in range(self._model.row_count())])
        return rects

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left:
            self.directionPressed.emit(Direction.left)
        if event.key() == QtCore.Qt.Key_Up:
            self.directionPressed.emit(Direction.up)
        if event.key() == QtCore.Qt.Key_Right:
            self.directionPressed.emit(Direction.right)
        if event.key() == QtCore.Qt.Key_Down:
            self.directionPressed.emit(Direction.down)
        if event.key() == QtCore.Qt.Key_Space:
            self.pauseRequested.emit()
        if event.key() == QtCore.Qt.Key_F2:
            self.restartGameRequested.emit()
        return QtGui.QWidget.keyPressEvent(self, event)

    def timerEvent(self, event):
        if event.timerId() == self._timer.timerId():
            self.timeSequenceFinished.emit()
        else:
            super().timerEvent(event)

    def adjust_geometry(self):
        self.resize(
            self._model.column_count() * Options.rect_size,
            self._model.row_count() * Options.rect_size)
        return self.geometry()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def paintEvent(self, event):
        if self._model is None:
            return

        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        painter.setPen(pen)

        for column, rects in enumerate(self._rects):
            for row, rect in enumerate(rects):
                value = self._model.get_value(row, column)
                if value == FieldSquareState.empty:
                    painter.setBrush(Options.colors['empty'])
                elif value == FieldSquareState.snake:
                    painter.setBrush(Options.colors['snake'])
                elif value == FieldSquareState.item:
                    painter.setBrush(Options.colors['item'])
                painter.drawRect(rect)

        if self._message_visible:
            painter.setBrush(Options.colors['message_background'])
            painter.drawRect(self.rect())
            painter.setPen(QtGui.QPen(Options.colors['message_text']))
            font = QtGui.QFont()
            font.setBold(True)
            font.setPixelSize(15)
            painter.setFont(font)
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter, self._message)
