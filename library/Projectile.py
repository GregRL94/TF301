# -*- coding: utf-8 -*-

'''
    File name: Projectile.py
    Author: Grégory LARGANGE
    Date created: 07/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 14/12/2020
    Python version: 3.8.1
'''

import math
import random

from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem


class Projectile(QGraphicsRectItem):
    """

    A class handling projectiles physics and behaviour.

    ...

    Attributes
    ----------
    m_range : int
        The maximum distance the projectile can travekl before exploding.

    cur_d : int
        The current distance the projectile has already traveled.

    Methods
    -------
    __init__(clock : MainClock, gameScene : GameScene, p_data : ProjectileData,
             _rotation : float, _range : int, _size : str, _type : str)
        The constructor of the class.

    rotate(_rotation : float)
        Applies _rotation to the projectile.

    move():
        Moves the projectile in the direction of its rotation according to its
        speed.

    range_rng()
        Returns a random distance within the target range +/- inaccuracy interval.

    v_decrease()
        Linear degression of the speed of the projectile.

    pen_decrease()
        Linear degression of the penetrative power of the projectile.

    paint(painter : QPainter, option : QOption, widget : QWidget)
        Instructions to draw the projectile on the main game scene.

    """

    m_range = 0
    cur_d = 0

    def __init__(self, clock, gameScene, p_data, _rotation, _range, _size="l", _type="AP"):
        """

        Parameters
        ----------
        clock : MainClock
            The main clock of the game.
        gameScene : gameScene.
            The main display of the game.
        p_data : ProjectileData
            A class holding projectile informations.
        _rotation : float
            A rotation to apply to the projectile.
        _range : int
            The distacce the projectile must travel.
        _size : string, optional
            A letter indicating the size of the shell. The default is "l".
            "s" => small
            "m" => medium
            "l" => large
        _type : string, optional
            A string indicating the type of the shell. The default is "AP".
            "AP" => Armor Piercing
            "HE" => High Explosive

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        super(Projectile, self).__init__(QRectF(0, 0, 0, 0))

        self.clock = clock
        self.gameScene = gameScene
        self._rotation = _rotation
        self._range = _range

        # Sets projectile parameters from p_data according to passed _size #
        if _size == "s":
            rect = QRectF(0, 0, p_data.w_h_ratio * p_data.size_values[0],
                          p_data.size_values[0])
            self.thk = p_data.thk_values[0]
            self.inacc = p_data.inaccuracy[0]
            self.m_range = p_data.ranges_shellSize[0]
            index = 0
        elif _size == "m":
            rect = QRectF(0, 0, p_data.w_h_ratio * p_data.size_values[1],
                          p_data.size_values[1])
            self.thk = p_data.thk_values[1]
            self.inacc = p_data.inaccuracy[1]
            self.m_range = p_data.ranges_shellSize[1]
            index = 1
        elif _size == "l":
            rect = QRectF(0, 0, p_data.w_h_ratio * p_data.size_values[2],
                          p_data.size_values[2])
            self.thk = p_data.thk_values[2]
            self.inacc = p_data.inaccuracy[2]
            self.m_range = p_data.ranges_shellSize[2]
            index = 2

        self.setRect(rect)
        self.eff_range = int(self.range_rng())

        if self._rotation != 0:
            self.rotate(self._rotation)

        self._type = _type
        # Sets projectile parameters from p_data according to _type #
        if self._type == "AP":
            self.v = self.v0 = p_data.speeds_shellType[0]
            self.dmg = p_data.damage_type[index][0]
            self.pen = self.p0 = p_data.pen_values[index][0]
            self.colors = [p_data.colors_values[0], p_data.colors_values[1]]
        else:
            self.v = self.v0 = p_data.speeds_shellType[1]
            self.dmg = p_data.damage_type[index][1]
            self.pen = self.p0 = p_data.pen_values[index][1]
            self.colors = [p_data.colors_values[2], p_data.colors_values[3]]
        self.v_dec = p_data.v_decreaseRate

        self.clock.clockSignal.connect(self.move)

    def rotate(self, _rotation):
        """

        Parameters
        ----------
        _rotation : float
            A rotation angle to apply in degrees.

        Returns
        -------
        None.

        Summary
        -------
        Sets the rotation of the projectile to _rotation.

        """
        self.setTransformOriginPoint(QPointF(self.rect().width() / 2,
                                             self.rect().height() / 2))
        self.setRotation(_rotation)

    def move(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Calculate the new position of the projectile according to its speed and
        rotation, and move the object to that new position.

        """
        rot_rad = math.radians(self._rotation)
        nextX = round(self.pos().x() + self.v*math.cos(rot_rad), 4)
        nextY = round(self.pos().y() + self.v*math.sin(rot_rad), 4)
        self.cur_d += int(math.sqrt(pow(nextX - self.pos().x(), 2) +\
                                pow(nextY - self.pos().y(), 2)))
        if (self.cur_d >= self.m_range) | (self.cur_d >= self.eff_range):
            self.gameScene.destroyObject(self)
        else:
            self.setPos(nextX, nextY)
            self.v_decrease()
            if self._type == "AP":
                self.pen_decrease()

    def range_rng(self):
        """

        Returns
        -------
        float
            The distance the projectile will travel before being destroyed.

        Summary
        -------
        Randomly generates a distance at which the projectile will explode.
        This random distance dpends on the inaccuracy parameter.

        """
        disp = self._range * self.inacc
        return random.uniform(self._range - disp, self._range + disp)

    def v_decrease(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Linera degression of the speed of the projectile.

        """
        self.v = round(self.v - self.v_dec, 4)

    def pen_decrease(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Linear degression of the projectile penetration.

        """
        self.pen = int(self.p0 + self.p0 * ((self.v - self.v0) / self.v0))

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
        painter.setBrush(QBrush(self.colors[0]))
        painter.setPen(QPen(self.colors[1], self.thk))
        painter.drawRect(self.rect())
