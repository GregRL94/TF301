# -*- coding: utf-8 -*-

'''
    File name: RangeCircles.py
    Author: Grégory LARGANGE
    Date created: 19/03/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 19/03/2021
    Python version: 3.8.1
'''

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush, QCursor
from PyQt5.QtWidgets import QGraphicsEllipseItem


class RangeCircles(QGraphicsEllipseItem):

    def __init__(self, _pos, r1, r2, color1, color2):
        super(RangeCircles, self).__init__(_pos.x() - r1, _pos.y() - r1, 2 * r1, 2 * r1)
        self.innerR = r2
        self.innerColor = color2
        self.outerColor = color1

    def paint(self, painter, option, widget=None):
        True