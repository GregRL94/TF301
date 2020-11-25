# -*- coding: utf-8 -*-

'''
    File name: InGameData.py
    Author: Grégory LARGANGE
    Date created: 19/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 19/10/2020
    Python version: 3.8.1
'''


class ProjectileData():

    speeds_shellType = [150, 125]
    ranges_shellSize= [9000, 15000, 21000]
    damage_type = [[210, 350], [420, 680], [720, 1080]]
    pen_values = [[150, 50], [300, 75], [400, 100]]


class RadioCommunications():

    alliedShips = []
    ennemyShips = []
    alliedDetectedShips = []
    ennemyDetectedShips = []
    radioCommsRate = 19

    def __init__(self, mainClock, gameScene):
        self.gameScene = gameScene
        self.clock = mainClock
        self.next_radioComm = self.radioCommsRate

        self.clock.clockSignal.connect(self.fixedUpdate)

    def updateShipLists(self):
        for ship in self.gameScene.shipList.values():
            if ship.shipTag == "ALLY":
                self.alliedShips.append(ship)
            else:
                self.ennemyShips.append(ship)

    def fixedUpdate(self):
        if self.next_radioComm <= 0:
            self.gatherDetectedShips()
            self.transmitDetectedShips()
            self.next_radioComm = self.radioCommsRate
        else:
            self.next_radioComm -= 1

    def gatherDetectedShips(self):
        tmpADS = []
        tmpEDS = []

        for ship in self.alliedShips:
            shipDSList = ship.detected_ships
            tmpADS = tmpADS + shipDSList
        tmpADS = list(dict.fromkeys(tmpADS))

        for ship in self.ennemyShips:
            shipDSList = ship.detected_ships
            tmpEDS = tmpEDS + shipDSList
        tmpEDS = list(dict.fromkeys(tmpADS))

        self.alliedDetectedShips = tmpADS
        self.ennemyDetectedShips = tmpEDS

    def transmitDetectedShips(self):
        for alliedShip in self.alliedShips:
            alliedShip.receiveRadioComm(self.alliedDetectedShips)
        for ennemyShip in self.ennemyShips:
            ennemyShip.receiveRadioComm(self.ennemyDetectedShips)
