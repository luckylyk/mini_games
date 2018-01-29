from PyQt4 import QtGui


class Options(object):
    field_size = (20, 20)
    rect_size = 10
    speed = 100
    colors = {
        'snake': QtGui.QColor(45, 45, 85),
        'empty': QtGui.QColor(125, 125, 125),
        'item': QtGui.QColor(255, 125, 125),
        'message_text': QtGui.QColor(125, 255, 125),
        'message_background': QtGui.QColor(125, 125, 125)}


class Direction(object):
    left = 0
    up = 1
    right = 2
    down = 3


class FieldSquareState(object):
    empty = 0
    snake = 1
    item = 2
