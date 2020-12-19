# -*- coding: utf-8 -*-

'''
    File name: Battleship.py
    Author: Grégory LARGANGE
    Date created: 14/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 19/12/2020
    Python version: 3.8.1
'''

from PyQt5.QtCore import QRectF, QPointF

from library import Ship, GunTurret


class Battleship(Ship.Ship):
    """

    A class derived from Ship class to create Battleship type of ships.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    __init__(clock : MainClock, gameScene : GameScene, pos : QPointF,
             gun_tech : int, fireControl_tech : int, pc_tech : int, radar_tech : int)
        The constructor of the class.

    spawnWeapons()
        Spawn the ships turrets.

    """

    def __init__(self, clock, gameScene, pos, gun_tech, fireControl_tech,
                 pc_tech, radar_tech):
        """

        Parameters
        ----------
        clock : MainClock
            The main clock of the game.
        gameScene : GameScene
            The main display of the game.
        pos : QPointF
            The world poijnt at which to spawn the projectile.
        gun_tech : int
            The gun technology level to be used on the ship. Between 0 and 2.
        fireControl_tech : int
            The fire control technology level to be used opn the ship.
            Between 0 and 2.
        pc_tech : int
            The computer technology level to be used on the ship.
            Between 0 and 2.
        radar_tech : int
            The radar technology level to be used on the ship.
            Between 0 and 3.

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        super(Battleship, self).__init__(clock, gameScene)

        rect = QRectF(0, 0, 1150, 250)
        self._type = "BB"
        self.hp = self.max_hp = 10000
        self.armor = 300
        self.shield = self.max_shield = 10000
        self.speed = 0
        self.max_speed = 9
        self.speed_options = {
            "AHEAD_FULL": self.max_speed,
            "FAST": int(2 * self.max_speed / 3),
            "SLOW": int(self.max_speed / 3),
            "STOP": 0
            }
        self.accel = self.max_accel = 0.5
        self.turn_rate = 0.13
        self.concealement = self.base_concealement = 0.1
        self.base_detection_range = 5000
        self.guns_range = self.projectileData.ranges_shellSize[2]
        self.gun_tech = gun_tech
        self.fc_tech = fireControl_tech
        self.pc_tech = pc_tech
        self.radar_tech = radar_tech
        self.detection_range = self.base_detection_range +\
            self.base_detection_range * self.techData.radar_tech_aug[self.radar_tech]

        self.setRect(rect)
        self.setPos(pos)
        self.spawnWeapons()
        self.printInfos()

    def spawnWeapons(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Spawns the turrets of the battlship at predefined places. See documentation
        for further informations.

        """
        self.gun_turrets_pos = [QPointF(self.x() + 175, self.y() + 75),
                                 QPointF(self.x() + 625, self.y() + 75),
                                 QPointF(self.x() + 800, self.y() + 75)]

        turretC = GunTurret.GunTurret(self.clock, self.gameScene, "l", self)
        turretC.setPos(self.gun_turrets_pos[0])
        turretC.setDFromShipCenter(175 - self.rect().width() / 2)
        turretC.setZValue(3)
        self.gameScene.addItem(turretC)


        turretB = GunTurret.GunTurret(self.clock, self.gameScene, "l", self)
        turretB.setPos(self.gun_turrets_pos[1])
        turretB.setDFromShipCenter(625 - self.rect().width() / 2)
        turretB.setZValue(3)
        self.gameScene.addItem(turretB)

        turretA = GunTurret.GunTurret(self.clock, self.gameScene, "l", self)
        turretA.setPos(self.gun_turrets_pos[2])
        turretA.setDFromShipCenter(800 - self.rect().width() / 2)
        turretA.setZValue(3)
        self.gameScene.addItem(turretA)

        self.gun_turrets_list = [turretC, turretB, turretA]
