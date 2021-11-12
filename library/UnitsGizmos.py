# -*- coding: utf-8 -*-

"""
    File name: UnitsGizmos.py
    Author: Grégory LARGANGE
    Date created: 19/03/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 29/09/2021
    Python version: 3.8.1
"""

from PyQt5.QtCore import QRect, Qt, QRectF
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsRectItem,
)


class RangeCirclesGizmo(QGraphicsEllipseItem):
    """

    A class to draw visualisation circles for a ship gun range and detection range.

    ...

    Attributes
    ----------
    thkc : int
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

    update_pos(newPos : QPointF)
        Sets the current position of the item to newPos.

    paint(painter : QPainter, option : QOption, widget : QWidget)
        Instructions to draw the circle item on the main game scene.

    """

    thkc = 20
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
        super(RangeCirclesGizmo, self).__init__(0, 0, 0, 0)

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

    def update_pos(self, newPos):
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
        painter.setPen(QPen(QColor(self.outerColor), self.thkc, Qt.SolidLine))
        painter.drawEllipse(self.rect())

        painter.setPen(QPen(QColor(self.innerColor), self.thkc, Qt.SolidLine))
        painter.drawEllipse(self.innerRect)


class LineGizmo(QGraphicsLineItem):
    """

    A class to draw a visualisation line from point_a to point_b.

    ...

    Attributes
    ----------
    thkc : int
        Thickness of the line.

    color : string
        The color of the line.


    Methods
    -------
    __init__(point_a : QPointF, point_b : QPointF)
        Constructor of the class.

    update_line(new_point_a : QPointF, new_point_b : QPointF)
        Redraws the line according to new_point_a and new_point_b.

    """

    thkc = 20

    def __init__(self, point_a, point_b, color):
        """

        Parameters
        ----------
        point_a : QpointF
            The starting point of the line.

        point_b : QPointF
            The end point of the line.

        Returns
        -------
        None.

        Summary
        -------
        Constructor.

        """
        super(LineGizmo, self).__init__(0, 0, 0, 0)

        self.setData(2, False)  # Not considered an obstacle
        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)

        self.setLine(point_a.x(), point_a.y(), point_b.x(), point_b.y())
        self.setPen(QPen(QColor(color), self.thkc, Qt.SolidLine))

    def update_line(self, new_point_a, new_point_b=None):
        """

        Parameters
        ----------
        new_point_a : QPointF
            The new starting point of the line.

        new_point_b : QPointF
            The new end point of the line.

        Returns
        -------
        None.

        Summary
        -------
        Redraw the line according to new_point_a and new_point_b.

        """
        if new_point_b is not None:
            self.setLine(
                new_point_a.x(), new_point_a.y(), new_point_b.x(), new_point_b.y()
            )
        else:
            self.setLine(
                new_point_a.x(),
                new_point_a.y(),
                new_point_a.x() + 1,
                new_point_a.y() + 1,
            )


class RectangleGizmo(QGraphicsRectItem):
    """

    A class to draw a visualisation rectangle at a given position, with width and height.

    ...

    Attributes
    ----------
    thkc : int
        Thickness of the line.

    color : string
        The color of the rectangle.


    Methods
    -------
    __init__(pos : QPointF, width: int, height : int)
        Constructor of the class.

    update_rect(newPos: QPointF, angle : float)
        Redraws the rectangle at newPos with rotation angle.

    rotate(angle : float)
        Rotates the rectangle by angle.

    paint(painter : QPainter, option : QOption, widget : QWidget)
        Instructions to draw the rectangle item on the main game scene.

    """

    thkc = 20
    color = "black"

    def __init__(self, _pos, width, height, color):
        """

        Parameters
        ----------
        point_a : QpointF
            The starting point of the line.

        point_b : QPointF
            The end point of the line.

        Returns
        -------
        None.

        Summary
        -------
        Constructor.

        """
        super(RectangleGizmo, self).__init__(0, 0, 0, 0)

        self.setData(2, False)  # Not considered an obstacle
        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsFocusable, False)

        self.setRect(QRectF(0, 0, width, height))
        self.setPos(_pos)
        self.color = color

    def update_rect(self, new_pos, angle):
        """

        Parameters
        ----------
        new_point : QPointF
            The new position of the rectangle.
        angle : float
            The angle to rotate the rectangle to.

        Returns
        -------
        None.

        Summary
        -------
        Updates the position and the rotation of the rectangle gizmo.

        """
        self.setPos(new_pos)
        self._rotate(angle)

    def _rotate(self, angle):
        """

        Parameters
        ----------
        angle : float
            The angle to rotate the rectangle to.

        Returns
        -------
        None.

        Summary
        -------
        Rotates the rectangle gizmo.

        """
        self.setTransformOriginPoint(self.rect().center())
        self.setRotation(angle)

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
        painter.setPen(QPen(QColor(self.color), self.thkc, Qt.DotLine))
        painter.drawRect(self.rect())
