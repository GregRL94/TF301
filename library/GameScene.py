# -*- coding: utf-8 -*-

'''
    File name: GameScene.py
    Author: Grégory LARGANGE
    Date created: 12/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 01/04/2021
    Python version: 3.8.1
'''

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsScene

from library import Island, Waypoint
from library.MathsFormulas import Geometrics as geo


class GameScene(QGraphicsScene):

    attachedGView = None
    nextShipID = 0
    nextIslandID = 0
    currentItem = None
    waypoints = []  # Deletable points
    trajpoints = []  # Permanent points

    def __init__(self, parent=None):
        super(GameScene, self).__init__(parent)

        self.innerBL = 0
        self.innerBR = 0
        self.innerBT = 0
        self.innerBB = 0
        self.innerArea = 0
        self.shipList = {}
        self.islandsList = []

    def mousePressEvent(self, mouseDown):
        if ((int(mouseDown.scenePos().x()) >= self.innerBL) & (int(mouseDown.scenePos().x()) <= self.innerBR)) &\
            ((int(mouseDown.scenePos().y()) >= self.innerBT) & (int(mouseDown.scenePos().y()) <= self.innerBB)):
            itemSelected = self.itemAt(mouseDown.scenePos(),
                                       self.attachedGView.transform())
            if (mouseDown.button() == Qt.RightButton) and not itemSelected:
                for item in self.selectedItems():
                    point = QPointF(int(mouseDown.scenePos().x()),
                                    int(mouseDown.scenePos().y()))
                    item.updatePath(point)
                mouseDown.accept()
            else:
                super(GameScene, self).mousePressEvent(mouseDown)
        else:
            super(GameScene, self).mousePressEvent(mouseDown)

    def setInnerMap(self, extPer, innerMap):
        self.innerBL = int(extPer * innerMap)
        self.innerBR = int(innerMap)
        self.innerBT = int(extPer * innerMap)
        self.innerBB = int(innerMap)

    def displayMap(self, obstaclesList):
        for obstacle in obstaclesList:
            self.currentItem = Island.Island(self, obstacle)
            thisIslandId = self.nextIslandID
            self.currentItem.setData(0, thisIslandId)
            self.currentItem.setData(1, "ISLAND")
            self.currentItem.setZValue(1)
            self.nextIslandID += 1
            self.addItem(self.currentItem)
            self.islandsList.append(self.currentItem)
            self.currentItem = None

    def shipsInDetectionRange(self, ship0ID, ship0Tag, ship0CenterSPos, ship0ScanRange):
        shipsInDRange = []

        for ship in self.shipList.values():
            if (ship.data(0) != ship0ID) & (ship.data(1) != ship0Tag):
                effS0ScanRange = ship0ScanRange - (ship0ScanRange - 1000) * ship.instant_vars["concealement"]
                shipNCenterSPos = geo.parallelepiped_Center(ship.pos(), ship.rect().width(),
                                                            ship.rect().height())
                dSNS0 = geo.distance_A_B(ship0CenterSPos, shipNCenterSPos)
                if dSNS0 <= effS0ScanRange:
                    shipsInDRange.append(ship)
        return shipsInDRange

    def dispGrid(self, step):
        for i in range(0, int(self.height()), step):
            self.addLine(0, i, int(self.width()), i, QPen(QColor("black"), 4))

        for i in range(0, int(self.width()), step):
            self.addLine(i, 0, i, self.height(), QPen(QColor("black"), 4))

        self.addLine(self.innerBL, self.innerBT, self.innerBR, self.innerBT, QPen(QColor("black"), 20))
        self.addLine(self.innerBL, self.innerBT, self.innerBL, self.innerBB, QPen(QColor("black"), 20))
        self.addLine(self.innerBR, self.innerBT, self.innerBR, self.innerBB, QPen(QColor("black"), 20))
        self.addLine(self.innerBL, self.innerBB, self.innerBR, self.innerBB, QPen(QColor("black"), 20))

    def dispPenalties(self, penaltyMap, step):
        baseColor = [255, 255, 255]

        for i, line in enumerate(penaltyMap):
            for j, penalty in enumerate(line):
                c_color = QColor(baseColor[0] * ((100 - penalty * 10) / 100),
                                baseColor[1] * ((100 - penalty * 10) / 100),
                                baseColor[2] * ((100 - penalty * 10) / 100))
                self.addRect(j * step, i * step, step, step, QPen(c_color), QBrush(c_color))

    def printPoint(self, point, size, color, permanent=False):
        c_point = Waypoint.Waypoint(point.x() - int(size / 2), point.y() - int(size / 2), size, size, color)
        if permanent:
            self.trajpoints.append(c_point)
        else:
            self.waypoints.append(c_point)
        self.addItem(c_point)

    def clearWaypoints(self):
        for item in self.waypoints:
            self.removeItem(item)
        self.waypoints.clear()

    def addShip(self, shipObject):
        thisShipId = self.nextShipID
        shipObject.setData(0, thisShipId)
        shipObject.setZValue(2)
        self.shipList[thisShipId] = shipObject
        self.nextShipID += 1
        self.addItem(shipObject)

    def clearMap(self):
        for item in self.islandsList:
            self.removeItem(item)
        self.islandsList.clear()
        self.nextIslandID = 0

        self.clearWaypoints()
        for item in self.trajpoints:
            self.removeItem(item)
        self.trajpoints.clear()

        self.clear()
        self.update()

    def destroyObject(self, _object):
        self.removeItem(_object)
        del _object
