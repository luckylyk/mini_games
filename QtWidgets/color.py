#!/usr/bin/env python

#############################################################################
#
# 2017
# Created by luckylyk
# this is free to use
#
# COLOR WHEEL and COLOR LIST SELECTOR
# for PyQt4 and python 3
# plateform tested Window
# (don't have linux or mac os to test, but it's probable cross plateform)
#
# the trigonometry functions are messy, so feel free to improve it !!
# love it are share it
#
#############################################################################


from PyQt4 import QtCore, QtGui
from math import sqrt, atan, degrees, tan, sin, cos, radians, fabs


class QTriangleRectangle(object):
    '''
    this class represent a Triangle rectangle... 
    there's three kwargs : a, b, c
    every kwarg take a QtCore.QPoint()
    representing the three point of the triangle
    there's no check if the triangle is rectangle. 
    If it's not, all the calculating methods are wrong... so becarefull
    '''

    def __init__(self, a=QtCore.QPoint(), b=QtCore.QPoint(), c=QtCore.QPoint()):
        self._qpoint_a = a
        self._qpoint_b = b
        self._qpoint_c = c

    def a(self):
        return self._qpoint_a

    def b(self):
        return self._qpoint_b

    def c(self):
        return self._qpoint_c

    def dist_a_b(self):
        return self._get_distance_from_two_point(
            self._qpoint_a, self._qpoint_b)

    def dist_b_c(self):
        return self._get_distance_from_two_point(
            self._qpoint_b, self._qpoint_c)

    def dist_a_c(self):
        return self._get_distance_from_two_point(
            self._qpoint_a, self._qpoint_c)

    def angle_a(self):
        return 180 - self.angle_b() - self.angle_c()

    def angle_b(self):
        degree = degrees(atan(
            self.dist_a_c() / self.dist_a_b()))
        return degree

    def angle_c(self):
        try:
            degree = degrees(atan(
                self.dist_a_b() / self.dist_a_c()))
        except ZeroDivisionError:
            degree = 90 * self.quarter()
        return degree

    def absolute_angle_c(self):
        quarter = self.quarter()
        if quarter == 0:
            return round(180.0 + self.angle_c(), 1)
        elif quarter == 1:
            return round(270.0 + (90 - self.angle_c()), 1)
        elif quarter == 2:
            return round(self.angle_c(), 1)
        elif quarter == 3:
            return fabs(round(90.0 + (90 - self.angle_c()), 1))

    def quarter(self):
        quarter = None
        if self.b().y() <= self.a().y() and self.b().x() < self.c().x():
            quarter = 0
        elif self.b().y() < self.a().y() and self.b().x() >= self.c().x():
            quarter = 1
        elif self.b().y() >= self.a().y() and self.b().x() > self.c().x():
            quarter = 2
        elif self.b().y() >= self.a().y() and self.b().x() <= self.c().x():
            quarter = 3

        return quarter

    def _get_distance_from_two_point(self, qpoint_a, qpoint_b):
        a = (qpoint_b.x() - qpoint_a.x())**2
        b = (qpoint_b.y() - qpoint_a.y())**2

        return sqrt(abs(a + b))


class ColorWheel(QtGui.QWidget):
    '''
    this Widget is a Color Wheel
    when the current color is changed, the widget emit the currentColorChanged
    signal
    It's also possible to get the current color by the methods
    current_color()
    '''
    currentColorChanged = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_clicked = False
        self._rect = QtCore.QRect(50, 50, 100, 100)
        self._current_color = QtGui.QColor(255, 255, 255)
        self._color_point = QtCore.QPoint(150, 50)
        self._current_tool = None
        self._angle = 180
        self.setFixedSize(200, 200)
        self.initUI()

    def keyPressEvent(self, event):
        self.set_current_color(0, 0, 0)

    def initUI(self):
        self._conicalGradient = QtGui.QConicalGradient(
            self.width() / 2, self.height() / 2, 180)
        self._conicalGradient.setColorAt(0.0, QtGui.QColor(0, 255, 255))
        self._conicalGradient.setColorAt(0.16, QtGui.QColor(0, 0, 255))
        self._conicalGradient.setColorAt(0.33, QtGui.QColor(255, 0, 255))
        self._conicalGradient.setColorAt(0.5, QtGui.QColor(255, 0, 0))
        self._conicalGradient.setColorAt(0.66, QtGui.QColor(255, 255, 0))
        self._conicalGradient.setColorAt(0.83, QtGui.QColor(0, 255, 0))
        self._conicalGradient.setColorAt(1.0, QtGui.QColor(0, 255, 255))

        self._vertical_gradient = QtGui.QLinearGradient(
            0, self._rect.top(),
            0, self._rect.top() + self._rect.height())
        self._vertical_gradient.setColorAt(0.0, QtGui.QColor(0, 0, 0, 0))
        self._vertical_gradient.setColorAt(1.0, QtGui.QColor(0, 0, 0))

        self._horizontal_gradient = QtGui.QLinearGradient(
            self._rect.left(), 0,
            self._rect.left() + self._rect.width(), 0)
        self._horizontal_gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def mousePressEvent(self, event):
        if self._rect.contains(event.pos()):
            self._current_tool = 'rect'
        else:
            self._current_tool = 'wheel'
        self.mouse_update(event)

    def mouseMoveEvent(self, event):
        self._is_clicked = True
        self.mouse_update(event)

    def mouse_update(self, event):
        if self._current_tool == 'rect':
            self.color_point = event.pos()
        else:
            triangle = QTriangleRectangle(
                a=QtCore.QPoint(event.pos().x(), self._get_center().y()),
                b=event.pos(),
                c=self._get_center())
            self._angle = triangle.absolute_angle_c()
        self.repaint()
        self.currentColorChanged.emit(self.current_color())

    def mouseReleaseEvent(self, event):
        self._is_clicked = False

    def paint(self, painter):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
        pen.setWidth(0)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)

        painter.setBrush(self._conicalGradient)
        painter.setPen(pen)
        painter.drawRoundedRect(
            6, 6, (self.width() - 12), (self.height() - 12),
            self.width(), self.height())

        painter.setBrush(self.palette().color(QtGui.QPalette.Background))
        painter.drawRoundedRect(
            25, 25, (self.width() - 50), (self.height() - 50),
            self.width(), self.height())

        self._horizontal_gradient.setColorAt(
            1.0, self._get_current_wheel_color())
        painter.setBrush(self._horizontal_gradient)
        painter.drawRect(self._rect)

        painter.setBrush(self._vertical_gradient)
        painter.drawRect(self._rect)

        pen.setColor(QtGui.QColor('#000000'))
        pen.setWidth(3)
        painter.setPen(pen)

        painter.drawLine(*self._get_points_by_angle())

        pen.setWidth(5)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen)
        painter.drawPoint(self._color_point)

    @property
    def color_point(self):
        return self._color_point

    @color_point.setter
    def color_point(self, point):
        if point.x() < self._rect.left():
            x = self._rect.left()
        elif point.x() > self._rect.left() + self._rect.width():
            x = self._rect.left() + self._rect.width()
        else:
            x = point.x()

        if point.y() < self._rect.top():
            y = self._rect.top()
        elif point.y() > self._rect.top() + self._rect.height():
            y = self._rect.top() + self._rect.height()
        else:
            y = point.y()

        self._color_point = QtCore.QPoint(x, y)

    def _get_current_wheel_color(self):
        value = 360 - self._angle
        if value is None:
            return None
        value = value / 360.0

        r, g, b = 255.0, 255.0, 255.0
        # RED
        if (value >= 0.0 and value <= 0.33) or (value >= 0.66 and value <= 1.0):
            if value >= 0.66 and value <= 0.83:
                factor = value - 0.66
                r = round(255 * (factor / .16))
            if (value > 0.0 and value < 0.16) or (value > 0.83 and value < 1.0):
                r = 255
            elif value >= 0.16 and value <= 0.33:
                factor = value - 0.16
                r = 255 - round(255 * (factor / .16))
        else:
            r = 0
        r = r if r <= 255 else 255
        r = r if r >= 0 else 0

        # GREEN
        if value >= 0.0 and value <= 0.66:
            if value >= 0.0 and value <= 0.16:
                g = round(255.0 * (value / .16))
            elif value > 0.16 and value < 0.5:
                g = 255
            if value >= 0.5 and value <= 0.66:
                factor = value - 0.5
                g = 255 - round(255.0 * (factor / .16))
        else:
            g = 0
        g = g if g <= 255.0 else 255.0
        g = g if g >= 0 else 0

        # BLUE
        if value >= 0.33 and value <= 1.0:
            if value >= 0.33 and value <= 0.5:
                factor = value - 0.33
                b = round(255 * (factor / .16))
            elif value > 0.5 and value < 0.83:
                b = 255.0
            if value >= 0.83 and value <= 1.0:
                factor = value - 0.83
                b = 255.0 - round(255.0 * (factor / .16))
        else:
            b = 0
        b = b if b <= 255 else 255
        b = b if b >= 0 else 0

        return QtGui.QColor(r, g, b)

    def _get_rect_relative(self, point):
        x = point.x() - self._rect.left()
        y = point.y() - self._rect.top()
        return QtCore.QPoint(x, y)

    def _get_center(self):
        return QtCore.QPoint(self.width() / 2, self.height() / 2)

    def current_color(self):
        point = self._get_rect_relative(self.color_point)
        x_factor = 1.0 - (point.x() / self._rect.width())
        y_factor = 1.0 - (point.y() / self._rect.height())

        r, g, b, a = self._get_current_wheel_color().getRgb()

        # fade to white
        differences = 255.0 - r, 255.0 - g, 255.0 - b
        r += round(differences[0] * x_factor)
        g += round(differences[1] * x_factor)
        b += round(differences[2] * x_factor)

        # fade to black
        r = round(r * y_factor)
        g = round(g * y_factor)
        b = round(b * y_factor)

        return QtGui.QColor(r, g, b)

    def _get_points_by_angle(self):
        angle = radians(self._angle)
        x = 100 + 77 * cos(float(angle))
        y = 100 + 77 * sin(float(angle))
        point_a = QtCore.QPoint(x, y)
        x = 100 + 93 * cos(float(angle))
        y = 100 + 93 * sin(float(angle))
        point_b = QtCore.QPoint(x, y)
        return (point_a, point_b)

    def set_current_color(self, color):
        [r, g, b] = color.getRgb()[:3]
        self._angle = 360.0 - (QtGui.QColor(r, g, b).getHslF()[0] * 360.0)
        self._angle = self._angle if self._angle != 720.0 else 0

        x = (((sorted([r, g, b], reverse=True)[
             0] - sorted([r, g, b])[0]) / 255.0) * self._rect.width()) + self._rect.left()

        y = (((255 - (sorted([r, g, b], reverse=True)[0])) / 255.0)
             * self._rect.height()) + self._rect.top()

        self._current_color = color
        self._color_point = QtCore.QPoint(x, y)
        self.repaint()


class ColorsListView(QtGui.QWidget):
    '''
    this widget represent a list off color QtGui.QColor
    by defaut is constructed with just a parent
    list of public methods ::
        set_rectangles_sizes(int)
            change the size of the colors rectangles
        set_colors(list_of_QtGui.QColor)
            set the color list to viez
        colors()  -->  [list of QtGui.QColor]
            to get the current setted colors
        current_color()  -->  QtGui.QColor
            to get the current color
    signals :
        currentColorChanged(QtGui.QColor)
            is emited when the current selected color is changed
    TO DO : the widget size management
    '''
    currentColorChanged = QtCore.pyqtSignal(QtGui.QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._colors = []
        self._rect_size = 25
        self._space_size = 5
        self._current_index = -1

    def set_rectangles_sizes(self, value):
        self._rect_size = value

    def _get_column_lenght(self):
        width = self.width()
        count = 0
        larging = 0
        while (larging) < width:
            larging += self._rect_size + self._space_size
            count += 1
        count = (count - 1)
        return count

    def _get_index_from_point(self, point):
        left, top = point.x(), point.y()
        column = left // (self._rect_size + self._space_size)
        row = top // (self._rect_size + self._space_size)
        if (column + 1) > self._get_column_lenght():
            return -1

        return (self._get_column_lenght() * (row)) + column

    def _change_color(self, event):
        self._current_index = self._get_index_from_point(event.pos())
        self.repaint()
        current_color = self.current_color()
        if current_color is not None:
            self.currentColorChanged.emit(self.current_color())

    def mousePressEvent(self, event):
        self._change_color(event)

    def mouseMoveEvent(self, event):
        self._change_color(event)

    def paintEvent(self, _):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.paint(painter)
        painter.end()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Plus:
            if self._rect_size < 150:
                self.set_rectangles_sizes(self._rect_size + 2)
                self.repaint()
        if event.key() == QtCore.Qt.Key_Minus:
            if self._rect_size > 5:
                self.set_rectangles_sizes(
                    self._rect_size - _current_wheel_color)
                self.repaint()

    def paint(self, painter):
        left, top = 0, 0
        pen = QtGui.QPen()

        for index, color in enumerate(self._colors):
            if index == self._current_index:
                pen.setWidth(3)
                pen.setColor(QtGui.QColor('#333333'))
            else:
                pen.setWidth(1)
                pen.setColor(QtGui.QColor('#000000'))

            painter.setPen(pen)
            painter.setBrush(color)
            painter.drawRect(left, top, self._rect_size, self._rect_size)
            left += self._rect_size + self._space_size
            if (index + 1) % self._get_column_lenght() == 0:
                left = 0
                top += self._rect_size + self._space_size

    def current_color(self):
        if len(self._colors) > self._current_index and self._current_index:
            return self._colors[self._current_index]

    def set_colors(self, colors):
        self._colors = colors
        self.repaint()

    def colors(self):
        return self._colors
