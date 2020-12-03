# -*- coding: utf-8 -*-

'''
    File name: Obstacle.py
    Author: Grégory LARGANGE
    Date created: 27/11/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 27/11/2020
    Python version: 3.8.1
'''

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush, QCursor
from PyQt5.QtWidgets import QGraphicsPolygonItem


class Island(QGraphicsPolygonItem):

    thickness = 100
    colorInner = QColor(107, 134, 68)
    colorBorder = QColor(108, 98, 79)

    def __init__(self, parentScene, polygon):
        super(Island, self).__init__()

        self.parentScene = parentScene
        self.poly = polygon
        self.setPolygon(self.poly)
        self.setAcceptHoverEvents(True)

    def hoverMoveEvent(self, mousePos):
        self.setCursor(QCursor(Qt.ForbiddenCursor))

    def paint(self, painter, option, widget=None):
        # Always draw the polygon core polygon
        painter.setBrush(QBrush(self.colorInner))
        painter.setPen(QPen(self.colorBorder, self.thickness, Qt.SolidLine))
        painter.drawPolygon(self.polygon())
