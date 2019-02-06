'''
QtMineSweeper
using PyQt4 and python 3
author: luckylyk
licence: free
Description:
this is an example code to make a minesweeper game.
as Windows 10 remove the minesweeper game from is game libs, i rescripted it in
python
'''


from PyQt4 import QtGui
from controller import MineSweeperController
from core import FieldSize
from random import choice
from model import MineSweeperModel
from view import MineSweeperFieldView


def start_minesweeper(size, number_of_bombs):
    '''
    function to start a minesweeper controller with options
    '''
    app = QtGui.QApplication([])
    controller = MineSweeperController(
        model=MineSweeperModel(),
        view=MineSweeperFieldView(),
        size=size,
        number_of_bombs=number_of_bombs)
    controller.show()
    app.exec_()


if __name__ == '__main__':
    height = choice(range(10, 50))
    width = choice(range(10, 50))
    bombs = choice(range((height * width) // 60, (height * width) // 6))
    start_minesweeper(size=FieldSize(width, height), number_of_bombs=bombs)
