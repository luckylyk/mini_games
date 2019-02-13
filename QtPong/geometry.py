
import math
from PyQt5 import QtCore


PLAYER_WIDTH_SCREEN_RATIO = .02
PLAYER_HEIGHT_SCREEN_RATIO = .1
BALL_SIZE_SCREEN_RATIO = .01


def get_playable_area(screen, player_number=0):
    assert player_number in [0, 1]
    playable_area = QtCore.QRectF(screen)
    left = screen.left() if player_number == 0 else screen.center.x()
    right = screen.center.x() if player_number == 0 else screen.right()
    playable_area.setLeft(left)
    playable_area.setRight(right)
    return playable_area


def get_start_position(screen, player=1):
    y = screen.y()
    offset = screen.width() / 10
    x = screen.left() + offset if player == 1 else screen.right() - offset
    return QtCore.QPointF(x, y)


def extract_midline(screen):
    return QtCore.QLine(
        QtCore.QPoint(int(screen.center().x()), 0),
        QtCore.QPoint(int(screen.center().x()), int(screen.height())))


def get_player_rect(screen, position):
    width = screen.width() * PLAYER_WIDTH_SCREEN_RATIO
    height = screen.height() * PLAYER_HEIGHT_SCREEN_RATIO
    player_rect = QtCore.QRectF(0, 0, width, height)
    player_rect.moveCenter(position)
    return player_rect


def get_ball_rect(screen, position):
    radius = diagonal(screen) * BALL_SIZE_SCREEN_RATIO
    rect = QtCore.QRectF(0, 0, radius, radius)
    rect.moveCenter(position)
    return rect


def diagonal(rect):
    return math.sqrt((rect.width() ** 2) + (rect.height() ** 2))