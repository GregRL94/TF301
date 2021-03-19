# -*- coding: utf-8 -*-

'''
    File name: Gun_Turret.py
    Author: Grégory LARGANGE
    Date created: 12/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 19/03/2020
    Python version: 3.8.1
'''

from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem


class Waypoint(QGraphicsEllipseItem):
    """

    A pure display class to vizualize trajectory or path points.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    __init__(x : int, y : int, w: int, h : int, color : string,
             parent[None] : QObject)
        Constructor.

    paint(painter : QPainter, option : QtOption, widget[None]: QWidget)
        Draws the item

    """

    def __init__(self, x, y, w, h, color, parent=None):
        """

        Parameters
        ----------
        x : int
            X position of the point rect.
        y : int
            Y position of the point rect.
        w : int
            width of the point rect.
        h : int
            height of the point rect.
        color : string
            The color of the point as a string.
        parent[Default=None] : QObject
            The parent item of the point

        Returns
        -------
        None

        Summary
        -------
        The constructor of the class.

        """
        super(Waypoint, self).__init__(x, y, w, h)
        self.color = color

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
        painter.setPen(QPen(QColor(self.color), 20))
        painter.drawEllipse(self.rect())
