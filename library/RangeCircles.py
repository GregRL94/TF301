# -*- coding: utf-8 -*-

"""
    File name: RangeCircles.py
    Author: Grégory LARGANGE
    Date created: 19/03/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 23/03/2021
    Python version: 3.8.1
"""

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem


class RangeCircles(QGraphicsEllipseItem):
    """

    A class to draw visualisation circles for a ship gun range and detection range.

    ...

    Attributes
    ----------
    thkC : int
        Thickness of the circles.

    outerColor : string
        The color of the outer circle.

    innerColor : string
        The color of the inner circle.

    Methods
    -------
    __init__(_pos : QPointF, det_range : int, guns_range : int,
             d_circle_color["black"] : string, d_gr_color["black"] : string)
        Constructor of the class.

    _updatePos(newPos : QPointF)
        Sets the current position of the item to newPos.

    paint(painter : QPainter, option : QOption, widget : QWidget)
        Instructions to draw the circle item on the main game scene.

    """

    thkC = 20
    outerColor = "black"
    innerColor = "black"

    def __init__(
        self, _pos, det_range, guns_range, d_circle_color="black", d_gr_color="black"
    ):
        """

        Parameters
        ----------
        _pos : QPointF
            The center of the ship the range circles are attached to.

        det_range : int
            The detection range of the ship the range circles are attached to.

        guns_range : int
            The detection range of the ship the range circles are attached to.

        d_circle_color : string
            The color of the detection circle as a string.

        d_gr_color : string
            The color of the guns range circle as a string.

        Returns
        -------
        None.

        Summary
        -------
        Constructor of the class.

        """
        super(RangeCircles, self).__init__(0, 0, 0, 0)

        self.setData(2, False)  # Not considered an obstacle
        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)

        if max(det_range, guns_range) is det_range:
            self.outerR = det_range
            self.innerR = guns_range
            self.outerColor = d_circle_color
            self.innerColor = d_gr_color
        else:
            self.outerR = guns_range
            self.innerR = det_range
            self.outerColor = d_gr_color
            self.innerColor = d_circle_color

        self.setRect(QRectF(0, 0, 2 * self.outerR, 2 * self.outerR))
        self.innerRect = QRectF(
            self.rect().top() + self.outerR - self.innerR,
            self.rect().left() + self.outerR - self.innerR,
            2 * self.innerR,
            2 * self.innerR,
        )
        self.setPos(_pos.x() - self.outerR, _pos.y() - self.outerR)

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
        painter.setPen(QPen(QColor(self.outerColor), self.thkC, Qt.SolidLine))
        painter.drawEllipse(self.rect())

        painter.setPen(QPen(QColor(self.innerColor), self.thkC, Qt.SolidLine))
        painter.drawEllipse(self.innerRect)
