from PyQt5 import QtCore, QtWidgets
import sys


class BoardField():

    _name: str

    # row
    _y_cord: int

    _x_cord: int

    _resources = []

    _neighbours = []

    # ground == True or ocean == False
    _type: bool

    _ui_representation: QtWidgets.QLabel

    # 1 == Thasis, 2 == Hellas, 3 == Elysium ???
    _board_type: int

    def __init__(self, x, y, field: QtWidgets.QLabel):
        self._x_cord = x
        self._y_cord = y
        self._ui_representation = field
