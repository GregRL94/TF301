# -*- coding: utf-8 -*-

'''
    File name: Projectile.py
    Author: Grégory LARGANGE
    Date created: 07/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 15/10/2020
    Python version: 3.8.1
'''

import math
import random

from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem


class Projectile(QGraphicsRectItem):

    projectileTag = ""
    size_values = [15, 22, 38]
    thk_values = [3, 5, 8]
    v_values = [150, 125]
    v_decreaseRate = 0.2
    m_range = 5000
    cur_d = 0
    dmg_values = [[210, 350], [420, 680], [720, 1080]]
    pen_values = [[150, 50], [300, 75], [400, 100]]
    colors_values = [QColor("lightGray"), QColor("gray"),
                     QColor("yellow"), QColor(255, 165, 0)]  # RGB value is orange

    def __init__(self, clock, gameScene, _rotation, _range, _size="l", _type="AP"):
        super(Projectile, self).__init__(QRectF(0, 0, 0, 0))

        self.clock = clock
        self.gameScene = gameScene
        self._rotation = _rotation
        self._range = _range

        if _size == "s":
            rect = QRectF(0, 0,
                               2 * self.size_values[0], self.size_values[0])
            self.thickness = self.thk_values[0]
            self.innacc = 0.025
            self.m_range = 9000
            sub_index = 0
        elif _size == "m":
            rect = QRectF(0, 0,
                               2 * self.size_values[1], self.size_values[1])
            self.thickness = self.thk_values[1]
            self.innacc = 0.0325
            self.m_range = 15000
            sub_index = 1
        elif _size == "l":
            rect = QRectF(0, 0,
                               2 * self.size_values[2], self.size_values[2])
            self.thickness = self.thk_values[2]
            self.innacc = 0.0375
            self.m_range = 21000
            sub_index = 2

        self.setRect(rect)
        self.eff_range = round(self.range_rng(), 4)

        if self._rotation != 0:
            self.rotate(self._rotation)

        self._type = _type
        if self._type == "AP":
            self.v = self.v0 = self.v_values[0]
            self.dmg = self.dmg_values[sub_index][0]
            self.pen = self.p0 = self.pen_values[sub_index][0]
            self.colors = [self.colors_values[0], self.colors_values[1]]
        else:
            self.v = self.v0 = self.v_values[1]
            self.dmg = self.dmg_values[sub_index][1]
            self.pen = self.p0 = self.pen_values[sub_index][1]
            self.colors = [self.colors_values[2], self.colors_values[3]]

        self.clock.clockSignal.connect(self.move)

    def rotate(self, _rotation):
        self.setTransformOriginPoint(QPointF(self.rect().width() / 2,
                                             self.rect().height() / 2))
        self.setRotation(_rotation)

    def move(self):
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
        disp = self._range * self.innacc
        f_range = random.uniform(self._range - disp, self._range + disp)
        return f_range

    def v_decrease(self):
        self.v = round(self.v - self.v_decreaseRate, 4)

    def pen_decrease(self):
        self.pen = int(self.p0 + self.p0 * ((self.v - self.v0) / self.v0))

    def setProjectileTag(self, tag):
        self.projectileTag = tag

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.colors[0]))
        painter.setPen(QPen(self.colors[1], self.thickness))
        painter.drawRect(self.rect())
