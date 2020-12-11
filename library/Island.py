# -*- coding: utf-8 -*-

'''
    File name: Obstacle.py
    Author: Grégory LARGANGE
    Date created: 27/11/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 11/12/2020
    Python version: 3.8.1
'''

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush, QCursor
from PyQt5.QtWidgets import QGraphicsPolygonItem


class Island(QGraphicsPolygonItem):
    """

    A class implementing obstacles that can be displayed by the game scene.

    ...

    Attributes
    ----------
    thickness : int
        The thickness of an obstacle border.

    colorInner : QColor
        The color of the inner part of the obstacle.

    colorBorder : QColor
        The color of the border of the obstacle.

    Methods
    -------
    __init__(parentScene : GameScene, polygon : QPolygonF)
        The constructor of the class.

    hoverMoveEvent(mousePos)
        Changes the appearance of the cursor when hovering above the item.

    paint(painter : QPainter, option : QtOption, widget=None)
        Instruction for the GameScene to draw the object.

    """

    thickness = 100
    colorInner = QColor(107, 134, 68)
    colorBorder = QColor(108, 98, 79)

    def __init__(self, parentScene, polygon):
        """

        Parameters
        ----------
        parentScene : GameScene
            The mqin scene the object will be displayed on.
        polygon : QPolygonF
            The polygon defining the item geometry.

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        super(Island, self).__init__()

        self.parentScene = parentScene
        self.poly = polygon
        self.setPolygon(self.poly)
        self.setAcceptHoverEvents(True)

    def hoverMoveEvent(self, mousePos):
        """

        Parameters
        ----------
        mousePos : MouseEvvent
            A signal indicating that the mouse cursor was moved.

        Returns
        -------
        None.

        Summary
        -------
        Display a forbidden cursor when hovering above the item.

        """
        self.setCursor(QCursor(Qt.ForbiddenCursor))

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
        # Always draw the polygon core polygon
        painter.setBrush(QBrush(self.colorInner))
        painter.setPen(QPen(self.colorBorder, self.thickness, Qt.SolidLine))
        painter.drawPolygon(self.polygon())
