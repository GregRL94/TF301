# -*- coding: utf-8 -*-

'''
    File name: MathsFormulas.py
    Author: Grégory LARGANGE
    Date created: 16/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 10/12/2020
    Python version: 3.8.1
'''

import math

from PyQt5.QtCore import QPointF


class Geometrics():
    """

    A class implementing uselful euclidian geometrics functions.

    Attributes
    ----------
    None.

    Methods
    -------
    parallelepiped_Center(p_topLeft : QPointF, p_width : float, p_height : float)
        Returns the center of a parallelepiped.

    distance_A_B(pointA : QPointF, pointB : QPointF)
        Returns the distance betwenn pointA and pointB.

    pythagore(sideB : float, sideC : float)
        To be applied in a sqaure rectangle. Returns the hypothenuse of a triangle
        of sides A, B, C, where A is the hypothenuse.

    alKashi_side(sideB : float, sideC : float, angleInRad : float)
        Returns side A of a regular triangle of sides A, B, C and angle a opposite
        to side A.

    alKashi_angle_cos(sideA : float, sideB : float, sideC : float)
        Returns angle a (in radians) opposite to side A in any regular triangle
        of sides A, B, C.

    smallestAngle(targetAngleDeg : float, curAngleDeg : float)
        Returns the smallest angle possible to go from curAngleDeg to
        targetAngleDeg.

    checkSegmentsIntersect(segmentAB : list of QPointF, segmentCD : list of QPointF)
        Returns True if there is an intersection between segmentAB and segmentCD,
        False otherwise.

    """

    def parallelepiped_Center(self, p_topLeft, p_width, p_height):
        """

        Parameters
        ----------
        p_topLeft : QPointF
            The top left point of the parallelepiped.
        p_width : float
            The width of the parallelepiped.
        p_height : float
            The height of the parallelepiped.

        Returns
        -------
        p_center : QPointF
            The center of the parallelepiped.

        Summary
        -------
        Returns the center of the parallelepiped.

        """
        p_center = QPointF(p_topLeft.x() + p_width / 2,
                           p_topLeft.y() + p_height / 2)
        return p_center

    def distance_A_B(self, pointA, pointB):
        """

        Parameters
        ----------
        pointA : QPointF
            A point of the scene.
        pointB : QPointF
            A point of the scene.

        Returns
        -------
        distance : Float
            The distance between pointA and pointB.

        Summary
        -------
        Returns the distance between pointA and pointB.

        """
        distance = math.sqrt(
            pow(pointB.x() - pointA.x(), 2) +\
            pow(pointB.y() - pointA.y(), 2))
        return distance

    def pythagore(self, sideB, sideC):
        """

        Parameters
        ----------
        sideB : float
            The length of a side of the square angle of the triangle.
        sideC : float
            The length of an other side of the square angle of the triangle.

        Returns
        -------
        sideA : float
            The length of sideA, the hypothenuse of the triangle.

        Summary
        -------
        VALID FOR SQUARE TRIANGLES ONLY.
        returns the length of the hypothenuse of the triangle.

        """
        sideA = math.sqrt(pow(sideB, 2) + pow(sideC, 2))
        return sideA

    def alKashi_side(self, sideB, sideC, angleInRad):
        """

        Parameters
        ----------
        sideB : float
            The length of a side of the a angle of the triangle.
        sideC : float
            The length of an other side of the a angle of the triangle.
        angleInRad : float
            The reference angle used for calculations.

        Returns
        -------
        sideA : float
            The length of sideA of the triangle.

        Summary
        -------
        Returns the length of the sideA of the triangle.

        """
        sideA = math.sqrt(sideB ** 2 + sideC ** 2 - 2 * sideB * sideC * math.cos(angleInRad))
        return sideA

    def alKashi_angle_cos(self, sideA, sideB, sideC):
        """

        Parameters
        ----------
        sideA : float
            The length of sideA of the triangle.
        sideB : float
            The length of sideB of the triangle.
        sideC : float
            The length of sideC of the triangle.

        Returns
        -------
        angleInRad : float
            The value in radians of the anfle a opposite to sideA of the triangle.

        Summary
        -------
        Returns the angle a in radians.

        """
        angleInRad = math.acos(-(sideA ** 2 - (sideB ** 2 + sideC ** 2)) / (2 * sideB * sideC))
        return angleInRad

    def smallestAngle(self, targetAngleDeg, curAngleDeg):
        """

        Parameters
        ----------
        targetAngleDeg : float
            The target angle.
        curAngleDeg : float
            The initial angle.

        Returns
        -------
        diff : float
            The smallest angle.

        Summary
        -------
        Returns the smallest angle between curAngleDeg and targetAngleDeg.

        """
        offset = 360 if targetAngleDeg < curAngleDeg else -360
        diff1 = targetAngleDeg - curAngleDeg
        diff2 = targetAngleDeg - curAngleDeg + offset
        diff = diff1 if abs(diff1) < abs(diff2) else diff2
        return diff

    def checkSegmentsIntersect(self, segmentAB, segmentCD):
        """

        Parameters
        ----------
        segmentAB : list of QPointF
            A segment of the scene.
        segmentCD : list of QPointF
            A segment of the scene.

        Returns
        -------
        bool
            True if intersection, False otherwise.

        Summary
        -------
        Returns True if segmentAB and segmentCD have a real intersection, False
        otherwise.

        """
        XA = segmentAB[0].x()
        YA = segmentAB[0].y()
        XB = segmentAB[1].x()
        YB = segmentAB[1].y()

        XC = segmentCD[0].x()
        YC = segmentCD[0].y()
        XD = segmentCD[1].x()
        YD = segmentCD[1].y()

        IintX = [max(min(XA, XB), min(XC, XD)),
                 min(max(XA, XB), max(XC, XD))]

        if (max(XA, XB) < min(XC, XD)) | (min(XA, XB) > max(XC, XD)):
            return False

        if ((XA - XB) == 0) | ((XC - XD) == 0):
            if (XA - XB) == 0:
                if (XA < min(XC, XD)) | (XA > max(XC, XD)):
                    return False
                elif (min(YA, YB) > max(YC, YD)) | (max(YA, YB) < min(YC, YD)):
                    return False
                else:
                    return True
            else:
                if (XC < min(XA, XB)) | (XC > max(XA, XB)):
                    return False
                elif (min(YC, YD) > max(YA, YB)) | (max(YC, YD) < min(YA, YB)):
                    return False
                else:
                    return True

        # Following calculations based on line equation Y = AX + B
        AsegAB = (YA - YB) / (XA - XB)
        BsegAB = YB - AsegAB * XB

        AsegCD = (YC - YD) / (XC - XD)
        BsegCD = YD - AsegCD * XD

        # If both segment have same coef A then they are parallel
        if (AsegAB == AsegCD):
            return False

        # Following calculation based on fact that if I is intersection point
        # then YI = AsegAB * Xi + BsegAB = AsegCD * Xi + BsegCD
        XI = (BsegCD - BsegAB) / (AsegAB - AsegCD)

        if (XI >= IintX[0]) & (XI <= IintX[1]):
            return True
        else:
            return False


class Cinematics():
    """

    A class implementing uselful basic cinematic functions.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    movementBy(originPoint : QPointF, moveDistance : float, angleInRad : float)
        Calculates the new position of a point after a movement.

    brakeDistance(vinit : float, deceleration : float)
        Calculates the breaking distance of an object. Assumes a uniform linear
        movement.

    rotationRadius(speed : float, rotSpeedInD_s : float)
        Calculates the rotation radius of an object with a circular uniform
        movement.

    rotationCenters(centerPos : QPointF, heading : float, speed : float,
                    rotSpeedInD_s : float)
        Calculates the position of rotation centers of an object with a circular
        uniform movement.

    """

    def movementBy(self, originPoint, moveDistance, angleInRad):
        """

        Parameters
        ----------
        originPoint : QPOintF
            The initial position of the moving point.
        moveDistance : float
            The absolute ditance travelled by the point.
        angleInRad : float
            The angle of travel of the moving point.

        Returns
        -------
        newPoint : QPointF
            The position of the point after its movement.

        Summary
        -------
        Returns the new position of a point after a movement of moveDistance in
        the angleInRad direction.

        """
        newX = round(originPoint.x() + moveDistance * math.cos(angleInRad), 2)
        newY = round(originPoint.y() + moveDistance * math.sin(angleInRad), 2)
        newPoint = QPointF(newX, newY)
        return newPoint

    def brakeDistance(self, vinit, deceleration):
        """

        Parameters
        ----------
        vinit : float
            The initial velocity of the object.
        deceleration : float
            The constant deceleration of an object.

        Returns
        -------
        brakeD : float
            The breaking distance of the object.

        Summary
        -------
        Returns the breaking distance of an object breaking from the initial
        speed vinit with a deceleration deceleration.

        """
        brakeD = int((deceleration / 2) * (-vinit / deceleration) ** 2 - ((vinit ** 2) / deceleration))
        return brakeD

    def rotationRadius(self, speed, rotSpeedInD_s):
        """

        Parameters
        ----------
        speed : float
            The linear speed of the object.
        rotSpeedInD_s : float
            The rotation speed of the object.

        Returns
        -------
        radius : float
            The radius of the object's turn.

        Summary
        -------
        Returns the turn radius of an object with a linear speed speed and a
        rotation speed rotSpeedInD_s.

        """
        radius = int((180 * speed) / (math.pi * rotSpeedInD_s))
        return radius

    def rotationCenters(self, centerPos, heading, speed, rotSpeedInD_s):
        """

        Parameters
        ----------
        centerPos : QPointF
            The center of the object.
        heading : float
            The movement's direction of the object.
        speed : float
            The linear speed of the object.
        rotSpeedInD_s : float
            The rotation speed of the object.

        Returns
        -------
        list
            List of the rotation centers.

        Summary
        -------
        Calculates the position of the rotation centers on either side of the
        object, and returns a list with both of them.

        """
        radius = self.rotationRadius(speed, rotSpeedInD_s)

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
    """

    A class implementing controllers.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    proportional(targetValue : float, currentValue : float, maxGain : float,
                 customDiff : optional float)
        Applies a proportional controller to the input.

    """

    def proportional(self, targetValue, currentValue, maxGain, customDiff=None):
        """

        Parameters
        ----------
        targetValue : float
            The desired value.
        currentValue : float
            The current value.
        maxGain : float
            The maximum gain that can be applied to the input.
        customDiff : float, optional
            User can input here its custom error calculation. The default is None.

        Returns
        -------
        gain : float
            The calculated gain to apply.

        Summary
        -------
        Calculates the gain to apply to currentValue in order to reach target
        value while not exceeing maxGain.

        """
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
