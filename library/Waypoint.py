# -*- coding: utf-8 -*-

from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem


class Waypoint(QGraphicsEllipseItem):

    def __init__(self, x, y, w, h, color, parent=None):
        super(Waypoint, self).__init__(x, y, w, h)
        self.color = color
    
    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(QColor(self.color), 20))
        painter.drawEllipse(self.rect())
        