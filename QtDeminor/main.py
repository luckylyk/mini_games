'''
QtDeminor
using PyQt4 and python 3
author: luckylyk
licence: free
Description:
this is an example code to make a deminor game.
as Windows 10 remove the deminor game from is game libs, i rescripted it in
python
'''


from PyQt4 import QtGui
from controller import DeminorController
from core import FieldSize
from random import choice
from model import DeminorModel
from view import DeminorFieldView


def start_deminor(size, number_of_bombs):
    '''
    function to start a deminor controller with options
    '''
    app = QtGui.QApplication([])
    controller = DeminorController(
        model=DeminorModel(),
        view=DeminorFieldView(),
        size=size,
        number_of_bombs=number_of_bombs)
    controller.show()
    app.exec_()


if __name__ == '__main__':
    height = choice(range(10, 50))
    width = choice(range(10, 50))
    bombs = choice(range((height * width) // 60, (height * width) // 6))
    start_deminor(size=FieldSize(width, height), number_of_bombs=bombs)
