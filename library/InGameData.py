# -*- coding: utf-8 -*-

"""
    File name: InGameData.py
    Author: Grégory LARGANGE
    Date created: 19/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 14/07/2021
    Python version: 3.8.1
"""


class TechsData:
    """

    A class holding technologies parameters.

    ...

    Attributes
    ----------
    gun_tech_acc : list of float
        A list of accuracy values per gun technology level.

    fc_tech_e : list of float
        A list of speed estimation error per fire control technology level.

    pc_tech_reduc : list of float
        A list of error reduction percentage per cycle, per computer technology level.

    radar_tech_aug : list of float
        A list of base radar range augmentation percentage per radar technology level.

    Methods
    -------
    None.

    """

    # The higher the index in the lists the higher is the associated tech level #

    gun_tech_acc = [
        1.0,
        0.8,
        0.6,
    ]  # The higher the tech, the more accurate the guns
    fc_tech_e = [
        0.3,
        0.2,
        0.1,
    ]  # The higher the tech, the lower the error on target speed
    pc_tech_reduc = [
        0.1,
        0.25,
        0.5,
    ]  # The higher the tech, the faster the fc error is reduced
    radar_tech_aug = [
        0,
        0.25,
        0.5,
    ]  # The higher the tech, the higher the boost on the base radar range
    fc_correction_rate = (
        150  # The rate at which the error on target speed estimation is reduced.
    )
    cost_per_tech = [2500, 5000]  # Cost tech1 -> tech2, tech2 -> tech3

    # Projectile data #
    shot_innac = [0.0667, 0.0834, 0.0952]
    speeds_shellType = [150, 125]  # Element 0 is AP, 1 is HE
    damage_type = [
        [240, 360],
        [480, 720],
        [800, 1200],
    ]  # A shell of size can always be of type AP or HE
    pen_values = [
        [150, 50],
        [300, 75],
        [400, 100],
    ]  # HE shells have much lower penetration power than AP shells


class RadioCommunications:
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

        self.alliedShips = []
        self.ennemyShips = []
        self.alliedDetectedShips = []
        self.ennemyDetectedShips = []

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
            if ship.data(1) == "ALLY":
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
            shipDSList = ship.det_and_range["detected_ships"]
            tmpADS = tmpADS + shipDSList
        tmpADS = list(dict.fromkeys(tmpADS))

        for ship in self.ennemyShips:
            shipDSList = ship.det_and_range["detected_ships"]
            tmpEDS = tmpEDS + shipDSList
        tmpEDS = list(dict.fromkeys(tmpEDS))

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
