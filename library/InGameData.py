# -*- coding: utf-8 -*-

'''
    File name: InGameData.py
    Author: Grégory LARGANGE
    Date created: 19/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 10/12/2020
    Python version: 3.8.1
'''


class ProjectileData():
    """

    A class holding projectiles parameters

    ...

    Attributes
    ----------
    speeds_shellType : list of int
        A list of speeds per shell type.

    ranges_shellSize : list of int
        A list of ranges per shell size.

    damage_type : list of lists of int
        A list per shell size of sublist of damage per shell type.

    pen_values : list of sublists of int
        A list per shell size of sublist of penetration per shell type.

    Methods
    -------
    None

    """

    speeds_shellType = [150, 125]
    ranges_shellSize= [9000, 15000, 21000]
    damage_type = [[210, 350], [420, 680], [720, 1080]]
    pen_values = [[150, 50], [300, 75], [400, 100]]


class RadioCommunications():
    """

    A class implementing a form of 'radio communication' between ships of the
    same fleet.

    ...

    Attributes
    ----------
    alliedShips : list of Ships
        A list of all allied ships on the scene.

    ennemyShips : list of Ships
        A list of all ennemy ships on the scene.

    alliedDetectedShips : list of Ships
        A list of all ennemy ships detected by all allied ships.

    ennemyDetectedShips : list of Ships
        A list of all allied ships detected by all ennemy ships.

    radioCommsRate : int
        The period between two radio emmissions.

    Methods
    -------
    __init__(mainClock : MainClock, gameScene : GameScene)
        The constructor of the class.

    updateShipLists()
        Updates the allied ship list and the ennemy ship list.

    fixedUpdate()
        Performs a radio communication each radioCommsRate.

    gatherDetectedShips()
        Gather all ennemy ships detected by allied ships and all ennemy ships 
        detected by allied ships.

    transmitDetectedShips()
        Transmit to each allied ship a list of all detected ennemy ships.
        Transmit to each ennemy ship a list of all detected allied ships.

    """

    alliedShips = []
    ennemyShips = []
    alliedDetectedShips = []
    ennemyDetectedShips = []
    radioCommsRate = 19

    def __init__(self, mainClock, gameScene):
        """

        Parameters
        ----------
        mainClock : MainClock
            The main clock of the game.
        gameScene : GameScene
            the main display for the game.

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        self.gameScene = gameScene
        self.clock = mainClock
        self.next_radioComm = self.radioCommsRate

        self.clock.clockSignal.connect(self.fixedUpdate)

    def updateShipLists(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Updates the alliedShips list and the ennmyShips list.

        """
        for ship in self.gameScene.shipList.values():
            if ship.shipTag == "ALLY":
                self.alliedShips.append(ship)
            else:
                self.ennemyShips.append(ship)

    def fixedUpdate(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Synchronisation with the game main clock. Each radioCommsRate, performs
        the 'radio comm' process.
        
        """
        if self.next_radioComm <= 0:
            self.gatherDetectedShips()
            self.transmitDetectedShips()
            self.next_radioComm = self.radioCommsRate
        else:
            self.next_radioComm -= 1

    def gatherDetectedShips(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Gather all detected ships from all ships, for allies and ennemies
        respectively.

        """
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
        """

        Returns
        -------
        None.

        Summary
        -------
        Transmit to all ships the list of all detected ships, for allies and
        ennemies respectively.

        """
        for alliedShip in self.alliedShips:
            alliedShip.receiveRadioComm(self.alliedDetectedShips)
        for ennemyShip in self.ennemyShips:
            ennemyShip.receiveRadioComm(self.ennemyDetectedShips)
