# -*- coding: utf-8 -*-

'''
    File name: Target.py
    Author: Grégory LARGANGE
    Date created: 15/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 19/03/2020
    Python version: 3.8.1
'''

from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem


class Target(QGraphicsRectItem):
    """

    ##### THIS CLASS IS OBSOLETE #####

    """

    shipID = 0
    shipTag = "ENNEMY"
    concealement = 0.1

    def __init__(self, rect, clock, v):
        super(Target, self).__init__(rect)

        self.clock = clock
        self.v = v

        self.clock.clockSignal.connect(self.fixed_update)

    def setID(self, shipId):
        self.shipID = shipId

    def fixed_update(self):
        nextX = self.x() + self.v
        nextY = self.y() - self.v / 4

        self.setPos(nextX, nextY)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor("red")))
        painter.setPen(QPen(QColor("darkRed"), 10))
        painter.drawRect(self.rect())
