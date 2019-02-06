'''
this module contain all function used to generate a graphic element
'''

from PyQt4 import QtCore, QtGui


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
        rect.left() + rect.width() - rect.width() // 12, rect.top() + rect.height() // 2 - (rect.height() // 3))

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
