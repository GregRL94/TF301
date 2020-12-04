# -*- coding: utf-8 -*-

'''
    File name: MapGenerator.py
    Author: Grégory LARGANGE
    Date created: 25/11/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 03/12/2020
    Python version: 3.8.1
'''

import random

from PyQt5.QtCore import QPoint, QPointF
from PyQt5.QtGui import QPolygonF
from library import MathsFormulas


class MapGenerator():

    curO = 0
    nObstacles = 0
    emergencyBreak = 500

    def __init__(self, mapWidth, mapHeight, mapSlicing):
        self.geometrics = MathsFormulas.Geometrics()
        self.gameMap = []

        self.mapW = mapWidth
        self.mapH = mapHeight
        self.mapA = self.mapW * self.mapH
        self.mapS = mapSlicing

        self.maxO = 0.0
        self.minObsW = 0
        self.maxObsW = 0
        self.minObsH = 0
        self.maxObsH = 0
        self.minD2O = 0

        self.minPoints = 4
        self.maxPoints = 10

        self.polygonsList = []

        for i in range(int((self.mapW / self.mapS))):
            self.gameMap.append([])
            for j in range(int((self.mapH / self. mapS))):
                self.gameMap[i].append(0)

        # print("######### MAP INITIALISATION ########")
        # for element in self.gameMap:
        #     print(element)
        # print("#####################################")

    def setMapParameters(self, maxObstruction, minObstWidth, maxObstWidth,
                         minObstHeight, maxObstHeight, minD2Obstacles):
        self.maxO = maxObstruction
        self.minObsW = minObstWidth
        self.maxObsW = maxObstWidth
        self.minObsH = minObstHeight
        self.maxObsH = maxObstHeight
        self.minD2O = minD2Obstacles

    def resetMap(self):
        if len(self.gameMap) > 0:
            for i in range(len(self.gameMap)):
                for j in range(len(self.gameMap[0])):
                    self.gameMap[i][j] = 0

        self.curO = 0
        self.nObstacles = 0
        self.polygonsList.clear()

    def checkAvailableSpace(self, coordList):
        x = coordList[0]
        y = coordList[1]
        w = coordList[2]
        h = coordList[3]

        c_tlx = x - self.minD2O
        if c_tlx < 0:
            c_tlx = 0

        c_tly = y - self.minD2O
        if c_tly < 0:
            c_tly = 0

        c_brx = x + w + self.minD2O
        if c_brx > len(self.gameMap) - 1:
            c_brx = len(self.gameMap) - 1
            w = c_brx - x

        c_bry = y + h + self.minD2O
        if c_bry > len(self.gameMap[0]) - 1:
            c_bry = len(self.gameMap[0]) - 1
            h = c_bry - y

        for i in range(c_tlx, c_brx + 1):
            for j in range(c_tly, c_bry + 1):
                if self.gameMap[i][j] != 0:
                    # print("An obstacle is already present in the desired area.")
                    return None

        # print("The obstacle:", y, x, h, w, "can be placed")
        return [x, y, w, h]

    def randomObstacle(self):
        tlx = random.randint(0, len(self.gameMap) - 1 - self.minObsW)
        tly = random.randint(0, len(self.gameMap[0]) - 1 - self.minObsH)
        w = random.randint(self.minObsW, self.maxObsW) - 1 # we account for the existing line x
        h = random.randint(self.minObsH, self.maxObsH) - 1 # we account for the existing column y

        brx = tlx + w
        if brx > len(self.gameMap) - 1:
            brx = len(self.gameMap) - 1
            w = brx - tlx

        bry = tly + h
        if bry > len(self.gameMap[0]) - 1:
            bry = len(self.gameMap[0]) - 1
            h = bry - tly

        # print("Proposed obstacle:", tlx, tly, w, h)
        return [tlx, tly, w, h]

    def randomPoint(self, x, y, width, height):
        px = random.randint(x, x + width) * 1000
        py = random.randint(y, y + height) * 1000
        return QPoint(px, py)

    def generateObstacle(self, ObsAsList):
        x = ObsAsList[0]
        y = ObsAsList[1]
        w = ObsAsList[2]
        h = ObsAsList[3]
        poly = QPolygonF()

        for i in range(x, x + w):
            for j in range(y, y + h):
                self.gameMap[i][j] = 1

        polyTL = QPoint(y * 1000, x * 1000)
        polyBL = QPoint(y * 1000, (x + w) * 1000)
        polyBR = QPoint((y + h) * 1000, (x + w) * 1000)
        polyTR = QPoint((y + h) * 1000, x * 1000)

        poly<<polyTL<<polyBL<<polyBR<<polyTR

        # The randomized number of points the polygon of the obstacle will be made of.
        #nPoints = random.randint(self.minPoints, self.maxPoints)
        #c = -1
        # Construction of the polygon
        # for n in range(nPoints):
        #     c += 1
        #     point = self.randomPoint(x, y, w, h)
        #     poly<<point
        #     if c > 2:
        #         thisSegment = [poly.at(c - 1), poly.at(c)]
        #         segments  = []
        #         for p in range(c - 2):
        #             q = p + 1
        #             if q > poly.count() - 1:
        #                 break
        #             segments.append([poly.at(p), poly.at(q)])
        #         for segment in segments:
        #             intersect = self.geometrics.checkSegmentsIntersect(thisSegment, segment)
        #             if intersect is True:
        #                 point = self.randomPoint(x, y, w, h)
        #                 poly.replace(c, point)

        self.polygonsList.append(poly)

        oA = w * h
        oP = oA / self.mapA
        # print("Obstruction percentage of this obtacle:", oP)
        self.curO += oP
        # print("New current obstruction of the map:", self.curO)

    def generateMap(self):
        safeCounter = 0

        while self.curO < self.maxO:
            curObs = self.randomObstacle()
            okObs = self.checkAvailableSpace(curObs)
            if okObs is not None:
                self.generateObstacle(okObs)
                self.nObstacles += 1
            safeCounter += 1
            if safeCounter > self.emergencyBreak:
                break

        print("Finished map generation. Map obstruction:", self.curO)
        print("######## FINAL MAP ############")
        for element in self.gameMap:
            print(element)
        print("###############################")

        return self.polygonsList


class Node():

    iGrid = 0
    jGrid = 0
    traversible = True
    gCost = 0
    hCost = 0

    def __init__(self, iGrid, jGrid, traversible):
        self.iGrid = iGrid
        self.jGrid = jGrid
        self.traversible = traversible

    def setGcost(self, gCostValue):
        self.gCost = gCostValue

    def setHcost(self, hCostValue):
        self.hCost = hCostValue

    def fCost(self):
        return self.gCost + self.hCost

    def retScenePos(self):
        return QPointF(self.jGrid * 1000, self.iGrid * 1000)


class Astar():

    def __init__(self, gameMap):
        self.allNodes = []
        self.openList = []
        self.closedList = []
        self.currentNode = None
        self.currentNodeParent = None

        for i in range(len(gameMap)):
            self.allNodes.append([])
            for j in range(len(gameMap[0])):
                traversible = True if (gameMap[i][j] == 0) else False
                self.allNodes[i].append(Node(i, j, traversible))

    def getNode(self, i, j):
        return self.allNodes[i][j]

    def getNeighbours(self, node):
        iMin = node.iGrid - 1
        iMax = node.iGrid + 1
        jMin = node.jGrid - 1
        jMax = node.jGrid + 1
        neighbours = []

        if node.iGrid == 0:
            iMin = node.iGrid
        if node.iGrid == (len(self.allNodes) - 1):
            iMax = node.iGrid
        if node.jGrid == 0:
            jMin = node.jGrid
        if node.jGrid == (len(self.allNodes[0]) - 1):
            jMax = node.jGrid

        for i in range(iMin, iMax + 1):
            for j in range(jMin, jMax + 1):
                if (i == node.iGrid) & (j == node.jGrid):
                    continue
                else:
                    neighbours.append(self.allNodes[i][j])

        return neighbours

    def findPath(self, startPos, targetPos):
        startNode = self.getNode(int(startPos.y() / 1000),
                                 int(startPos.x() / 1000))
        targetNode = self.getNode(int(targetPos.y() / 1000),
                                  int(targetPos.x() / 1000))

        self.openList.append(startNode)