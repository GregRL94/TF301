# -*- coding: utf-8 -*-

"""
    File name: Ship.py
    Author: Grégory LARGANGE
    Date created: 09/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 29/09/2021
    Python version: 3.8.1
"""

import math
import random

from os import path

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush, QCursor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem

from library.GunTurret import GunTurret as tur
from library.InGameData import TechsData as tech_dat
from library.utils import HEAP
from library.utils.Config import Config
from library.utils.MathsFormulas import (
    Geometrics as geo,
    Cinematics as cin,
    Controllers as con,
)
from library.UnitsGizmos import (
    RangeCirclesGizmo as c_gizmo,
    LineGizmo as l_gizmo,
    RectangleGizmo as r_gizmo,
)
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
        self.targetList = HEAP.HEAP()
        self.gameScene = gameScene
        self.clock = clock

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self.clock.clockSignal.connect(self.fixedUpdate)

    def __init_instance__(self, tag, pos, rotation=None):
        rect = QRectF(0, 0, self.geometry["_width"], self.geometry["_height"])
        self.coordinates["center"] = QPointF()
        self.instant_vars["hp"] = self.hull["max_hp"]
        self.instant_vars["shield"] = self.hull["max_shield"]
        self.instant_vars["concealement"] = self.hull["base_concealement"]
        self.instant_vars["detection_range"] = (
            self.hull["base_detection_range"]
            + self.hull["base_detection_range"]
            * tech_dat.radar_tech_aug[self.techs["radar_tech"]]
        )
        self.speed_params["speed_options"] = {
            "AHEAD_FULL": self.hull["max_speed"],
            "FAST": int(2 * self.hull["max_speed"] / 3),
            "SLOW": int(self.hull["max_speed"] / 3),
            "STOP": 0,
        }
        self.det_and_range["det_r_range"] = cin.rotationRadius(
            self.speed_params["speed_options"]["SLOW"], self.hull["turn_rate"]
        )
        self.det_and_range["fleet_detected_ships"] = []
        self.discoveredShips = []

        p_cfg = path.join(
            path.dirname(path.realpath(__file__)), "configs/projectileConfig.py"
        )
        all_p_dat, _ = Config._file2dict(p_cfg)
        table_cfg = path.join(
            path.dirname(path.realpath(__file__)), "configs/penetrationTable.py"
        )
        all_table, _ = Config._file2dict(table_cfg)
        if self.naming["_type"] == "BB":
            self.p_dat = all_p_dat["large"]
            self.table = all_table["large"]
        elif self.naming["_type"] == "CA":
            self.p_dat = all_p_dat["medium"]
            self.table = all_table["medium"]
        else:
            self.p_dat = all_p_dat["small"]
            self.table = all_table["small"]
        self.currentTurret = None
        self.playerTarget = None
        self.follow_ship = None

        self.setData(1, tag)
        self.setData(2, True)  # Considered an obstacle
        self.setData(3, "SHIP")
        self.setRect(rect)
        self.setPos(pos)
        if rotation:
            self.rotate(rotation)

        self.spawnWeapons()
        self.setGizmos()

    @classmethod
    def _battleShip(
        cls, clock, gameScene, gameMap, mapSlicing, tag, _config, pos, rotation=None
    ):
        bb = cls(clock, gameScene, gameMap, mapSlicing)
        bb.__dict__.update(_config)
        bb.__init_instance__(tag, pos, rotation)

        return bb

    @classmethod
    def cruiser(
        cls, clock, gameScene, gameMap, mapSlicing, tag, _config, pos, rotation=None
    ):
        ca = cls(clock, gameScene, gameMap, mapSlicing)
        ca.__dict__.update(_config)
        ca.__init_instance__(tag, pos, rotation)

        return ca

    @classmethod
    def destroyer(
        cls, clock, gameScene, gameMap, mapSlicing, tag, _config, pos, rotation=None
    ):
        dd = cls(clock, gameScene, gameMap, mapSlicing)
        dd.__dict__.update(_config)
        dd.__init_instance__(tag, pos, rotation)

        return dd

    @classmethod
    def corvette(
        cls, clock, gameScene, gameMap, mapSlicing, tag, _config, pos, rotation=None
    ):
        pt = cls(clock, gameScene, gameMap, mapSlicing)
        pt.__dict__.update(_config)
        pt.__init_instance__(tag, pos, rotation)

        return pt

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
        obs_det_results = self.dynamicObjectDetection()
        if obs_det_results:
            self.dodgeManoeuver(obs_det_results)
        else:
            self.move()

        # Debug display #
        if self.iterators["next_point_print"] <= 0:
            self.gameScene.printPoint(self.coordinates["center"], 100, "blue", True)
            if self.coordinates["rot_direction"] < 0:
                self.gameScene.printPoint(
                    self.coordinates["r_centers"][0], 100, "blue", True
                )
            elif self.coordinates["rot_direction"] > 0:
                self.gameScene.printPoint(
                    self.coordinates["r_centers"][1], 100, "blue", True
                )
            self.iterators["next_point_print"] = self.refresh["print_point_rate"]
        else:
            self.iterators["next_point_print"] -= 1
        ##################
        # If follow mode, update target point to new target ship pos:
        if self.follow_ship:
            self.pathfinding["targetPoint"] = self.follow_ship.pos()
        # Test if the target point of the pathfinding has been reached
        if self.checkpointReached(self.pathfinding["targetPoint"], True) is False:
            if (self.iterators["next_path_update"] <= 0) & (
                self.pathfinding["targetPoint"] is not None
            ):
                try:
                    self.updatePath()
                except Exception as e:
                    print("WARNING: Skipped a path update.\n", e)
                self.iterators["next_path_update"] = self.refresh["path_update_rate"]
            else:
                self.iterators["next_path_update"] -= 1

        # Test to launch a radar scan (gets all ships in detection range)
        if self.iterators["next_radar_scan"] <= 0:
            self.scan()
            self.addNewTargets()
            self.iterators["next_radar_scan"] = self.refresh["refresh_rate"]
        else:
            self.iterators["next_radar_scan"] -= 1

        # Test to acquire the best target
        if self.iterators["next_target_lock"] <= 0:
            for turret in self.weapons["turrets_list"]:
                if self.playerTarget:
                    if self.isTargetable(self.playerTarget):
                        turret.setTarget(self.playerTarget)
                    elif (
                        self.playerTarget in self.det_and_range["fleet_detected_ships"]
                    ):
                        self.updatePath(self.attack_move())
                    else:
                        self.playerTarget = None
                else:
                    try:
                        targetShip, shotType = self.autoSelectTarget()
                        turret.setTarget(targetShip)
                        turret.setShot(shotType)
                    except:
                        pass
            self.iterators["next_target_lock"] = self.refresh["refresh_rate"]
        else:
            self.iterators["next_target_lock"] -= 1

        # Test to hide the range circles
        if self.isSelected() is False:
            for gizmo in self.displays.values():
                gizmo.hide()

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
        info = (
            self.naming["_type"]
            + str(self.data(0))
            + "  "
            + "HP: "
            + str(self.instant_vars["hp"])
        )
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
        for gizmo in self.displays.values():
            gizmo.show()

    def updateCenter(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Updates the position of the ship center.

        """
        self.coordinates["center"] = geo.parallelepiped_Center(
            self.pos(), self.rect().width(), self.rect().height()
        )

    def updateRCenters(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Updates the position od the ship rotation centers.

        """
        self.coordinates["r_centers"] = cin.rotationCenters(
            self.coordinates["center"],
            self.coordinates["heading"],
            self.instant_vars["speed"],
            self.hull["turn_rate"],
        )

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
            targetSpeed = self.speed_params["speed_options"][
                self.speed_params["default_speed"]
            ]
        else:
            targetSpeed = self.speed_params["speed_options"][speedOption]

        self.instant_vars["speed"] += con.proportional(
            targetSpeed, self.instant_vars["speed"], self.hull["max_accel"]
        )

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
            brakeD = cin.brakeDistance(
                self.instant_vars["speed"], -self.hull["max_accel"]
            )
            if (
                geo.distance_A_B(
                    self.coordinates["center"], self.pathfinding["checkpoint"]
                )
                <= brakeD
            ):
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
        distance = geo.distance_A_B(
            self.coordinates["center"], self.pathfinding["checkpoint"]
        )
        a_h = (
            self.pathfinding["checkpoint"].x() - self.coordinates["center"].x()
        ) / distance
        if a_h > 1.0:
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
        diff = geo.smallestAngle(
            self.pathfinding["t_heading"], self.coordinates["heading"]
        )
        if diff < -0.5:
            self.coordinates["rot_direction"] = -1
        elif diff > 0.5:
            self.coordinates["rot_direction"] = 1
        else:
            self.coordinates["rot_direction"] = 0
        self.coordinates["heading"] += con.proportional(
            self.pathfinding["t_heading"],
            self.coordinates["heading"],
            self.hull["turn_rate"],
            diff,
        )
        self.rotate()

    def follow(self, ship):
        """
        Parameters
        ----------
        ship : Ship
            The other ALLIED ship to follow.

        Returns
        -------
        None.

        Summary:
        Sets up an other ship to follow.

        """
        self.follow_ship = ship

    def updatePath(self, targetPoint=None):
        """

        Returns
        -------
        None

        Summary
        -------
        Updates the trajectory by calling the Astar pathfinding algorithm.

        """
        self.gameScene.clearWaypoints()  # Debug display
        if self.pathfinding["trajectory"]:
            self.pathfinding["trajectory"].clear()
        else:
            self.pathfinding["trajectory"] = []

        if targetPoint:
            self.pathfinding["targetPoint"] = targetPoint
            self.follow_ship = None

        self.pathfinding["sel_checkpoint_id"] = None
        self.astar.reset()
        for node in self.astar.findPath(
            self.coordinates["center"], self.pathfinding["targetPoint"]
        ):
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
            toleranceRect = QRectF(
                checkpoint.x() - self.pathfinding["cp_tolerance"],
                checkpoint.y() - self.pathfinding["cp_tolerance"],
                2 * self.pathfinding["cp_tolerance"],
                2 * self.pathfinding["cp_tolerance"],
            )
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
                if (
                    self.pathfinding["sel_checkpoint_id"] + 1
                    <= len(self.pathfinding["trajectory"]) - 1
                ):
                    self.pathfinding["sel_checkpoint_id"] += 1
                    self.pathfinding["checkpoint"] = self.pathfinding["trajectory"][
                        self.pathfinding["sel_checkpoint_id"]
                    ]
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

        if geo.distance_A_B(
            rot_center, self.pathfinding["checkpoint"]
        ) < cin.rotationRadius(self.instant_vars["speed"], self.hull["turn_rate"]):
            return False
        else:
            return True

    def updatePos(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Update the position of the ship in the game world.

        """
        headingInRad = math.radians(self.coordinates["heading"])
        nextPoint = cin.movementBy(self.pos(), self.instant_vars["speed"], headingInRad)
        self.setPos(nextPoint)
        self.updateTurretPos()
        self.update_gizmos()

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
            r = abs(turret.d_shipCenter)
            # gamma = round(math.degrees(math.atan((turret._height / 2) / r)), 4)
            teta = math.radians(self.coordinates["heading"] + tur_angle)
            nextTurPosX = self.coordinates["center"].x() + r * math.cos(teta)
            nextTurPosY = self.coordinates["center"].y() - 75 + r * math.sin(teta)

            turret.setPos(nextTurPosX, nextTurPosY)

    def update_gizmos(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Update this unit gizmos.

        """
        self.displays["rangeCirclesDisp"].update_pos(self.coordinates["center"])
        self.displays["lineToDestination"].update_line(
            self.coordinates["center"], self.pathfinding["targetPoint"]
        )
        self.displays["lineToTarget"].update_line(
            self.coordinates["center"], self.playerTarget
        )
        self.displays["selected"].update_rect(self.pos(), self.coordinates["heading"])

    def rotate(self, rotation=None):
        """

        Returns
        -------
        None.

        Summary
        -------
        Rotates the ship around its central axis.

        """
        self.setTransformOriginPoint(self.rect().center())
        if rotation:
            self.setRotation(rotation)
            self.coordinates["heading"] = rotation
        else:
            self.setRotation(self.coordinates["heading"])

    def steer(self, direction, hard=False):
        """

        Parameters
        ----------
        direction : string
            The direction the ship should steer to.

        Returns
        -------
        None.

        Summary
        -------
        Rotates the ship at tur_rate rate in towards direction.

        """
        if direction == "PORT":
            self.coordinates["heading"] -= self.hull["turn_rate"]
            self.coordinates["rot_direction"] = -1
        elif direction == "STARBOARD":
            self.coordinates["heading"] += self.hull["turn_rate"]
            self.coordinates["rot_direction"] = 1
        self.rotate()
        if hard:
            self.reachSpeed("SLOW")

    def dodgeManoeuver(self, obstaclesDetectionResults, isEvasive=False):
        """

        Parameters
        ----------
        obstaclesDetectionResults : list
            The list of returned distances by the detection rays.
        isEvasive[False]: bool
            Wether this is an evasive manoeuver.

        Returns
        -------
        None.

        Summary
        -------
        Tests the returned distances of the detection rays, and decides
        to steer the ship accordingly.

        """
        if obstaclesDetectionResults:
            if obstaclesDetectionResults[0] and obstaclesDetectionResults[1]:
                self.steer("STARBOARD", True)
            elif obstaclesDetectionResults[1] and obstaclesDetectionResults[2]:
                self.steer("PORT", True)
            elif obstaclesDetectionResults[0]:
                self.steer("STARBOARD")
            elif obstaclesDetectionResults[1]:
                choice = random.random()
                if choice < 0.5:
                    self.steer("PORT")
                else:
                    self.steer("STARBOARD")
            elif obstaclesDetectionResults[2]:
                self.steer("PORT")
            else:
                self.reachSpeed("STOP")
        elif isEvasive:
            choice = random.random()
            if choice < 0.5:
                self.steer("PORT"),
            else:
                self.steer("STARBOARD")
        self.updatePos()

    def move(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Moves the ship according to its speed and direction.

        """
        if self.pathfinding["checkpoint"] is not None:
            self.computeHeading()
            self.rotateToHeading()
        self.setSpeed()
        self.updatePos()

        if self.checkpointReached(self.pathfinding["checkpoint"]):
            self.selectNextCheckpoint()

    def attack_move(self):
        angle = geo.angle(self.pos(), self.playerTarget.pos())
        o_point = QPointF(
            self.playerTarget.pos().x() - 18000 * math.cos(angle),
            self.playerTarget.pos().y() - 18000 * math.sin(angle),
        )
        # Tests if the optimum point is within an obstacle
        if self.gameScene.itemAt(o_point, self.gameScene.attachedGView.transform()):
            print("Point in an obstacle, generating new set of points")
            # If yes, computes new sets alternative points
            for i in range(1000, 4000, 1000):
                print("New set of points, at", i, " distance from original point")
                point_matrix = [
                    QPointF(o_point.x() + i, o_point.y() + i),
                    QPointF(o_point.x() - i, o_point.y() + i),
                    QPointF(o_point.x() + i, o_point.y() - i),
                    QPointF(o_point.x() - i, o_point.y() - i),
                ]
                for point in point_matrix:
                    # If a point in the new set is NOT within an obstacle, returns it
                    if not self.gameScene.itemAt(
                        point, self.gameScene.attachedGView.transform()
                    ):
                        print("Valid point found")
                        return point
                    print("No valid point in this set, new set")
        else:
            print("Point is valid")
            return o_point

        print("No valid point found! returning None !")
        return None

    def dynamicObjectDetection(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Cast detetcion rays at given angles in the frontal arc of the ship.
        Returns None if the detection rays don't intercept any objects, the list
        of distance of the detected object per detection ray otherwise.

        """
        det_distances = [None, None, None]
        _range = self.det_and_range["det_r_range"]

        for i, direction in enumerate(self.det_and_range["det_r_angles"]):
            det_distances[i] = self.gameScene.detectionRay(
                geo.parallelepiped_Center(
                    self.pos(), self.rect().width(), self.rect().height()
                ),
                math.radians(self.coordinates["heading"] + direction),
                _range,
                250,
                int((self.rect().width() / 2) + 50),
            )

        for distance in det_distances:
            if distance:
                return det_distances
        return None

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
            self,
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

    def isInRange(self, otherShip):
        """

        Parameters
        ----------
        otherShip: Ship object
            The ship to evaluate.

        Returns
        -------
        bool.

        Summary
        -------
        Calculate if othership is within gun range.
        Returns true if yes, false otherwise.

        """
        otherShipPos = geo.parallelepiped_Center(
            otherShip.pos(), otherShip.rect().width(), otherShip.rect().height()
        )
        distance = geo.distance_A_B(self.coordinates["center"], otherShipPos)
        if distance <= self.weapons["guns_range"]:
            return True
        return False

    def isTargetable(self, other_ship):
        """
        Parameters
        ----------
        other_ship : Ship Object
            An ennemy Ship

        Returns
        -------
        None.

        Summary
        -------
        Returns True if the selected enemy ship is Targetable,
        False otherwise.

        """
        ship_center = geo.parallelepiped_Center(
            other_ship.pos(), other_ship.rect().width(), other_ship.rect().height()
        )
        if (
            self.gameScene.isInLineOfSight(
                self.coordinates["center"], ship_center, 250,
            )
            and self.isInRange(other_ship)
            and other_ship in self.det_and_range["fleet_detected_ships"]
        ):
            return True
        return False

    def addNewTargets(self):
        """

        Returns
        -------
        sIR : list
            A list of all detected ennemy ships in gun range.

        Summary
        -------
        Computes and returns a list of all enney detected ships within gun range.

        """
        self.det_and_range["fleet_detected_ships"].clear()

        if self.det_and_range["detected_ships"]:
            self.det_and_range["fleet_detected_ships"].extend(
                self.det_and_range["detected_ships"]
            )
        if self.det_and_range["rcom_ships"]:
            self.det_and_range["fleet_detected_ships"].extend(
                self.det_and_range["rcom_ships"]
            )

        for ship in self.det_and_range["fleet_detected_ships"]:
            if ship.data(0) not in self.discoveredShips:
                _shipHeapItem = ShipHEAPItem(ship)
                self.targetList.addItem(_shipHeapItem)
                self.discoveredShips.append(ship.data(0))

    def setTarget(self, ennemyShip=None):
        """

        Parameters
        ----------
        ennemyShip : Ship[None]
            A Ship object

        Returns
        -------
        None.

        Summary
        -------
        Forces the current target to be ennemyShip.

        """
        self.playerTarget = ennemyShip

    def autoSelectTarget(self):
        """

        Returns
        -------
        tuple : (Ship, str)
            Ship: the ship object to target.
            str: The shot type to select.

        Summary
        -------
        Computes and return the best ship to set as target
        and the best suited shot type.

        """

        for shipheapitem in self.targetList.items:
            ship = shipheapitem.shipInstance
            shipheapitem.isTargetable = self.isTargetable(ship)
            if shipheapitem.isTargetable:
                (
                    shipheapitem.potentialDamage,
                    shipheapitem.idealShot,
                ) = self.evaluateTarget(ship)
                self.targetList.updateItem(shipheapitem)

        if len(self.targetList.items) > 0:
            for shipheapitem in self.targetList.items:
                if shipheapitem.isTargetable:
                    return (shipheapitem.shipInstance, shipheapitem.idealShot)

        return (None, None)

    def evaluateTarget(self, target):
        """

        Parameters
        ----------
        target: Ship
            The Ship object to evaluate.

        Returns
        -------
        tuple : (potential: float, shot_choice: str)

        Summary
        -------
        Computes the minimal amount of damage that can be done to target.

        """
        shot_choice = ""
        potential = 0
        ##################### COMPUTE HIT PROBABILITY PER SALVO #####################
        #############################################################################
        targetCenter = geo.parallelepiped_Center(
            target.pos(), target.rect().width(), target.rect().height()
        )
        targetDistance = round(
            geo.distance_A_B(self.coordinates["center"], targetCenter)
        )
        targetArea = round(target.rect().width() * target.rect().height())
        n_shots = (
            len(self.weapons["turrets_list"]) * self.weapons["turrets_list"][0].n_guns
        )
        azimut_error = math.radians(self.weapons["turrets_list"][0].gun_acc)
        errorOnD = self.p_dat["accy"] * targetDistance
        errorOnD = round(errorOnD)
        hitArea = round(
            errorOnD * math.tan(azimut_error) * (2 * targetDistance - errorOnD)
        )
        hitChance = targetArea / hitArea
        hitProbability = round(1 - (1 - hitChance) ** n_shots, 4)
        #############################################################################
        #############################################################################

        ####################### CHOOSES BEST SUITED SHOT TYPE #######################
        #############################################################################
        penAtDist = self.table[int(targetDistance / 1000)]
        dmgHE = min(
            int((self.p_dat["pen_HE"] / target.hull["armor"]) * self.p_dat["dmg_HE"]),
            self.p_dat["dmg_HE"],
        )
        if penAtDist > target.hull["armor"]:
            dmgAP = self.p_dat["dmg_AP"]
            if dmgHE > dmgAP:
                shot_choice = "HE"
                potential = dmgHE
            else:
                shot_choice = "AP"
                potential = dmgAP
        else:
            shot_choice = "HE"
            potential = dmgHE
        potential = round(potential * hitProbability)
        #############################################################################
        #############################################################################
        return (potential, shot_choice)

    def receiveDamage(self, value):
        self.instant_vars["hp"] -= value
        if self.instant_vars["hp"] < 0:
            self.instant_vars["hp"] = 0

    def receiveCritical(self, crit_code):
        if crit_code == 0:
            component_index = random.randint(0, 2)
            component_list = list(self.crit_components.keys())
            if self.crit_components[component_list[component_index]] == "OK":
                self.crit_components[component_list[component_index]] = "DAMAGED"
            elif self.crit_components[component_list[component_index]] == "DAMAGED":
                self.crit_components[component_list[component_index]] = "DESTROYED"

        if crit_code == 1:
            self.crit_components["FIRES"] += 1

    def repair(self):
        pass

    def spawnWeapons(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Spawns the turrets of the ship at predefined places. See documentation
        for further informations.

        """
        spawnPosList = [
            QPointF(self.x() + coord[0], self.y() + coord[1])
            for coord in self.weapons["turrets_pos"]
        ]

        for i, spawnPos in enumerate(spawnPosList):
            if self.weapons["turrets_size"] == "s":
                currentTurret = tur.small(self.clock, self.gameScene, self)
            elif self.weapons["turrets_size"] == "m":
                currentTurret = tur.medium(self.clock, self.gameScene, self)
            elif self.weapons["turrets_size"] == "l":
                currentTurret = tur.large(self.clock, self.gameScene, self)
            try:
                currentTurret.setPos(spawnPos)
                currentTurret.d_shipCenter = (
                    self.weapons["turrets_pos"][i][0] - self.rect().width() / 2
                )
                currentTurret.setZValue(3)
                self.gameScene.addItem(currentTurret)
                self.weapons["turrets_list"].append(currentTurret)
                currentTurret = None
            except Exception as e:
                print(e)
                print("Could not generate turret")

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
        elif self.naming["_type"] == "DD":
            txt = "Destroyer"
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
                num_guns = turret.n_guns
        if self.weapons["laser_turrets_list"] is not None:
            for laser in self.weapons["laser_turrets_list"]:
                num_laser += 1
        print("MAIN ARMAMENT:", str(num_turr), "turrets of ", str(num_guns), "guns")
        print("SECONDARY ARMAMENT:", str(num_laser), "laser turrets")
        print("")
        print("")
        print("**************** END ****************")
        print("")

    def setGizmos(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Spawns the ranges circles displays.

        """
        c = QPointF(
            self.pos().x() + self.rect().width() / 2,
            self.pos().y() + self.rect().height() / 2,
        )

        if self.data(1) == "ALLY":
            self.displays["rangeCirclesDisp"] = c_gizmo(
                c,
                self.instant_vars["detection_range"],
                self.weapons["guns_range"],
                "cyan",
                "blue",
            )
        else:
            self.displays["rangeCirclesDisp"] = c_gizmo(
                c,
                self.instant_vars["detection_range"],
                self.weapons["guns_range"],
                "yellow",
                "red",
            )

        color = "blue" if self.data(1) == "ALLY" else "red"
        self.displays["selected"] = r_gizmo(
            self.pos(), self.rect().width(), self.rect().height(), color
        )
        self.displays["lineToDestination"] = l_gizmo(
            self.rect().center(), self.rect().center(), "blue"
        )
        self.displays["lineToTarget"] = l_gizmo(
            self.rect().center(), self.rect().center(), "red"
        )
        for gizmo in self.displays.values():
            self.gameScene.addItem(gizmo)

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


class ShipHEAPItem(HEAP.HEAPItem):
    def __init__(self, ship):
        """
        Parameters
        ----------
        ship : Ship
            An object of class Ship.
        potential : float
            An evaluation of the potential damage that can be evaluated on this ship.

        Returns
        -------
        None.

        Summary
        -------
        Constructor of the class.

        """
        self.shipInstance = ship
        self.isTargetable = False
        self.potentialDamage = 0
        self.idealShot = ""

    def compareTo(self, otherShipHEAPItem):
        """

        Parameters
        ----------
        otherShipHEAPItem : ShipHEAPItem
            The other shipHEAPItem to compare this shipHEAPItem to.

        Returns
        -------
        int
            The result of the comparison.

        Summary
        -------
        Compares the shipHEAPItems according to their potential.
        Returns 1 if potential of this shipHEAPItem is lower, -1 if higher.
        Special case if both potentials are equal. See function in line comments.

        """
        # If the current shipHEAPItem has a lower potential than the shipHEAPItem's potential it is compared to.
        if self.potentialDamage <= otherShipHEAPItem.potentialDamage:
            return -1
        # If the current shipHEAPItem has a higher potential than the shipHEAPItem's potential it is compared to
        return 1
