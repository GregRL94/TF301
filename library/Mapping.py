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

    def getGrid(self):
        return self.self.gameMap


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

        print("Looking for the neighbours of node:", node.iGrid, node.jGrid)
        print("Neighbours are in interval:", "(" + str(iMin) + "," + str(iMax) + ")", "on I",
              "(" + str(jMin) + "," + str(jMax) + ")", "on J")

        for i in range(iMin, iMax + 1):
            for j in range(jMin, jMax + 1):
                if (i == node.iGrid) & (j == node.jGrid):
                    print("Hit the node position, skipping...")
                    continue
                else:
                    print("Adding neighbour:", "neigh" + "(" + str(i) + "," + str(j) + ")")
                    neighbours.append(self.allNodes[i][j])
        for neighnode in neighbours:
            print(neighnode.iGrid, neighnode.jGrid, neighnode.traversible)
        print("")
        return neighbours

    def distanceB2Nodes(self, nodeA, nodeB):
        distJ = int(abs(nodeB.jGrid - nodeA.jGrid))  # distance on X
        distI = int(abs(nodeB.iGrid - nodeA.iGrid))  # distance on Y

        if distJ > distI:
            a = int(14 * distI + 10 * (distJ - distI))
        else:
            a = int(14 * distJ + 10 * (distI - distJ))
        print("Distance between node" + "(" + str(nodeA.iGrid) + "," + str(nodeA.jGrid) + ")",
              "and node" + "(" + str(nodeB.iGrid) + "," + str(nodeB.jGrid) + "):", a)
        return a

    def retracePath(self, startNode, endNode):
        print("Retracing path...")
        currentNode = endNode

        while currentNode != startNode:
            self.finalPath.append(currentNode)
            currentNode = currentNode.parent

        self.finalPath.reverse()
        print("<<< FINAL PATH >>>")
        for node in self.finalPath:
            print(node.iGrid, node.jGrid)
        print("<<<>>>")

    def findPath(self, startPos, targetPos):
        startNode = self.getNode(int(startPos.y() / 1000), int(startPos.x() / 1000))
        targetNode = self.getNode(int(targetPos.y() / 1000), int(targetPos.x() / 1000))
        print("======== STARTING PATHFINDING ========")
        print("Start node:", "node" + "(" + str(startNode.iGrid) + "," + str(startNode.jGrid) + ")")
        print("Target node:", "node" + "(" + str(targetNode.iGrid) + "," + str(targetNode.jGrid) + ")")
        print("...")

        self.openList.append(startNode)
        print("Added start node to openList")
        print("New openList length:", len(self.openList))
        print("")

        print("******* Pathfinding loop *******")
        while len(self.openList) > 0:
            self.currentNode = self.openList[0]
            print("1st node of open list:", "node" + "(" + str(self.currentNode.iGrid) + "," + str(self.currentNode.jGrid) + ")")
            print("Going through openList.", len(self.openList), "nodes in openList.")
            for i in range(1, len(self.openList)):
                print("Node", str(i + 1), "of", len(self.openList))
                if (self.openList[i].fCost() < self.currentNode.fCost()) |\
                    ((self.openList[i].fCost() == self.currentNode.fCost()) &\
                     (self.openList[i].hCost < self.currentNode.hCost)):
                    print("Found closer node. Updating current node.")
                    self.currentNode = self.openList[i]
            print("Finished going through openList.")
            print("NODE" + "(" + str(self.currentNode.iGrid) + "," + str(self.currentNode.jGrid) + ")", "IS GOING TO BE EVALUATED.")
            print("")

            print("Removing evaluated", "node" + "(" + str(self.currentNode.iGrid) + "," + str(self.currentNode.jGrid) + ")", "from openList...")
            self.openList.remove(self.currentNode)
            print("New openList length:", len(self.openList))

            print("Adding evaluated", "node" + "(" + str(self.currentNode.iGrid) + "," + str(self.currentNode.jGrid) + ")", "to closedList...")
            self.closedList.append(self.currentNode)
            print("New closedList length:", len(self.closedList))
            print("")

            if self.currentNode == targetNode:
                print("Reached target node!!!")
                self.retracePath(startNode, targetNode)
                return self.finalPath
            else:
                print("--- Neighbours evaluation loop ---")
                neighboursList = self.getNeighbours(self.currentNode)
                for node in neighboursList:
                    if (node.traversible is False) | (node in self.closedList):
                        stra = "Node" + "(" + str(node.iGrid) + "," + str(node.jGrid) + ") " + str(node.traversible) + " is skipped because not traversible."
                        strb = "Node" + "(" + str(node.iGrid) + "," + str(node.jGrid) + ") " + str(node.traversible) + " is skipped because already in closedList."
                        if node.traversible is False:
                            print(stra)
                        if node in self.closedList:
                            print(strb)
                        continue

                    newMoveCost = self.currentNode.gCost + self.distanceB2Nodes(self.currentNode, node)
                    print("New move cost for node" + "(" + str(node.iGrid) + "," + str(node.jGrid) + "):", newMoveCost)
                    if (newMoveCost < node.gCost) | (node not in self.openList):
                        print("New move cost is lower or node is not in openList.")
                        print("Computing new data for node" + "(" + str(node.iGrid) + "," + str(node.jGrid) + ")")
                        node.gCost = newMoveCost
                        node.hCost = self.distanceB2Nodes(node, targetNode)
                        node.parent = self.currentNode
                        print("Node" + "(" + str(node.iGrid) + "," + str(node.jGrid) + ")", "parent:",
                              "Node" + "(" + str(self.currentNode.iGrid) + "," + str(self.currentNode.jGrid) + ")")
                        if node not in self.openList:
                            print("Node" + "(" + str(node.iGrid) + "," + str(node.jGrid) + ")" , node.traversible, "is added to openList.")
                            self.openList.append(node)
                            print("New openList length:", len(self.openList))
                print("-----------------------------------")
                print("")
