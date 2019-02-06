

from PyQt5 import QtGui


STYLE = {
    "pitch-background": "black",
    "pitch-border-color": "white",
    "pitch-border-width": 3.0,
    "pitch-midline-color": "grey",
    "pitch-midline-width": 3.0,
    "player-color": "white",
    "ball-color": "white",

}


def draw_pitch(painter, rect, midline=None, custom_style=None):
    style = STYLE.copy()
    style.update(custom_style)
    pen = QtGui.QPen(QtGui.QColor(style["pitch-border-color"]))
    pen.setWidthF(style["pitch-border-width"])
    painter.setPen(pen)
    brush = QtGui.QBrush(QtGui.QColor(style["pitch-background"]))
    painter.setBrush(brush)
    painter.drawRect(rect)
    if midline is None:
        return
    pen = QtGui.QPen(QtGui.QColor(style["pitch-midline-color"]))
    pen.setWidthF(style["pitch-midline-width"])
    painter.setPen(pen)
    painter.drawLine(midline)


def draw_player(painter, rect, custom_style=None):
    style = STYLE.copy()
    style.update(custom_style)
    color = style["player-color"]
    draw_rect_without_border(painter, rect, color)


def draw_ball(painter, rect, custom_style=None):
    style = STYLE.copy()
    style.update(custom_style)
    color = style["ball-color"]
    draw_rect_without_border(painter, rect, color)


def draw_rect_without_border(painter, rect, color):
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
    painter.setPen(pen)
    brush = QtGui.QBrush(QtGui.QColor(color))
    painter.setBrush(brush)
    painter.drawRect(rect)