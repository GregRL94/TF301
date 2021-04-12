# -*- coding: utf-8 -*-

'''
    File name: Ship.py
    Author: Grégory LARGANGE
    Date created: 09/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 01/04/2021
    Python version: 3.8.1
'''

import math

from os import path

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem

from library import GunTurret, RangeCircles
from library.InGameData import TechsData as tech_dat
from library.MathsFormulas import Geometrics as geo, Cinematics as cin,\
    Controllers as con
from library.Mapping import Astar as astar
from library.utils.Config import Config


class Ship(QGraphicsRectItem):
    """

    The core class for all ship untis.

    ...

    Attributes
    ----------
    Go in class to see all attributes.

    Methods
    -------
    __init__(clock : Mainclock, gameScene : GameScene, gameMap : list of lists,
             mapSlicing : int)
        Constructor of the class.

    fixedUpdate()
        Updates the ship state.

    hoverMoveEvent(mousePos)
        Changes the appearance of the cursor, display hp informations.

    mousePressEvent(mousePos)
        Prints the position of the ship at click.

    updateCenter()
        Gets the current position of the ship center and stores it.

    updateRCenters()
        Updates the rotation centers (left and right) positions.

    reachSpeed(speedOption : string)
        Applies a controller to reach the speed indicated by SpeedOption.

    setSpeed()
        Sets the speed for the ship to reach.

    computeHeading()
        Computes the angle for the ship to reach.

    rotateToHeading()
        Applies a controller to rotate the ship until self.t_heading is reached.

    updatePath()
        Updates the trajectory by calling the Astar with the new position of th ship.

    checkpointReached(checkpoint : QPointF, targetPoint[False] : bool)
        Check if the ship center is within a tolerance rectangle of checkpoint. Passing
        True for targetpoint checks if the checkpoint to check is the target destination point.

    selectNextCheckpoint()
        Selects the next checkpoint to be reached in the trajectory list.

    checkpointInTurnRadius()
        Checks if the next checkpoint to reach is within the hardest turn radius.

    updateTurretPos()
        Update the ships turrets positions according to its position and rotation in the game scene.

    move()
        Updates the ship position in the game scene according to its speed and rotation.

    scan()
        Callback to GameScene shipsIndetectionRange function. Gets a list of all ships within
        detection range who have a different tag.

    receiveRadioComm(infosList : list)
        Sets det_and_range["rcom_ships"] to infosList. Receives a list of all ennemy ships detected by all allied ships.

    computeShipsInRange()
        Computes the list list of all detected ships which are withing the ships gun range.

    autoSelectTarget()
        Uses an algorithm to determine the best target to shoot at.

    repair()
        Repairs a ship core component.

    printInfos()
        Print all infos about the ship.

    paint()
        Paints the ship on the game scene

    """

    def __init__(self, clock, gameScene, gameMap, mapSlicing):
        """

        Parameters
        ----------
        clock : MainClock
            The main clock of the game.
        gameScene : GameScene
            The main display of the game.
        gameMap : list of lists
            The game map as a square matrix.
        mapSlicing : The resolution of the map.

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        super(Ship, self).__init__(QRectF(0, 0, 0, 0))
        self.astar = astar(gameMap, mapSlicing)
        self.gameScene = gameScene
        self.clock = clock

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self.clock.clockSignal.connect(self.fixedUpdate)

    def __init_instance__(self, pos, tag):
        rect = QRectF(0, 0, self.geometry["_width"], self.geometry["_height"])
        self.coordinates["center"] = QPointF()
        self.instant_vars["hp"] = self.hull["max_hp"]
        self.instant_vars["shield"] = self.hull["max_shield"]
        self.instant_vars["concealement"] = self.hull["base_concealement"]
        self.instant_vars["detection_range"] = self.hull["base_detection_range"] +\
            self.hull["base_detection_range"] * tech_dat.radar_tech_aug[self.techs["radar_tech"]]
        self.speed_params["speed_options"] = {
            "AHEAD_FULL": self.hull["max_speed"],
            "FAST": int(2 * self.hull["max_speed"] / 3),
            "SLOW": int(self.hull["max_speed"] / 3),
            "STOP": 0
            }

        self.setData(1, tag)
        self.setRect(rect)
        self.setPos(pos)

        self.spawnWeapons()
        self.setRangeCirclesDisp()
        self.printInfos()

    @classmethod
    def _battleShip(cls, clock, gameScene, gameMap, mapSlicing, pos, tag, _config):
        bb = cls(clock, gameScene, gameMap, mapSlicing)
        bb.__dict__.update(_config)
        bb.__init_instance__(pos, tag)

        return bb

    def fixedUpdate(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Updates the ship at each clock signal.

        """
        self.updateCenter()
        self.updateRCenters()
        self.move()

        # Debug display #
        if self.iterators["next_point_print"] <= 0:
            self.gameScene.printPoint(self.coordinates["center"], 100, "blue", True)
            if self.coordinates["rot_direction"] < 0:
                self.gameScene.printPoint(self.coordinates["r_centers"][0], 100, "blue", True)
            elif self.coordinates["rot_direction"] > 0:
                self.gameScene.printPoint(self.coordinates["r_centers"][1], 100, "blue", True)
            self.iterators["next_point_print"] = self.refresh["print_point_rate"]
        else:
            self.iterators["next_point_print"] -= 1
        ##################
        # Test if the target point of the pathfinding has been reached
        if self.checkpointReached(self.pathfinding["targetPoint"], True) is False:
            if (self.iterators["next_path_update"] <= 0) & (self.pathfinding["targetPoint"] is not None):
                self.updatePath()
                self.iterators["next_path_update"] = self.refresh["path_update_rate"]
            else:
                self.iterators["next_path_update"] -= 1

        # Test to launch a radar scan (gets all ships in detection range)
        if self.iterators["next_radar_scan"] <= 0:
            self.scan()
            self.det_and_range["ships_in_range"] = self.computeShipsInRange()
            self.iterators["next_radar_scan"] = self.refresh["refresh_rate"]
        else:
            self.iterators["next_radar_scan"] -= 1

        # Test to acquire the best target
        if self.iterators["next_target_lock"] <= 0:
            for turret in self.weapons["turrets_list"]:
                turret.setTarget(self.autoSelectTarget())
            self.iterators["next_target_lock"] = self.refresh["refresh_rate"]
        else:
            self.iterators["next_target_lock"] -= 1

        # Test to hide the range circles
        if self.isSelected() is False:
            self.displays["rangeCirclesDisp"].hide()

    def hoverMoveEvent(self, mousePos):
        """

        Parameters
        ----------
        mousePos : QEvent
            An event indicating that the mouse was moved over the item..

        Returns
        -------
        None.

        Summary
        -------
        Changes the apperance of the cursor and display basic infos.

        """
        self.setCursor(QCursor(Qt.PointingHandCursor))
        # Display an information bubble
        info = self.naming["_type"] + str(self.data(0)) + "  " + "HP: " + str(self.instant_vars["hp"])
        super().setToolTip(info)

    def mousePressEvent(self, mouseDown):
        """
        Parameters
        ----------
        mouseDown: QMouseEvent
            A signal indicating that a mouse button was pressed.

        Returns
        -------
        None.

        Summary
        -------
        Prints the postion of the item. Displays the range circles.

        """
        print(self.naming["_type"] + str(self.data(0)), "selected at:", mouseDown.pos())
        self.displays["rangeCirclesDisp"].show()

    def updateCenter(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Updates the position of the ship center.

        """
        self.coordinates["center"] = geo.parallelepiped_Center(self.pos(),
                                                               self.rect().width(),
                                                               self.rect().height())

    def updateRCenters(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Updates the position od the ship rotation centers.

        """
        self.coordinates["r_centers"] = cin.rotationCenters(self.coordinates["center"], self.coordinates["heading"],
                                                            self.instant_vars["speed"], self.hull["turn_rate"])

    def reachSpeed(self, speedOption):
        """

        Parameters
        ----------
        speedOption : string
            A string corresponding to a key of the speed_option dictionary.

        Returns
        -------
        None.

        Summary
        -------
        Tries to reach the discrete speed value corresponding to speedOption.

        """
        targetSpeed = 0

        if speedOption is None:
            targetSpeed = self.speed_params["speed_options"][self.speed_params["default_speed"]]
        else:
            targetSpeed = self.speed_params["speed_options"][speedOption]

        self.instant_vars["speed"] += con.proportional(targetSpeed, self.instant_vars["speed"], self.hull["max_accel"])

    def setSpeed(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Sets the speed that the ship should reach.

        """
        if self.pathfinding["checkpoint"] is None:
            if self.speed_params["speed_user_override"]:
                self.reachSpeed(self.speed_params["speed_user_override"])
                # print("User overridde:", self.speed_user_override)
            else:
                self.reachSpeed("STOP")
                # print("No user override, using: STOP because no further checkpoints.")
        else:
            # print("Remaining distance to checkpoint:", geo.distance_A_B(self.center, self.checkpoint))
            brakeD = cin.brakeDistance(self.instant_vars["speed"], -self.hull["max_accel"])
            if geo.distance_A_B(self.coordinates["center"], self.pathfinding["checkpoint"]) <= brakeD:
                self.reachSpeed("STOP")
            elif self.checkpointInTurnRadius() is False:
                # print("Slowing down to match checkpoint")
                self.reachSpeed("SLOW")
            else:
                if self.speed_params["speed_user_override"]:
                    # print("No brake triggers. Using user overridde:", self.speed_user_override)
                    self.reachSpeed(self.speed_params["speed_user_override"])
                else:
                    # print("No brake triggers. No user override. Using default speed:", self.speed_params["default_speed"])
                    self.reachSpeed(self.speed_params["default_speed"])

    def computeHeading(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Computes the rotation angle to apply in order to reach the next checkpoint.

        """
        distance = geo.distance_A_B(self.coordinates["center"], self.pathfinding["checkpoint"])
        a_h = (self.pathfinding["checkpoint"].x() - self.coordinates["center"].x()) / distance
        if a_h > 1.:
            a_h = 1
        elif a_h < -1:
            a_h = -1
        self.pathfinding["t_heading"] = round(math.degrees(math.acos(a_h)), 4)
        if (self.pathfinding["checkpoint"].y() - self.coordinates["center"].y()) < 0:
            self.pathfinding["t_heading"] *= -1

    def rotateToHeading(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Applies a basic controller to rotate the ship from its current heading
        to the target heading.

        """
        diff = geo.smallestAngle(self.pathfinding["t_heading"], self.coordinates["heading"])
        if diff < -0.5:
            self.coordinates["rot_direction"] = -1
        elif diff > 0.5:
            self.coordinates["rot_direction"] = 1
        else:
            self.coordinates["rot_direction"] = 0
        self.coordinates["heading"] += con.proportional(self.pathfinding["t_heading"], self.coordinates["heading"], self.hull["turn_rate"], diff)
        self.setTransformOriginPoint(QPointF(self.rect().width() / 2, self.rect().height() / 2))
        self.setRotation(self.coordinates["heading"])

    def updatePath(self, targetPoint=None):
        """

        Returns
        -------
        None

        Summary
        -------
        Updates the trajectory by calling the Astar pathfinding algorithm.

        """
        self.gameScene.clearWaypoints() # Debug display
        if self.pathfinding["trajectory"]:
            self.pathfinding["trajectory"].clear()
        else:
            self.pathfinding["trajectory"] = []

        if targetPoint:
            self.pathfinding["targetPoint"] = targetPoint

        self.pathfinding["sel_checkpoint_id"] = None
        self.astar.reset()
        for node in self.astar.findPath(self.coordinates["center"], self.pathfinding["targetPoint"]):
            self.pathfinding["trajectory"].append(QPointF(node.xPos, node.yPos))
        self.selectNextCheckpoint()
        # Debug display
        for point in self.pathfinding["trajectory"]:
            self.gameScene.printPoint(point, 1000, "black")

    def checkpointReached(self, checkpoint, targetPoint=False):
        """

        Parameters
        ----------
        checkpoint : QPointF
            The point to check if the ship has reached.
        targetPoint[Default=False] : bool
            Determines if the passed checkpoint is also the targetPoint.

        Returns
        -------
        bool
            Indicates if a checkpoint has been reached.

        Summary
        -------
        Checks if the ship center is within a tolerance rectangle of a point.
        Returns True if yes, False otherwise.

        """
        if checkpoint:
            toleranceRect = QRectF(checkpoint.x() - self.pathfinding["cp_tolerance"],
                                   checkpoint.y() - self.pathfinding["cp_tolerance"],
                                   2 * self.pathfinding["cp_tolerance"], 2 * self.pathfinding["cp_tolerance"])
            if toleranceRect.contains(self.coordinates["center"]):
                if targetPoint:
                    self.pathfinding["targetPoint"] = None
                else:
                    self.pathfinding["checkpoint"] = None
                return True
            else:
                return False
        else:
            return True

    def selectNextCheckpoint(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Selects the next point in the trajectory list to be reached. If there
        is no more points, resets the trajectory, current checkpoint and targetpoint.

        """
        if self.pathfinding["trajectory"] is None:
            self.pathfinding["checkpoint"] = None
            self.pathfinding["sel_checkpoint_id"] = None
        else:
            if self.pathfinding["sel_checkpoint_id"] is None:
                self.pathfinding["checkpoint"] = self.pathfinding["trajectory"][0]
                self.pathfinding["sel_checkpoint_id"] = 0
            else:
                if self.pathfinding["sel_checkpoint_id"] + 1 <= len(self.pathfinding["trajectory"]) - 1:
                    self.pathfinding["sel_checkpoint_id"] += 1
                    self.pathfinding["checkpoint"] = self.pathfinding["trajectory"][self.pathfinding["sel_checkpoint_id"]]
                else:
                    self.pathfinding["trajectory"] = None
                    self.pathfinding["checkpoint"] = None
                    self.pathfinding["targetPoint"] = None

    def checkpointInTurnRadius(self):
        """

        Returns
        -------
        bool
            True if the point is reachable, False otherwise.

        Summary
        -------
        Calculates if a point is reachable with the hardest turn. returns True if yes,
        False otherwise.

        """
        rot_center = QPointF()

        if self.coordinates["rot_direction"] < 0:
            rot_center = self.coordinates["r_centers"][0]
        elif self.coordinates["rot_direction"] > 0:
            rot_center = self.coordinates["r_centers"][1]
        else:
            return None

        if geo.distance_A_B(rot_center, self.pathfinding["checkpoint"]) <\
            cin.rotationRadius(self.instant_vars["speed"], self.hull["turn_rate"]):
            return False
        else:
            return True

    def updateTurretPos(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Updates the position of the ship's turret in game world referential
        according to the ship's own movements and the position of its turrets
        in its referential.

        """
        for turret in self.weapons["turrets_list"]:
            tur_angle = 180 if turret.d_shipCenter < 0 else 0
            teta = math.radians(self.coordinates["heading"] + tur_angle)
            r = abs(turret.d_shipCenter)
            nextTurPosX = self.coordinates["center"].x() + r * math.cos(teta)
            nextTurPosY = self.coordinates["center"].y() - 25 + r * math.sin(teta)

            turret.setPos(nextTurPosX, nextTurPosY)

    def move(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Moves the ship according to is ship in the direction heading.

        """
        if self.pathfinding["checkpoint"] is not None:
            self.computeHeading()
            self.rotateToHeading()
        self.setSpeed()
        headingInRad = math.radians(self.coordinates["heading"])
        nextPoint = cin.movementBy(self.pos(), self.instant_vars["speed"], headingInRad)
        self.setPos(nextPoint)
        self.updateTurretPos()
        self.displays["rangeCirclesDisp"]._updatePos(self.coordinates["center"])

        if self.checkpointReached(self.pathfinding["checkpoint"]):
            self.selectNextCheckpoint()

    def scan(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Scans the game world for ennemy ships in its detection range.

        """
        self.det_and_range["detected_ships"] = self.gameScene.shipsInDetectionRange(
            self.data(0),
            self.data(1),
            self.coordinates["center"],
            self.instant_vars["detection_range"]
            )

    def receiveRadioComm(self, infosList):
        """

        Parameters
        ----------
        infosList : list
            A list of Ship objects.

        Returns
        -------
        None.

        Summary
        -------
        Receives a list of ennemy ships detected by allied ships.

        """
        self.det_and_range["rcom_ships"] = infosList

    def computeShipsInRange(self):
        """

        Returns
        -------
        sIR : list
            A list of all detected ennemy ships in gun range.

        Summary
        -------
        Computes and returns a list of all enney detected ships within gun range.

        """
        sIR = []

        if self.det_and_range["detected_ships"]:
            if len(self.det_and_range["detected_ships"]) > 0:
                for ship in self.det_and_range["detected_ships"]:
                    detSCPos = geo.parallelepiped_Center(
                        ship.pos(), ship.rect().width(), ship.rect().height())
                    distance = geo.distance_A_B(self.coordinates["center"], detSCPos)
                    if distance <= self.weapons["guns_range"]:
                        sIR.append(ship)
        if self.det_and_range["rcom_ships"]:
            if len(self.det_and_range["rcom_ships"]) > 0:
                for ship in self.det_and_range["rcom_ships"]:
                    if ship not in sIR:
                        detSCPos = geo.parallelepiped_Center(
                            ship.pos(), ship.rect().width(), ship.rect().height())
                        distance = geo.distance_A_B(self.coordinates["center"], detSCPos)
                        if distance <= self.weapons["guns_range"]:
                            sIR.append(ship)
        return sIR

    def autoSelectTarget(self):
        """

        Returns
        -------
        target : Ship
            The Ship object to target.

        Summary
        -------
        Computes and return the best ship to set as target.

        """
        target = None

        if self.det_and_range["ships_in_range"] is not None:
            if len(self.det_and_range["ships_in_range"]) > 0:
                target = self.det_and_range["ships_in_range"][0]
        return target

    def repair(self):
        True

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
        gun_turrets_pos = [QPointF(self.x() + 175, self.y() + 75),
                           QPointF(self.x() + 625, self.y() + 75),
                           QPointF(self.x() + 800, self.y() + 75)]

        turretC = GunTurret.GunTurret(self.clock, self.gameScene, "l", self)
        turretC.setPos(gun_turrets_pos[0])
        turretC.setDFromShipCenter(175 - self.rect().width() / 2)
        turretC.setZValue(3)
        self.gameScene.addItem(turretC)

        turretB = GunTurret.GunTurret(self.clock, self.gameScene, "l", self)
        turretB.setPos(gun_turrets_pos[1])
        turretB.setDFromShipCenter(625 - self.rect().width() / 2)
        turretB.setZValue(3)
        self.gameScene.addItem(turretB)

        turretA = GunTurret.GunTurret(self.clock, self.gameScene, "l", self)
        turretA.setPos(gun_turrets_pos[2])
        turretA.setDFromShipCenter(800 - self.rect().width() / 2)
        turretA.setZValue(3)
        self.gameScene.addItem(turretA)

        self.weapons["turrets_list"] = [turretC, turretB, turretA]

    def printInfos(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Print infos about the ship.

        """
        txt = ""
        num_turr = 0
        num_laser = 0
        num_guns = 0

        print("********* GENERATED SHIP: *********")
        if self.naming["_type"] == "BB":
            txt = "Battleship"
        elif self.naming["_type"] == "CA":
            txt = "Cruiser"
        elif self.naming["_type"] == "FF":
            txt = "Frigate"
        elif self.naming["_type"] == "PT":
            txt = "Torpedo Corvette"
        print("TYPE:", txt)
        print("")
        print("---------- SURVIVABILITY ----------")
        print("HP:", str(self.hull["max_hp"]))
        print("ARMOR:", str(self.hull["armor"]))
        print("SHIELD:", str(self.hull["max_shield"]))
        print("")
        print("------------ MOBILITY -------------")
        print("MAXIMUM SPEED:", str(self.hull["max_speed"]) + "unit/s")
        print("MAXIMUM ACCELERATION", str(self.hull["max_accel"]) + "unit/s²")
        print("TURNING RATE", str(self.hull["turn_rate"]) + "°/s")
        print("")
        print("--------- TECHNOLOGIES ------------")
        print("GUN TECHNOLOGY:", "Mk", str(self.techs["guns_tech"]))
        print("FIRE CONTROL TECHNOLOGY:", "Mk", str(self.techs["fc_tech"]))
        print("TARGETING COMPUTER TECHNOLOGY:", "Mk", str(self.techs["pc_tech"]))
        print("RADAR TECHNOLOGY:", "Mk", str(self.techs["radar_tech"]))
        print("")
        print("----------- VISIBILITY ------------")
        print("CONCEALEMENT", str(self.hull["base_concealement"]))
        print("")
        print("----------- DETECTION -------------")
        print("DETECTION RANGE", str(self.instant_vars["detection_range"]) + "units")
        print("")
        print("----------- ARMAMENT --------------")
        if self.weapons["turrets_list"] is not None:
            for turret in self.weapons["turrets_list"]:
                num_turr += 1
                num_guns = turret.gun_number
        if self.weapons["laser_turrets_list"] is not None:
            for laser in self.weapons["laser_turrets_list"]:
                num_laser += 1
        print("MAIN ARMAMENT:", str(num_turr), "turrets of ", str(num_guns), "guns")
        print("SECONDARY ARMAMENT:", str(num_laser), "laser turrets")
        print("")
        print("")
        print("**************** END ****************")
        print("")

    def setRangeCirclesDisp(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Spawns the ranges circles displays.

        """
        c = QPointF(self.pos().x() + self.rect().width() / 2, self.pos().y() + self.rect().height() / 2)

        if self.data(1) == "ALLY":
            self.displays["rangeCirclesDisp"] = RangeCircles.RangeCircles(c, self.instant_vars["detection_range"], self.weapons["guns_range"], "cyan", "blue")
        else:
            self.displays["rangeCirclesDisp"] = RangeCircles.RangeCircles(c, self.instant_vars["detection_range"], self.weapons["guns_range"], "yellow", "red")

        self.gameScene.addItem(self.displays["rangeCirclesDisp"])

    def paint(self, painter, option, widget=None):
        """

        Parameters
        ----------
        painter : QPainter
            A QPainter object.
        option : QtOption
            Options to apply to the QPainter.
        widget : QWidget, optional
            A QWidget object. The default is None.

        Returns
        -------
        None.

        Summary
        -------
        Instructions to draw the item on the game scene.

        """
        if self.data(1) == "ALLY":
            if self.isSelected():
                painter.setBrush(QBrush(QColor("green")))
                painter.setPen(QPen(QColor("darkGreen"), 10))
            else:
                painter.setBrush(QBrush(QColor("blue")))
                painter.setPen(QPen(QColor("darkBlue"), 10))
        if self.data(1) == "ENNEMY":
            if self.isSelected():
                painter.setBrush(QBrush(QColor("yellow")))
                painter.setPen(QPen(QColor("red"), 10))
            else:
                painter.setBrush(QBrush(QColor("red")))
                painter.setPen(QPen(QColor("darkred"), 10))
        painter.drawEllipse(self.rect())
