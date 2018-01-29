from PyQt4 import QtCore, QtGui
from color import ColorWheel, ColorsListView


class SimpleColorPaint(QtGui.QWidget):
    color = QtGui.QColor('#FF0000')

    def __init__(self, parent):
        super(SimpleColorPaint, self).__init__(parent)
        self.setMinimumSize(200, 25)

    def set_color(self, color):
        self.color = color
        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def paint(self, painter):
        pen = QtGui.QPen(QtGui.QColor('#000000'))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(self.color)
        painter.drawRect(self.rect())


class ColorExample(QtGui.QWidget):

    def __init__(self, parent=None):
        super(ColorExample, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self._color_wheel = ColorWheel(self)
        self._current_color = SimpleColorPaint(self)
        self._colors_list = ColorsListView(self)
        self._colors_list.set_rectangles_sizes(20)
        self._add = QtGui.QPushButton('add')

        self._color_wheel.currentColorChanged.connect(
            self._current_color.set_color)
        self._add.clicked.connect(self.on_add_clicked)

        self._layout = QtGui.QVBoxLayout(self)
        self._layout.addWidget(self._color_wheel)
        self._layout.addWidget(self._current_color)
        self._layout.addWidget(self._colors_list)
        self._layout.addWidget(self._add)

    def on_add_clicked(self):
        self._colors_list.set_colors(
            self._colors_list.colors() + [self._color_wheel.current_color()])


if __name__ == '__main__':
    app = QtGui.QApplication([])
    example = ColorExample()
    example.show()
    app.exec_()