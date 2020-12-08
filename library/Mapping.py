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

from PyQt5.QtCore import QPoint
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
                    return None
        return [x, y, w, h]

    def randomObstacle(self):
        tlx = random.randint(0, len(self.gameMap) - 1 - self.minObsW)
        tly = random.randint(0, len(self.gameMap[0]) - 1 - self.minObsH)
        w = random.randint(self.minObsW, self.maxObsW)
        h = random.randint(self.minObsH, self.maxObsH)

        brx = tlx + w
        if brx > len(self.gameMap) - 1:
            brx = len(self.gameMap) - 1
            w = brx - tlx

        bry = tly + h
        if bry > len(self.gameMap[0]) - 1:
            bry = len(self.gameMap[0]) - 1
            h = bry - tly
        return [tlx, tly, w, h]

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

        self.polygonsList.append(poly)

        oA = w * h
        oP = oA / self.mapA
        self.curO += oP

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
    xPos = 0
    yPos = 0
    traversible = True
    gCost = 0
    hCost = 0
    parent = None

    def __init__(self, iGrid, jGrid, traversible):
        self.iGrid = iGrid
        self.jGrid = jGrid
        self.xPos = self.jGrid * 1000
        self.yPos = self.iGrid * 1000
        self.traversible = traversible

    def fCost(self):
        return int(self.gCost + self.hCost)


class Astar():

    def __init__(self, gameMap):
        self.allNodes = []
        self.openList = []
        self.closedList = []
        self.finalPath = []
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

    def distanceB2Nodes(self, nodeA, nodeB):
        distJ = int(abs(nodeB.jGrid - nodeA.jGrid))  # distance on X
        distI = int(abs(nodeB.iGrid - nodeA.iGrid))  # distance on Y

        if distJ > distI:
            return int(14 * distI + 10 * (distJ - distI))
        return int(14 * distJ + 10 * (distI - distJ))

    def retracePath(self, startNode, endNode):
        currentNode = endNode

        while currentNode != startNode:
            self.finalPath.append(currentNode)
            currentNode = currentNode.parent

        self.finalPath.reverse()

    def findPath(self, startPos, targetPos):
        startNode = self.getNode(int(startPos.y() / 1000), int(startPos.x() / 1000))
        targetNode = self.getNode(int(targetPos.y() / 1000), int(targetPos.x() / 1000))

        self.openList.append(startNode)

        while len(self.openList) > 0:
            self.currentNode = self.openList[0]
            for i in range(1, len(self.openList)):
                if (self.openList[i].fCost() < self.currentNode.fCost()) |\
                    ((self.openList[i].fCost() == self.currentNode.fCost()) &\
                     (self.openList[i].hCost < self.currentNode.hCost)):
                    self.currentNode = self.openList[i]

            self.openList.remove(self.currentNode)
            self.closedList.append(self.currentNode)

            if self.currentNode == targetNode:
                self.retracePath(startNode, targetNode)
                return self.finalPath
            else:
                neighboursList = self.getNeighbours(self.currentNode)
                for node in neighboursList:
                    if (node.traversible is False) | (node in self.closedList):
                        continue

                    newMoveCost = self.currentNode.gCost + self.distanceB2Nodes(self.currentNode, node)
                    if (newMoveCost < node.gCost) | (node not in self.openList):
                        node.gCost = newMoveCost
                        node.hCost = self.distanceB2Nodes(node, targetNode)
                        node.parent = self.currentNode
                        if node not in self.openList:
                            self.openList.append(node)


class HEAPItem():

    def __init__(self):
        self.heapIndex = 0
        self.sFCost = 0

    def compareTo(self, otherHEAPItem):
        if otherHEAPItem.sFCost < self.sFCost:
            return 1
        elif otherHEAPItem.sFCost == self.sFCost:
            return 0
        else:
            return -1


class HEAP():

    def __init__(self, maxHeapSize):
        self.items = []
        self.itemCount = 0

    def addItem(self, _heapItem):
        _heapItem.heapIndex = self.itemCount
        self.items.append(_heapItem)
        self.sortUp(_heapItem)
        self.itemCount += 1

    def sortUp(self, _heapItem):
        parentIndex = int((_heapItem.heapIndex - 1 ) / 2)

        while True:
            parentItem = self.items[parentIndex]
            if _heapItem.compareTo(parentItem) > 0:
                self.swap(_heapItem, parentItem)
            else:
                break

    def swap(self, _heapItemA, _heapItemB):
        self.items[_heapItemA.heapIndex] = _heapItemB
        self.items[_heapItemB.heapIndex] = _heapItemA
        tmp_itemAIndex = _heapItemA.heapIndex
        _heapItemA.heapIndex = _heapItemB.heapIndex
        _heapItemB.heapIndex = tmp_itemAIndex