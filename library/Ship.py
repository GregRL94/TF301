# -*- coding: utf-8 -*-

'''
    File name: Ship.py
    Author: Grégory LARGANGE
    Date created: 09/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 19/03/2021
    Python version: 3.8.1
'''

import math

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem

from library.MathsFormulas import Geometrics as geo, Cinematics as cin,\
    Controllers as con
from library.Mapping import Astar as astar



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

    setDestination(targetPoint)
        Sets the destination of the ship to target point. Calculates a path to targetPoint
        via an Astar algorithm and sets the trajectory to follow as a list of points.

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
        Sets rcom_ships to infosList. Receives a list of all ennemy ships detected by all allied ships.

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

    #--------- HULL CHARACTERISTICS --------#
    _type = ""
    max_hp = 0
    armor = 0
    max_shield = 0
    max_speed = 0
    max_accel = 0
    turn_rate = 0
    base_concealement = 0
    base_detection_range = 0
    #---------------------------------------#

    #-------- WEAPONS CHARACTERISTICS ------#
    gun_turrets_list = None
    gun_turrets_pos = None
    laser_turrets_list = None
    laser_turrets_pos = None
    guns_range = 0
    guns_tech = 0
    fc_tech = 0
    pc_tech = 0
    radar_tech = 0
    #---------------------------------------#

    #-------------- SCAN RATES -------------#
    refresh_rate = 9
    print_point_rate = 74  # TO DELETE ONLY FOR VISU
    #---------------------------------------#

    #------ CRITICAL COMPONENT STATES ------#
    bridge_state = "OK"
    engine_state = "OK"
    radar_state = "OK"
    shield_generator_state = "OK"
    #---------------------------------------#

    #-------- DETECTION AND RANGING --------#
    detected_ships = None
    rcom_ships = None
    ships_in_range = None
    #---------------------------------------#

    #-------------- PATHFINDING ------------#
    pathUpdateRate = 99
    center = QPointF()
    r_centers = None
    trajectory = None
    checkpoint = None
    sel_checkpoint_id = None
    targetPoint = None
    cp_tolerance = 500
    heading = 0
    t_heading = 0
    rot_direction = 0
    #---------------------------------------#

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

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self.gameScene = gameScene
        self.clock = clock
        self.next_Path_Update = self.pathUpdateRate
        self.next_radarScan = 0
        self.next_targetAcquisition = 0
        self.next_point_print = 0  # Debug print

        self.speed_user_override = None
        self.default_speed = "FAST"
        self.speed_options = {
            "AHEAD_FULL": 0,
            "FAST": 0,
            "SLOW": 0,
            "STOP": 0
            }

        self.clock.clockSignal.connect(self.fixedUpdate)

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
        if self.next_point_print <= 0:
            self.gameScene.printPoint(self.center, 100, "blue", True)
            if self.rot_direction < 0:
                self.gameScene.printPoint(self.r_centers[0], 100, "blue", True)
            elif self.rot_direction > 0:
                self.gameScene.printPoint(self.r_centers[1], 100, "blue", True)
            self.next_point_print = self.print_point_rate
        else:
            self.next_point_print -= 1
        ##################
        # Test if the target point of the pathfinding has been reached
        if self.checkpointReached(self.targetPoint, True) is False:
            if (self.next_Path_Update <= 0) & (self.targetPoint is not None):
                self.updatePath()
                self.next_Path_Update = self.pathUpdateRate
            else:
                self.next_Path_Update -= 1

        # Test to launch a radar scan (gets all ships in detection range)
        if self.next_radarScan <= 0:
            self.scan()
            self.ships_in_range = self.computeShipsInRange()
            self.next_radarScan = self.refresh_rate
        else:
            self.next_radarScan -= 1

        # Test to acquire the best target
        if self.next_targetAcquisition <= 0:
            for turret in self.gun_turrets_list:
                turret.setTarget(self.autoSelectTarget())
            self.next_targetAcquisition = self.refresh_rate
        else:
            self.next_targetAcquisition -= 1

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
        info = self._type + str(self.data(0)) + "  " + "HP: " + str(self.hp)
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
        Prints the postion of the item.

        """
        print(self._type + str(self.data(0)), "selected at:", mouseDown.pos())

    def updateCenter(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Updates the position of the ship center.

        """
        self.center = geo.parallelepiped_Center(self.pos(),
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
        self.r_centers = cin.rotationCenters(self.center, self.heading,
                                             self.speed, self.turn_rate)

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
            targetSpeed = self.speed_options[self.default_speed]
        else:
            targetSpeed = self.speed_options[speedOption]

        self.speed += con.proportional(targetSpeed, self.speed, self.max_accel)

    def setSpeed(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Sets the speed that the ship should reach.

        """
        if self.checkpoint is None:
            if self.speed_user_override:
                self.reachSpeed(self.speed_user_override)
                # print("User overridde:", self.speed_user_override)
            else:
                self.reachSpeed("STOP")
                # print("No user override, using: STOP because no further checkpoints.")
        else:
            # print("Remaining distance to checkpoint:", geo.distance_A_B(self.center,
            #                                                                         self.checkpoint))
            brakeD = cin.brakeDistance(self.speed, -self.max_accel)
            if geo.distance_A_B(self.center, self.checkpoint) <= brakeD:
                self.reachSpeed("STOP")
            elif self.checkpointInTurnRadius() is False:
                # print("Slowing down to match checkpoint")
                self.reachSpeed("SLOW")
            else:
                if self.speed_user_override:
                    # print("No brake triggers. Using user overridde:", self.speed_user_override)
                    self.reachSpeed(self.speed_user_override)
                else:
                    # print("No brake triggers. No user override. Using default speed:", self.default_speed)
                    self.reachSpeed(self.default_speed)

    def computeHeading(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Computes the rotation angle to apply in order to reach the next checkpoint.

        """
        distance = geo.distance_A_B(self.center, self.checkpoint)
        a_h = (self.checkpoint.x() - self.center.x()) / distance
        if a_h > 1.:
            a_h = 1
        elif a_h < -1:
            a_h = -1
        self.t_heading = round(math.degrees(math.acos(a_h)), 4)
        if (self.checkpoint.y() - self.center.y()) < 0:
            self.t_heading *= -1

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
        diff = geo.smallestAngle(self.t_heading, self.heading)
        if diff < -0.5:
            self.rot_direction = -1
        elif diff > 0.5:
            self.rot_direction = 1
        else:
            self.rot_direction = 0
        self.heading += con.proportional(self.t_heading,
                                                      self.heading,
                                                      self.turn_rate, diff)
        self.setTransformOriginPoint(QPointF(self.rect().width() / 2,
                                             self.rect().height() / 2))
        self.setRotation(self.heading)

    def setDestination(self, targetPoint):
        """

        Parameters
        ----------
        targetPoint : QPointF
            The world point the unit must move to.

        Returns
        -------
        None

        Summary
        -------
        Sets the end point of the pathfinding algorithm to targetPoint.

        """
        self.trajectory = []
        self.targetPoint = targetPoint
        self.astar.reset()
        for node in self.astar.findPath(self.center, self.targetPoint):
            self.trajectory.append(QPointF(node.xPos, node.yPos))
        # Debug display
        for point in self.trajectory:
            self.gameScene.printPoint(point, 1000, "black")

    def updatePath(self):
        """

        Returns
        -------
        None

        Summary
        -------
        Updates the trajectory by calling the Astar pathfinding algorithm.

        """
        self.gameScene.clearWaypoints() # Debug display
        self.trajectory.clear()
        self.sel_checkpoint_id = None
        self.astar.reset()
        for node in self.astar.findPath(self.center, self.targetPoint):
            self.trajectory.append(QPointF(node.xPos, node.yPos))
        self.selectNextCheckpoint()
        # Debug display
        for point in self.trajectory:
            self.gameScene.printPoint(point, 1000, "black")

    def checkpointReached(self, checkpoint, targetPoint=False):
        """

        Parameters
        ----------
        checkpoint : QPointF
            The point to check if the ship has reached.
        targetPoint[Default=Fasle] : bool
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
            toleranceRect = QRectF(checkpoint.x() - self.cp_tolerance,
                                   checkpoint.y() - self.cp_tolerance,
                                   2 * self.cp_tolerance, 2 * self.cp_tolerance)
            if toleranceRect.contains(self.center):
                if targetPoint:
                    self.targetPoint = None
                else:
                    self.checkpoint = None
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
        if self.trajectory is None:
            self.checkpoint = None
            self.sel_checkpoint_id = None
        else:
            if self.sel_checkpoint_id is None:
                self.checkpoint = self.trajectory[0]
                self.sel_checkpoint_id = 0
            else:
                if self.sel_checkpoint_id + 1 <= len(self.trajectory) - 1:
                    self.sel_checkpoint_id += 1
                    self.checkpoint = self.trajectory[self.sel_checkpoint_id]
                else:
                    self.trajectory = None
                    self.chekpoint = None
                    self.sel_checkpoint = None
                    self.targetPoint = None

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

        if self.rot_direction < 0:
            rot_center = self.r_centers[0]
        elif self.rot_direction > 0:
            rot_center = self.r_centers[1]
        else:
            return None

        if geo.distance_A_B(rot_center, self.checkpoint) <\
            cin.rotationRadius(self.speed, self.turn_rate):
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
        for turret in self.gun_turrets_list:
            tur_angle = 180 if turret.d_shipCenter < 0 else 0
            teta = math.radians(self.heading + tur_angle)
            r = abs(turret.d_shipCenter)
            nextTurPosX = self.center.x() + r * math.cos(teta)
            nextTurPosY = self.center.y() - 25 + r * math.sin(teta)

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
        if self.checkpoint is not None:
            self.computeHeading()
            self.rotateToHeading()
        self.setSpeed()
        headingInRad = math.radians(self.heading)
        nextPoint = cin.movementBy(self.pos(), self.speed,
                                               headingInRad)
        self.setPos(nextPoint)
        self.updateTurretPos()

        if self.checkpointReached(self.checkpoint):
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
        self.detected_ships = self.gameScene.shipsInDetectionRange(self.data(0),
                                                                   self.data(1),
                                                                   self.center,
                                                                   self.detection_range)

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
        self.rcom_ships = infosList

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

        if self.detected_ships:
            if len(self.detected_ships) > 0:
                for ship in self.detected_ships:
                    detSCPos = geo.parallelepiped_Center(
                        ship.pos(), ship.rect().width(), ship.rect().height())
                    distance = geo.distance_A_B(self.center, detSCPos)
                    if distance <= self.guns_range:
                        sIR.append(ship)
        if self.rcom_ships:
            if len(self.rcom_ships) > 0:
                for ship in self.rcom_ships:
                    if ship not in sIR:
                        detSCPos = geo.parallelepiped_Center(
                            ship.pos(), ship.rect().width(), ship.rect().height())
                        distance = geo.distance_A_B(self.center, detSCPos)
                        if distance <= self.guns_range:
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

        if self.ships_in_range is not None:
            if len(self.ships_in_range) > 0:
                target = self.ships_in_range[0]
        return target

    def repair(self):
        True

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
        if self._type == "BB":
            txt = "Battleship"
        elif self._type == "CA":
            txt = "Cruiser"
        elif self._type == "FF":
            txt = "Frigate"
        elif self._type == "PT":
            txt = "Torpedo Corvette"
        print("TYPE:", txt)
        print("")
        print("---------- SURVIVABILITY ----------")
        print("HP:", str(self.max_hp))
        print("ARMOR:", str(self.armor))
        print("SHIELD:", str(self.max_shield))
        print("")
        print("------------ MOBILITY -------------")
        print("MAXIMUM SPEED:", str(self.max_speed) + "unit/s")
        print("MAXIMUM ACCELERATION", str(self.max_accel) + "unit/s²")
        print("TURNING RATE", str(self.turn_rate) + "°/s")
        print("")
        print("--------- TECHNOLOGIES ------------")
        print("GUN TECHNOLOGY:", "Mk", str(self.gun_tech))
        print("FIRE CONTROL TECHNOLOGY:", "Mk", str(self.fc_tech))
        print("TARGETING COMPUTER TECHNOLOGY:", "Mk", str(self.pc_tech))
        print("RADAR TECHNOLOGY:", "Mk", str(self.radar_tech))
        print("")
        print("----------- VISIBILITY ------------")
        print("CONCEALEMENT", str(self.base_concealement))
        print("")
        print("----------- DETECTION -------------")
        print("DETECTION RANGE", str(self.detection_range) + "units")
        print("")
        print("----------- ARMAMENT --------------")
        if self.gun_turrets_list is not None:
            for turret in self.gun_turrets_list:
                num_turr += 1
                num_guns = turret.gun_number
        if self.laser_turrets_list is not None:
            for laser in self.laser_turrets_list:
                num_laser += 1
        print("MAIN ARMAMENT:", str(num_turr), "turrets of ", str(num_guns), "guns")
        print("SECONDARY ARMAMENT:", str(num_laser), "laser turrets")
        print("")
        print("")
        print("**************** END ****************")
        print("")

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
            painter.setBrush(QBrush(QColor("red")))
            painter.setPen(QPen(QColor("darkred"), 10))
        painter.drawEllipse(self.rect())
