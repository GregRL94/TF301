# -*- coding: utf-8 -*-

'''
    File name: MathsFormulas.py
    Author: Grégory LARGANGE
    Date created: 16/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 16/10/2020
    Python version: 3.8.1
'''

import math

from PyQt5.QtCore import QPointF

class Geometrics():

    def parallelepiped_Center(self, p_topLeft, p_width, p_height):
        p_center = QPointF(p_topLeft.x() + p_width / 2,
                           p_topLeft.y() + p_height / 2)
        return p_center

    def distance_A_B(self, pointA, pointB):
        distance = math.sqrt(
            pow(pointB.x() - pointA.x(), 2) +\
            pow(pointB.y() - pointA.y(), 2))
        return distance

    def pythagore(self, sideB, sideC):
        sideA = math.sqrt(pow(sideB, 2) + pow(sideC, 2))
        return sideA

    def alKashi_side(self, sideB, sideC, angleInRad):
        sideA = math.sqrt(sideB ** 2 + sideC ** 2 - 2 * sideB * sideC * math.cos(angleInRad))
        return sideA

    def alKashi_angle_cos(self, sideA, sideB, sideC):
        angleInRad = math.acos(-(sideA ** 2 - (sideB ** 2 + sideC ** 2)) / (2 * sideB * sideC))
        return angleInRad

    def smallestAngle(self, targetAngleDegrees, currentAngleDegrees):
        offset = 360 if targetAngleDegrees < currentAngleDegrees else -360
        diff1 = targetAngleDegrees - currentAngleDegrees
        diff2 = targetAngleDegrees - currentAngleDegrees + offset
        diff = diff1 if abs(diff1) < abs(diff2) else diff2
        return diff


class Cinematics():

    def movementBy(self, originPoint, moveDistance, angleInRad):
        newX = round(originPoint.x() + moveDistance * math.cos(angleInRad), 2)
        newY = round(originPoint.y() + moveDistance * math.sin(angleInRad), 2)
        newPoint = QPointF(newX, newY)
        return newPoint

    def brakeDistance(self, vinit, deceleration):
        brakeD = int((deceleration / 2) * (-vinit / deceleration) ** 2 - ((vinit ** 2) / deceleration))
        return brakeD

    def rotationRadius(self, speed, rotationSpeedInD_s):
        radius = int((180 * speed) / (math.pi * rotationSpeedInD_s))
        return radius

    def rotationCenters(self, centerPos, heading, speed, rotationSpeedInD_s):
        radius = self.rotationRadius(speed, rotationSpeedInD_s)

        h_l = math.radians(heading - 90)
        h_r = math.radians(heading + 90)
        port_rc_x = round(centerPos.x() + radius * math.cos(h_l), 2)
        port_rc_y = round(centerPos.y() + radius * math.sin(h_l), 2)
        port_rc = QPointF(port_rc_x, port_rc_y)

        starport_rc_x = round(centerPos.x() + radius * math.cos(h_r), 2)
        starport_rc_y = round(centerPos.y() + radius * math.sin(h_r), 2)
        starport_rc = QPointF(starport_rc_x, starport_rc_y)

        return [port_rc, starport_rc]


class Controllers():

    def proportional(self, targetValue, currentValue, maxGain, customDiff=None):
        staticGain = 1

        if customDiff is None:
            diff = targetValue - currentValue
        else:
            diff = customDiff

        gain = staticGain * diff
        if gain < -maxGain:
            gain = -maxGain
        elif gain > maxGain:
            gain = maxGain

        return gain