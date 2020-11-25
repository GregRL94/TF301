# -*- coding: utf-8 -*-

'''
    File name: Ship.py
    Author: Grégory LARGANGE
    Date created: 09/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 25/11/2020
    Python version: 3.8.1
'''


class MapGenerator():

    curO = 0
    nObstacles = 0
    gameMap = []

    def __init__(self, mapWidth, mapHeight, mapSlicing, maxObstruction, minObstacleArea, maxObstacleArea, minD2Obstacles):
        self.mapW = mapWidth
        self.mapH = mapHeight
        self.mapS = mapSlicing
        self.maxO = maxObstruction
        self.minObsA = minObstacleArea
        self.maxObsA = maxObstacleArea
        self.minD2O = minD2Obstacles

        c = 0
        for i in range(0, int((self.mapW / self.mapS) + 1)):
            self.gameMap.append([])
            for j in range(0, int((self.mapH / self. mapS) + 1)):
                self.gameMap[c].append(0)
            c += 1