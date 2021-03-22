# -*- coding: utf-8 -*-

'''
    File name: RangeCircles.py
    Author: Grégory LARGANGE
    Date created: 19/03/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 19/03/2021
    Python version: 3.8.1
'''

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem


class RangeCircles(QGraphicsEllipseItem):

    thicknessCircle = 20
    outerColor = "black"
    innerColor = "black"

    def __init__(self, r1, r2):
        super(RangeCircles, self).__init__(0, 0, 0, 0)
        self.outerR = max(r1, r2)
        self.innerR = min(r1, r2)
        self.setRect(QRectF(0, 0, 5000, 5000))
        #self.innerRect = QRectF(self.rect().top() + self.outerR - self.innerR,
        #                        self.rect().left() + self.outerR - self.innerR,
        #                        2 * self.innerR, 2 * self. innerR)
        self.innerRect = QRectF(0, 0, 2500, 2500)

    def setColors(self, _outerColor, _innerColor):
        self.outerColor = _outerColor
        self.innerColor = _innerColor

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(QColor(self.outerColor), self.thicknessCircle, Qt.SolidLine))
        painter.drawEllipse(self.rect())

        painter.setPen(QPen(QColor(self.innerColor), self.thicknessCircle, Qt.SolidLine))
        painter.drawEllipse(self.innerRect)
