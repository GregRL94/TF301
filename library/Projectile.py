# -*- coding: utf-8 -*-

"""
    File name: Projectile.py
    Author: Grégory LARGANGE
    Date created: 07/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 13/07/2021
    Python version: 3.8.1
"""

import math
import random

from os import path

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsRectItem

from library.utils.Config import Config
from library.utils.MathsFormulas import Cinematics as cin


class Projectile(QGraphicsRectItem):
    """

    A class handling projectiles physics and behaviour.

    ...

    Attributes
    ----------
    cur_d : int
        The current distance the projectile has already traveled.

    Methods
    -------
    __init__(clock : MainClock, gameScene : GameScene, _rotation : float,
             _range : int, _size : str, _type : str)
        The constructor of the class.

    __init_instance_(_range : int, _rotation : float)
        Initialize variables for instantiation.

    rotate(_rotation : float)
        Applies _rotation to the projectile.

    move():
        Moves the projectile in the direction of its rotation according to its
        speed.

    range_rng()
        Returns a random distance within the target range +/- dispersion interval.

    v_decrease()
        Linear degression of the speed of the projectile.

    pen_decrease()
        Linear degression of the penetrative power of the projectile.

    paint(painter : QPainter, option : QOption, widget : QWidget)
        Instructions to draw the projectile on the main game scene.

    """

    cfg_dict, cfg_text = Config._file2dict(
        path.join(
            path.dirname(path.realpath(__file__)), "configs", "projectileConfig.py"
        )
    )
    cur_d = 0

    def __init__(self, clock, gameScene, _type="AP"):
        """

        Parameters
        ----------
        clock : MainClock
            The main clock of the game.
        gameScene : gameScene.
            The main display of the game.
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
        self._type = _type

        self.clock.clockSignal.connect(self.move)

    def __init_instance__(self, tag, _range, _rotation):
        """

        Parameters
        ----------
        _range : int
            The distance the shot should travel.
        _rotation : float
            The angle at which the shot should be fired.

        Returns
        -------
        None.

        Summary
        -------
        Initialize variables for instantiation.

        """
        rect = QRectF(0, 0, self._width, self._height)
        self.eff_range = int(self.range_rng(_range))
        self._rotation = _rotation

        self.setData(1, tag)
        self.setData(2, False)  # Considered an obstacle
        self.setData(3, "SHOT")

        if self._type == "AP":
            self.v = self.v0 = self.v_AP
            self._pen = self.p0 = self.pen_AP
            self.dmg = self.dmg_AP
            self.colors = self.colors_AP
        else:
            self.v = self.v0 = self.v_HE
            self._pen = self.p0 = self.pen_HE
            self.dmg = self.dmg_HE
            self.colors = self.colors_HE

        self.setRect(rect)
        if self._rotation != 0:
            self.rotate(self._rotation)

    @classmethod
    def small(cls, clock, gameScene, tag, _range, _rotation, _type="AP"):
        """

        Parameters
        ----------
        clock : GameClock
            The main clock of the game.
        gameScene : GameScene
            The main display of the game.
        _range : int
            The distance the shot should travel.
        _rotation : float
            The angle at which the shot should be fired.
        _type : string
            The type of the shot.

        Returns
        -------
        s_shot : Projectile
            The projectile.

        Summary
        -------
        Creates a shot using the 'small' configuration setup.

        """
        cfg_s = cls.cfg_dict["small"].copy()
        s_shot = cls(clock, gameScene, _type)
        s_shot.__dict__.update(cfg_s)
        s_shot.__init_instance__(tag, _range, _rotation)

        return s_shot

    @classmethod
    def medium(cls, clock, gameScene, tag, _range, _rotation, _type="AP"):
        """

        Parameters
        ----------
        clock : GameClock
            The main clock of the game.
        gameScene : GameScene
            The main display of the game.
        _range : int
            The distance the shot should travel.
        _rotation : float
            The angle at which the shot should be fired.
        _type : string
            The type of the shot.

        Returns
        -------
        s_shot : Projectile
            The projectile.

        Summary
        -------
        Creates a shot using the 'medium' configuration setup.

        """
        cfg_m = cls.cfg_dict["medium"].copy()
        m_shot = cls(clock, gameScene, _type)
        m_shot.__dict__.update(cfg_m)
        m_shot.__init_instance__(tag, _range, _rotation)

        return m_shot

    @classmethod
    def large(cls, clock, gameScene, tag, _range, _rotation, _type="AP"):
        """

        Parameters
        ----------
        clock : GameClock
            The main clock of the game.
        gameScene : GameScene
            The main display of the game.
        _range : int
            The distance the shot should travel.
        _rotation : float
            The angle at which the shot should be fired.
        _type : string
            The type of the shot.

        Returns
        -------
        s_shot : Projectile
            The projectile.

        Summary
        -------
        Creates a shot using the 'large' configuration setup.

        """
        cfg_l = cls.cfg_dict["large"].copy()
        l_shot = cls(clock, gameScene, _type)
        l_shot.__dict__.update(cfg_l)
        l_shot.__init_instance__(tag, _range, _rotation)

        return l_shot

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
        self.setTransformOriginPoint(self.rect().center())
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
        nextPos = cin.movementBy(self.pos(), self.v, rot_rad)
        self.cur_d += self.v
        if (self.cur_d >= self.m_range) | (self.cur_d >= self.eff_range):
            self.gameScene.destroyObject(self)
        else:
            self.setPos(nextPos)
            self.v_decrease()
            if self._type == "AP":
                self.pen_decrease()
            for item in self.collidingItems():
                if (item.data(3) == "SHIP") and (item.data(1) != self.data(1)):
                    self.onImpact(item)
                    self.gameScene.destroyObject(self)

    def range_rng(self, _range):
        """

        Returns
        -------
        int
            The distance the projectile will travel before being destroyed.

        Summary
        -------
        Randomly generates a distance at which the projectile will explode.
        This random distance depends on the accuracy parameter.

        """
        disp = _range * self.accy
        return random.uniform(_range - disp, _range)

    def v_decrease(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Linear degression of the speed of the projectile.

        """
        self.v = self.v - self.decc

    def pen_decrease(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Linear degression of the projectile penetration.

        """
        self._pen = int(self.p0 + self.p0 * ((self.v - self.v0) / self.v0))

    def onImpact(self, otherItem):
        """

        Parameters
        ----------
        otherItem : Ship
            A ship item.

        Returns
        -------
        None.

        Summary
        -------
        Evaluates and applies damage to the colliding ship.

        """
        if self._type == "HE":
            dmgHE = min(int((self._pen / otherItem.hull["armor"]) * self.dmg), self.dmg)
            otherItem.receiveDamage(dmgHE)
        else:
            if self._pen > otherItem.hull["armor"]:
                otherItem.receiveDamage(self.dmg)

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
        painter.setBrush(QBrush(QColor(self.colors[0])))
        painter.setPen(QPen(QColor(self.colors[1]), self.thk))
        painter.drawRect(self.rect())
