# -*- coding: utf-8 -*-

'''
    File name: MapGenerator.py
    Author: Grégory LARGANGE
    Date created: 25/11/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 27/11/2020
    Python version: 3.8.1
'''

import random

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon
from library import MathsFormulas, Island


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

        c = 0
        for i in range(int((self.mapW / self.mapS) + 1)):
            self.gameMap.append([])
            for j in range(int((self.mapH / self. mapS) + 1)):
                self.gameMap[c].append(0)
            c += 1

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

        # print("The obstacle:", x, y, w, h, "can be placed")
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
        poly = QPolygon()

        for i in range(x, x + w + 1):
            for j in range(y, y + h + 1):
                self.gameMap[i][j] = 1

        # The randomized number of points the polygon of the obstacle will be made of.
        nPoints = random.randint(self.minPoints, self.maxPoints)
        c = -1
        # Construction of the polygon
        for n in range(nPoints):
            c += 1
            point = self.randomPoint(x, y, w, h)
            poly<<point
            if c > 2:
                thisSegment = [poly.at(c - 1), poly.at(c)]
                segments  = []
                for p in range(c - 2):
                    q = p + 1
                    if q > poly.count() - 1:
                        break
                    segments.append([poly.at(p), poly.at(q)])
                for segment in segments:
                    intersect = self.geometrics.checkSegmentsIntersect(thisSegment, segment)
                    if intersect is True:
                        point = self.randomPoint(x, y, w, h)
                        poly.replace(c, point)

        for point in poly:
            print(point)
        print("")

        oA = w * h
        oP = oA / self.mapA
        # print("Obstruction percentage of this obtacle:", oP)
        self.curO += oP
        # print("New current obstruction of the map:", self.curO)

    def generateMap(self):
        safeCounter = 0

        while self.curO < self.maxO:
            curO = self.randomObstacle()
            okO = self.checkAvailableSpace(curO)
            if okO is not None:
                self.generateObstacle(okO)
                self.nObstacles += 1
            safeCounter += 1
            if safeCounter > self.emergencyBreak:
                break

        print("Finished map generation. Map obstruction:", self.curO)
        print("######## FINAL MAP ############")
        for element in self.gameMap:
            print(element)
        print("###############################")
