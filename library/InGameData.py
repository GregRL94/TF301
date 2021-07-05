# -*- coding: utf-8 -*-

"""
    File name: InGameData.py
    Author: Grégory LARGANGE
    Date created: 19/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 07/04/2021
    Python version: 3.8.1
"""

from PyQt5.QtGui import QColor


class TurretData:
    """

    A class holding turrets parameters.

    ...

    Attributes
    ----------
    rect_values : list of int
        A list of heights for the turret rectangle per turret size.

    thk_values : list of int
        A list of thicknesses for the turret borders per turret size.

    n_guns : list of int
        A list of number of guns per turret size.

    reload_t_values : list of int
        A list of reload times per turret size.

    rot_rate_values : list of floqt
        A list of rotation speeds per turret size.

    acc_f_values : list of float
        A list of accuracy appreciation per turret size.

    w_h_ratio : float
        The ratio between the turret width and height.

    Methods
    -------
    None.

    """

    # Ordered regarding size of the turret. 0 small -> 2 large #
    rect_values = [25, 50, 100]
    thk_values = [5, 10, 10]
    n_guns = [1, 2, 3]  # Number of guns
    reload_t_values = [50, 75, 150]  # The lower the value the faster the turret reloads
    rot_rate_values = [
        3.6,
        2.4,
        1.2,
    ]  # The higher the value the faster the turret rotates
    acc_f_values = [0.6, 0.8, 1]  # The lower the value the better the accuracy
    w_h_ratio = 1.25


class ProjectileData:
    """

    A class holding projectiles parameters.

    ...

    Attributes
    ----------
    size_tags : list of string
        A list of tags to identify the size of a projectile.

    size_values : list of int
        A list of in game size per shell size.

    thk_values : list of int
        A list of thickness of projectile border per shell size.

    ranges_shellSize : list of int
        A list of ranges in units per shell size.

    inaccuracy : list of float
        A list of error margin per shell size.

    speeds_shellType : list of int
        A list of speeds per shell type.

    colors_values : list of QColor
        A list of colors per shell type.

    damage_type : list of lists of int
        A list per shell size of sublist of damage per shell type.

    pen_values : list of sublists of int
        A list per shell size of sublist of penetration per shell type.

    v_decreaseRate : float
        The speed lost per game clock cycle.

    w_h_ratio : float
        The ratio between the projectile width and height.

    Methods
    -------
    None.

    """

    ##### INFORMATIONS ON LIST CONTRUCTION #####
    # For simple lists: ordered regarding the size of the shells
    # [0] -> small, [2] -> large
    # For nested lists, the subelements of the list gives the type of the shell
    # [0]-> AP [1] -> HE
    # Hence [1][0] gives the value of a "Medium" size "AP" shell
    ############################################

    size_tags = ["s", "m", "l"]  # Also defines the ordering of shell size bound data
    size_values = [15, 22, 38]  # Hence here [0] is for "s" shells, [1] for "m" etc
    thk_values = [3, 5, 8]
    ranges_shellSize = [9000, 15000, 21000]
    inaccuracy = [0.025, 0.0325, 0.0375]
    speeds_shellType = [150, 125]  # Element 0 is AP, 1 is HE
    colors_values = [
        QColor("lightGray"),
        QColor("gray"),
        QColor("yellow"),
        QColor(255, 165, 0),
    ]  # RGB value is orange
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
    v_decreaseRate = 0.2
    w_h_ratio = 2


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

    # The formula is: acc(deg) = tan-1(disp(units)/range(units))
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
