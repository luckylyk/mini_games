from PyQt4 import QtCore, QtGui
from controller import SnakeGame


if __name__ == '__main__':
    application = QtGui.QApplication([])
    game = SnakeGame()
    game.show(title='Snake Game in Python')
    game.start()
    application.exec_()
