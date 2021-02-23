# -*- coding: utf-8 -*-

'''
    File name: GameScene.py
    Author: Grégory LARGANGE
    Date created: 12/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 18/12/2020
    Python version: 3.8.1
'''

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem

from library import MathsFormulas, Island, Waypoint


class GameScene(QGraphicsScene):

    attachedGView = None
    nextShipID = 0
    nextIslandID = 0
    currentItem = None
    waypoints = []  ###### to be deleted afteer Astar debug

    def __init__(self, parent=None):
        super(GameScene, self).__init__(parent)
        self.geometrics = MathsFormulas.Geometrics()

        self.shipList = {}
        self.islandsList = []

    def mousePressEvent(self, mouseDown):
        itemSelected = self.itemAt(mouseDown.scenePos(),
                                   self.attachedGView.transform())
        if (mouseDown.button() == Qt.RightButton) and not itemSelected:
            for item in self.selectedItems():
                point = QPointF(int(mouseDown.scenePos().x()),
                                int(mouseDown.scenePos().y()))
                item.setDestination(point)
            mouseDown.accept()
        else:
            super(GameScene, self).mousePressEvent(mouseDown)

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
                effS0ScanRange = ship0ScanRange - (ship0ScanRange - 1000) * ship.concealement
                shipNCenterSPos = self.geometrics.parallelepiped_Center(
                    ship.pos(), ship.rect().width(), ship.rect().height())
                dSNS0 = self.geometrics.distance_A_B(ship0CenterSPos,
                                                     shipNCenterSPos)
                if dSNS0 <= effS0ScanRange:
                    shipsInDRange.append(ship)
        return shipsInDRange

    def dispGrid(self, steps):
        for i in range(0, int(self.height()), steps):
            self.addLine(0, i, int(self.width()), i, QPen(QColor("black"), 4))

        for i in range(0, int(self.width()), steps):
            self.addLine(i, 0, i, self.height(), QPen(QColor("black"), 4))

    def printPoint(self, point, size, color):
        c_point = Waypoint.Waypoint(point.x() - int(size / 2), point.y() - int(size / 2), size, size, color) ###### to be deleted afteer Astar debug
        # self.addEllipse(point.x() - int(size / 2), point.y() - int(size / 2), size, size,
        #                 QPen(QColor(color)))  # QBrush(QColor(color))
        self.waypoints.append(c_point) ###### to be deleted afteer Astar debug
        self.addItem(c_point) ###### to be deleted afteer Astar debug

    ###### to be deleted afteer Astar debug
    def clearWaypoints(self):
        for item in self.waypoints:
            self.removeItem(item)
        self.waypoints.clear()
    ######

    def addShip(self, shipObject, tag):
        thisShipId = self.nextShipID
        shipObject.setData(0, thisShipId)
        shipObject.setData(1, tag)
        shipObject.setZValue(2)
        self.shipList[thisShipId] = shipObject
        self.nextShipID += 1
        self.addItem(shipObject)

    def clearMap(self):
        for item in self.islandsList:
            self.removeItem(item)
        self.nextIslandID = 0
        self.islandsList.clear()
        self.update()

    def destroyObject(self, _object):
        self.removeItem(_object)
        del _object
