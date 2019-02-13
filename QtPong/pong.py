import random
import math
from PyQt5 import QtWidgets, QtGui, QtCore
import draw
import geometry

DEFAULT_SPEED = 5


def compute_displacement(direction, speed, position, area=None):
    direction = math.radians(int(direction))
    x = position.x() + speed * math.cos(direction)
    y = position.y() + speed * math.sin(direction)
    if area is not None:
        x = x if x > area.left() else area.left()
        x = x if x < area.right() else area.right()
        y = y if y > area.top() else area.top()
        y = y if y < area.bottom() else area.bottom()
    return x, y


def reverse_angle(angle, horizontal=False):
    if horizontal:
        return remap_number(360 - angle, value=360)
    return remap_number(180 - angle, value=360)


def remap_number(number, value=10):
    ''' this method remap an int between 0 and value '''
    while number > value - 1:
        number -= value
    while number < 0:
        number += value
    return number


def diagonal(rect):
    return math.sqrt((rect.width() ** 2) + (rect.height() ** 2))


def compute_player_speed(positive, negative, reference_speed, speed_context):
    is_breaking = (
        (positive and reference_speed < 0) or
        (negative and reference_speed > 0))
    if is_breaking:
        return reference_speed / speed_context.break_factor
    is_accelerating = (
        (positive and reference_speed > 0) or
        (negative and reference_speed < 0))
    if is_accelerating:
        speed = abs(reference_speed)
        start_speed = speed_context.start_speed
        speed = start_speed if speed < start_speed else speed
        speed **= speed_context.acceleration_factor
        max_speed = speed_context.max_speed
        speed = max_speed if speed > max_speed else speed
        return speed if reference_speed > 0 else -speed
    # if not button pressed
    speed = abs(reference_speed) - speed_context.inertie_resistance
    speed = 0 if speed < 0 else speed
    return speed if reference_speed > 0 else -speed


class SpeedContext():
    def __init__(
            self, start_speed, acceletation_factor, max_speed,
            breaking_factor, intertie_resistance):
        self.start_speed = start_speed
        self.acceletation_factor = acceletation_factor
        self.max_speed = max_speed
        self.breaking_factor = breaking_factor
        self.inertie_resistance = intertie_resistance

# 360 / 0 = right
# 315 = right/up
# 270 = up
# 225 = up / left
# 180 = left
# 135 = left / down
# 90 = down
# 45 = right / down


def get_target_angle(directions):
    return None


def compute_acceleration_angle(vertical_speed, horizontal_speed, max_speed):
    return None


def compute_player_angle(angle, angle_acceleration, target_angle):
    return None


def test_get_target_angle():
    assert get_target_angle(['left', 'down']) == 135
    assert get_target_angle(['left', 'down']) == get_target_angle(['down', 'left'])
    assert get_target_angle(['down']) == 90
    assert get_target_angle(['right']) == 360
    assert get_target_angle(['right', 'up']) == 315
    assert get_target_angle(['right', 'down']) == 45


BUTTONS_DEFINITION = (
    {
        'up': QtCore.Qt.Key_Up,
        'down': QtCore.Qt.Key_Down,
        'left': QtCore.Qt.Key_Left,
        'right': QtCore.Qt.Key_Right
    },
    {
        'up': QtCore.Qt.Key_Z,
        'down': QtCore.Qt.Key_S,
        'left': QtCore.Qt.Key_Q,
        'right': QtCore.Qt.Key_D
    }
)


class PlayerPositionGenerator(object):
    def __init__(self, number, screen):
        self.speed_context = SpeedContext(
            start_speed=1.1,
            acceletation_factor=1.1,
            max_speed=25,
            breaking_factor=2,
            intertie_resistance=.5)

        self.number = number
        self.position = geometry.get_start_position(screen, player=number)
        self.angle = 0
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.buttons = []

    def __next__(self):
        self.vertical_speed = compute_player_speed(
            self.up, self.down, self.vertical_speed, self.speed_context)
        self.horizontal_speed = compute_player_speed(
            self.right, self.left, self.horizontal_speed, self.speed_context)

        target_angle = get_target_angle(self.buttons)
        acceleration_angle = compute_acceleration_angle(
            self.vertical_speed, self.horizontal_speed)
        self.angle = compute_player_angle(
            self.angle, acceleration_angle, target_angle)
        speed = round((self.vertical_speed + self.horizontal_speed) / 2)
        self.position = compute_displacement(self.angle, speed, self.position, area)
        yield self.position



class Widget(QtWidgets.QWidget):
    BASIC_SPEED = .0025

    def __init__(self):
        super(Widget, self).__init__(parent=None)
        self.timer = QtCore.QBasicTimer()
        self.timer.start(5, self)
        self.point = self.rect().center()
        self.speed = 5
        self.angle = random.randint(0, 360)
        self.ball_off = False

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            self.point = self.rect().center()

    def get_speed(self):
        return diagonal(self.rect()) * self.BASIC_SPEED

    def resizeEvent(self, e):
        self.speed = self.get_speed()

    def timerEvent(self, e):
        self.point = QtCore.QPointF(
            *compute_displacement(
                direction=self.angle,
                speed=self.speed,
                position=self.point))
        self.compute_bounce()
        self.repaint()

    def mouseMoveEvent(self, e):
        self.repaint()

    def paintEvent(self, e):
        painter = QtGui.QPainter()
        painter.begin(self)
        midline = geometry.extract_midline(self.rect())
        draw.draw_pitch(painter, self.rect(), midline)
        painter.drawText(QtCore.QPoint(5, 25), str(self.angle) + "°")
        pen = QtGui.QPen(QtGui.QColor('red'))
        pen.setWidth(3)
        painter.setPen(pen)
        ball = geometry.get_ball_rect(self.rect(), self.point)
        draw.draw_ball(painter, ball)
        painter.end()

    def compute_bounce(self):
        ball_in_frame = self.rect().contains(self.point.toPoint())
        if ball_in_frame and self.ball_off is True:
            self.ball_off = False
            return

        out_from_sides = (
            self.point.x() <= 0 or self.point.x() >= self.rect().width())
        if out_from_sides and self.ball_off is False:
            self.ball_off = True
            self.angle = reverse_angle(self.angle, horizontal=False)

        out_from_height = (
            self.point.y() <= 0 or self.point.y() >= self.rect().height())
        if out_from_height and self.ball_off is False:
            self.angle = reverse_angle(self.angle, horizontal=True)
            self.ball_off = True


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Widget()
    window.show()
    app.exec_()
