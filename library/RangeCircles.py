# -*- coding: utf-8 -*-

'''
    File name: RangeCircles.py
    Author: Grégory LARGANGE
    Date created: 19/03/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 22/03/2021
    Python version: 3.8.1
'''

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem


class RangeCircles(QGraphicsEllipseItem):

    thicknessCircle = 20
    outerColor = "black"
    innerColor = "black"

    def __init__(self, _pos, detectionRange, gunsRange, d_circle_color="black", d_gr_color="black"):
        super(RangeCircles, self).__init__(0, 0, 0, 0)

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)

        if max(detectionRange, gunsRange) is detectionRange:
            self.outerR = detectionRange
            self.innerR = gunsRange
            self.outerColor = d_circle_color
            self.innerColor = d_gr_color
        else:
            self.outerR = gunsRange
            self.innerR = detectionRange
            self.outerColor = d_gr_color
            self.innerColor = d_circle_color

        self.setRect(QRectF(0, 0, 2 * self.outerR, 2 * self.outerR))
        self.innerRect = QRectF(self.rect().top() + self.outerR - self.innerR,
                                self.rect().left() + self.outerR - self.innerR,
                                2 * self.innerR, 2 * self. innerR)
        self.setPos(_pos.x() - self.outerR, _pos.y() - self.outerR)
        print(self.pos())

    def _updatePos(self, newPos):
        """

        Parameters
        ----------
        newPos : QPointF
            The new position in the game scene of the center of the range circles.

        Returns
        -------
        None.

        Summary
        -------
        Updates the position of the range circles.

        """
        self.setPos(newPos.x() - self.outerR, newPos.y() - self.outerR)

    def paint(self, painter, option, widget=None):
        """

        Parameters
        ----------
        painter : QPainter
            A QPainter object.
        option : QtOption
            Options to apply to the QPainter.
        widget : QWidget, optional
            A QWidget object. The default is None.

        Returns
        -------
        None.

        Summary
        -------
        Instructions to draw the item on the game scene.

        """
        painter.setPen(QPen(QColor(self.outerColor), self.thicknessCircle, Qt.SolidLine))
        painter.drawEllipse(self.rect())

        painter.setPen(QPen(QColor(self.innerColor), self.thicknessCircle, Qt.SolidLine))
        painter.drawEllipse(self.innerRect)
