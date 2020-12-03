# -*- coding: utf-8 -*-

'''
    File name: Ship.py
    Author: Grégory LARGANGE
    Date created: 09/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 03/12/2020
    Python version: 3.8.1
'''

import math

from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from library import MathsFormulas, InGameData


class Ship(QGraphicsRectItem):

    #--- USED FOR IDENTIFICATION IN GAME ---#
    shipID = None
    shipTag = ""
    #---------------------------------------#

    #--------- HULL CHARACTERISTICS --------#
    _type = "BB"
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
    guns_tech = 1
    fireControl_tech = 1
    computer_tech = 1
    radar_tech = 1
    radar_b_values = [0, 0.25, 0.37, 0.5]
    #---------------------------------------#

    #-------------- SCAN RATES -------------#
    radar_scan_rate = 9
    target_acquisition_rate = 9
    print_point_rate = 99  # TO DELETE ONLY FOR VISU
    #---------------------------------------#

    #------ CRITICAL COMPONENT STATES ------#
    bridge_state = "ok"
    engine_state = "ok"
    radar_state = "ok"
    shield_generator_state = "ok"
    #---------------------------------------#

    #-------- DETECTION AND RANGING --------#
    detected_ships = None
    rcom_ships = None
    ships_in_range = None
    #---------------------------------------#

    #-------------- PATHFINDING ------------#
    center = QPointF()
    r_centers = None
    trajectory = [QPointF(5000, 5000),
                  QPointF(10000, 2500),
                  QPointF(12500, 12500)]
    checkpoint = None
    sel_checkpoint_id = None
    is_final_checkpoint = True
    heading = 0
    t_heading = 0
    rot_direction = 0
    #---------------------------------------#

    def __init__(self, clock, gameScene):
        super(Ship, self).__init__(QRectF(0, 0, 0, 0))
        self.geometrics = MathsFormulas.Geometrics()
        self.cinematics = MathsFormulas.Cinematics()
        self.controllers = MathsFormulas.Controllers()
        self.projectileData = InGameData.ProjectileData()

        self.gameScene = gameScene
        self.clock = clock
        self.next_radarScan = 0
        self.next_targetAcquisition = 0
        self.next_point_print = 0  # TO DELETE ONLY FOR VISUALISATION

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
        self.updateCenter()
        self.updateRCenters()
        self.move()

        # TO BE DELETED WHEN NOT NEEDED #
        if self.next_point_print <= 0:
            self.gameScene.printPoint(self.center)
            if self.rot_direction < 0:
                self.gameScene.printPoint(self.r_centers[0])
            elif self.rot_direction > 0:
                self.gameScene.printPoint(self.r_centers[1])
            self.next_point_print = self.print_point_rate
        else:
            self.next_point_print -= 1
        #################################
        if self.next_radarScan <= 0:
            self.scan()
            self.ships_in_range = self.computeShipsInRange()
            self.next_radarScan = self.radar_scan_rate
        else:
            self.next_radarScan -= 1

        if self.next_targetAcquisition <= 0:
            for turret in self.gun_turrets_list:
                turret.set_Target(self.autoSelectTarget())
            self.next_targetAcquisition = self.target_acquisition_rate
        else:
            self.next_targetAcquisition -= 1

    def updateCenter(self):
        self.center = self.geometrics.parallelepiped_Center(self.pos(),
                                                            self.rect().width(),
                                                            self.rect().height())
    def updateRCenters(self):
        self.r_centers = self.cinematics.rotationCenters(self.center,
                                                         self.heading,
                                                         self.speed,
                                                         self.turn_rate)

    def accelerateToSpeed(self, speedOption):
        targetSpeed = 0

        if speedOption is None:
            targetSpeed = self.speed_options[self.default_speed]
        else:
            targetSpeed = self.speed_options[speedOption]

        self.speed += self.controllers.proportional(targetSpeed, self.speed, self.max_accel)

    def setSpeed(self):
        if self.checkpoint is None:
            if self.speed_user_override:
                self.accelerateToSpeed(self.speed_user_override)
                print("User overridde:", self.speed_user_override)
            else:
                self.accelerateToSpeed("STOP")
                print("No user override, using: STOP because no further checkpoints.")
        else:
            print("Remaining distance to checkpoint:", self.geometrics.distance_A_B(self.center,
                                                                                    self.checkpoint))
            brakeD = self.cinematics.brakeDistance(self.speed, -self.max_accel)
            # print("Calculated break distance at current speed", self.speed, ":", brakeD)
            if self.geometrics.distance_A_B(self.center, self.checkpoint) <= brakeD:
                # print("brake trigger distance reached")
                self.accelerateToSpeed("STOP")
            elif self.checkpointInTurnRadius() is False:
                print("Slowing down to match checkpoint")
                self.accelerateToSpeed("SLOW")
            else:
                if self.speed_user_override:
                    print("No brake triggers. Using user overridde:", self.speed_user_override)
                    self.accelerateToSpeed(self.speed_user_override)
                else:
                    print("No brake triggers. No user override. Using default speed:", self.default_speed)
                    self.accelerateToSpeed(self.default_speed)

    def computeHeading(self):
        distance = self.geometrics.distance_A_B(self.center, self.checkpoint)
        a_h = (self.checkpoint.x() - self.center.x()) / distance
        if a_h > 1.:
            a_h = 1
        elif a_h < -1:
            a_h = -1
        self.t_heading = round(math.degrees(math.acos(a_h)), 4)
        if (self.checkpoint.y() - self.center.y()) < 0:
            self.t_heading *= -1

    def rotateToHeading(self):
        diff = self.geometrics.smallestAngle(self.t_heading, self.heading)
        if diff < -0.5:
            self.rot_direction = -1
        elif diff > 0.5:
            self.rot_direction = 1
        else:
            self.rot_direction = 0
        self.heading += self.controllers.proportional(self.t_heading,
                                                      self.heading,
                                                      self.turn_rate, diff)
        self.setTransformOriginPoint(QPointF(self.rect().width() / 2,
                                             self.rect().height() / 2))
        self.setRotation(self.heading)

    def computeTrajectory(self):
        True

    def checkpointReached(self):
        if self.checkpoint is not None:
            toleranceRect = QRectF(self.checkpoint.x() - 250,
                                   self.checkpoint.y() - 250,
                                   500, 500)
            if toleranceRect.contains(self.center):
                # print("Checkpoint reached. Returning True")
                self.checkpoint = None
                return True
            else:
                return False
        else:
            # print("No checkpoints, returning True")
            return True

    def selectNextCheckpoint(self):
        # print("Selecting new checkpoint...")
        if self.trajectory is None:
            self.checkpoint = None
            self.sel_checkpoint_id = None
            # print("No trajectory to follow")
        else:
            if self.sel_checkpoint_id is None:
                # print("Selecting first checkpoint")
                self.checkpoint = self.trajectory[0]
                # print(self.checkpoint.x(), self.checkpoint.y())
                self.sel_checkpoint_id = 0
            else:
                # print("Selecting next checkpoint")
                if self.sel_checkpoint_id + 1 <= len(self.trajectory) - 1:
                    self.sel_checkpoint_id += 1
                    self.checkpoint = self.trajectory[self.sel_checkpoint_id]
                else:
                    # print("No more checkpoints. Passing everything to None")
                    self.trajectory = None
                    self.chekpoint = None
                    self.sel_checkpoint = None

    def checkpointInTurnRadius(self):
        rot_center = QPointF()

        if self.rot_direction < 0:
            rot_center = self.r_centers[0]
        elif self.rot_direction > 0:
            rot_center = self.r_centers[1]
        else:
            print("No turning detected")
            return None

        if self.geometrics.distance_A_B(rot_center, self.checkpoint) <\
            self.cinematics.rotationRadius(self.speed, self.turn_rate):
            print("Checkpoint is not reachable")
            return False
        else:
            print("Checkpoint is reachable")
            return True

    def updateTurretPos(self):
        for turret in self.gun_turrets_list:
            tur_angle = 180 if turret.d_shipCenter < 0 else 0
            teta = math.radians(self.heading + tur_angle)
            r = abs(turret.d_shipCenter)
            nextTurPosX = self.center.x() + r * math.cos(teta)
            nextTurPosY = self.center.y() - 25 + r * math.sin(teta)

            turret.setPos(nextTurPosX, nextTurPosY)

    def move(self):
        if self.checkpoint is not None:
            self.computeHeading()
            self.rotateToHeading()
        self.setSpeed()
        headingInRad = math.radians(self.heading)
        nextPoint = self.cinematics.movementBy(self.pos(), self.speed,
                                               headingInRad)
        self.setPos(nextPoint)
        self.updateTurretPos()

        if self.checkpointReached():
            self.selectNextCheckpoint()

    def scan(self):
        self.detected_ships = self.gameScene.shipsInDetectionRange(self.shipID,
                                                                   self.shipTag,
                                                                   self.center,
                                                                   self.detection_range)

    def receiveRadioComm(self, infosList):
        self.rcom_ships = infosList

    def computeShipsInRange(self):
        sIR = []

        if self.detected_ships is not None:
            if len(self.detected_ships) > 0:
                for ship in self.detected_ships:
                    detSCPos = self.geometrics.parallelepiped_Center(
                        ship.pos(), ship.rect().width(), ship.rect().height())
                    distance = self.geometrics.distance_A_B(self.center, detSCPos)
                    if distance <= self.guns_range:
                        sIR.append(ship)
        if self.rcom_ships is not None:
            if len(self.rcom_ships) > 0:
                for ship in self.rcom_ships:
                    if ship not in sIR:
                        detSCPos = self.geometrics.parallelepiped_Center(
                            ship.pos(), ship.rect().width(), ship.rect().height())
                        distance = self.geometrics.distance_A_B(self.center, detSCPos)
                        if distance <= self.guns_range:
                            sIR.append(ship)
        return sIR

    def autoSelectTarget(self):
        target = None

        if self.ships_in_range is not None:
            if len(self.ships_in_range) > 0:
                target = self.ships_in_range[0]
        return target

    def repair(self):
        True

    def setID(self, shipId):
        self.shipID = shipId

    def setTag(self, shipTag):
        self.shipTag = shipTag

    def printInfos(self):
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
        print("FIRE CONTROL TECHNOLOGY:", "Mk", str(self.fireControl_tech))
        print("TARGETING COMPUTER TECHNOLOGY:", "Mk", str(self.computer_tech))
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
        if self.shipTag == "ALLY":
            painter.setBrush(QBrush(QColor("blue")))
            painter.setPen(QPen(QColor("darkBlue"), 10))
        if self.shipTag == "ENNEMY":
            painter.setBrush(QBrush(QColor("red")))
            painter.setPen(QPen(QColor("darkred"), 10))
        painter.drawEllipse(self.rect())
