# -*- coding: utf-8 -*-

'''
    File name: Gun_Turret.py
    Author: Grégory LARGANGE
    Date created: 12/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 14/12/2020
    Python version: 3.8.1
'''

import math
import random

from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from library import Projectile


class GunTurret(QGraphicsRectItem):

    d_shipCenter = 0
    refresh_rate = 10
    shell_t = "HE"
    azimut = 0
    fc_correction_rate = 150

    target = None
    t_id = None
    t_azimut = 0
    t_range = 0
    t_x_1 = t_v_x = 0
    t_y_1 = t_v_y = 0

    def __init__(self, clock, gameScene, tur_type, gun_tech, fc_tech, pc_tech,
                 parent=None):
        """

        Parameters
        ----------
        clock : MainClock
            The main clock of the game.
        gameScene : GameScene
            The main display of the game.
        tur_type : str
            The size of the turret. See InGameData.py file for further informations.
        gun_tech : int
            The technology level of the guns. See InGameData.py file for further
            informations.
        fc_tech : int
            The technology level of the fire control. See InGameData.py file for
            further informations.
        pc_tech : int
            The technology level of the targeting computer. See InGameData.py
            file for further informations.
        parent : Ship, optional
            The parent Ship object of the turret. The default is None.

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        super(GunTurret, self).__init__(QRectF(0, 0, 0, 0), parent)

        self.clock = clock
        self.gameScene = gameScene
        self.parentShip = parent
        self.p_data = self.parentShip.projectileData
        t_data = self.parentShip.turretData
        tech_data = self.parentShip.techData

        # Sets turret parameters from t_data according to passed tur_type #
        if tur_type == "s":
            rect = QRectF(0, 0, t_data.rect_values[0] * t_data.w_h_ratio,
                          t_data.rect_values[0])
            self.thickness = t_data.thk_values[0]
            self.rot_speed = t_data.rot_rate_values[0]
            self.acc_f = t_data.acc_f_values[0]
            self.gun_number = t_data.n_guns[0]
            self.reloadTime = t_data.reload_t_values[0]
            self.shell_s = self.p_data.size_tags[0]
        elif tur_type == "m":
            rect = QRectF(0, 0, t_data.rect_values[1] * t_data.w_h_ratio,
                          t_data.rect_values[1])
            self.thickness = t_data.thk_values[1]
            self.rot_speed = t_data.rot_rate_values[1]
            self.acc_f = t_data.acc_f_values[1]
            self.gun_number = t_data.n_guns[1]
            self.reloadTime = t_data.reload_t_values[1]
            self.shell_s = self.p_data.size_tags[1]
        elif tur_type == "l":
            rect = QRectF(0, 0, t_data.rect_values[2] * t_data.w_h_ratio,
                          t_data.rect_values[2])
            self.thickness = t_data.thk_values[2]
            self.rot_speed = t_data.rot_rate_values[2]
            self.acc_f = t_data.acc_f_values[2]
            self.gun_number = t_data.n_guns[2]
            self.reloadTime = t_data.reload_t_values[2]
            self.shell_s = self.p_data.size_tags[2]

        # Sets gun_acc parameters from tech_data according to passed gun_tech #
        self.gun_acc = round(tech_data.gun_tech_acc[gun_tech] * self.acc_f, 4)

        # Sets base_fc_error parameters from tech_data according to passed fc_tech #
        self.base_fc_error = tech_data.fc_tech_e[fc_tech]
        self.fc_error = self.base_fc_error

        # Sets fc_e_reduc_rate parameters from tech_data according to passed pc_tech #
        self.fc_e_reduc_rate = tech_data.pc_tech_reduc[pc_tech]

        self.setRect(rect)
        self.nextShot = self.reloadTime
        self.next_fc_correction = self.fc_correction_rate

        self.clock.clockSignal.connect(self.fixed_update)
        self.printInfos(tur_type)

    def fixed_update(self):
        if self.nextShot > 0:
            self.nextShot -= 1
        if self.target is not None:
            if self.next_fc_correction <= 0:
                self.fc_Error_Reduction()
                self.next_fc_correction = self.fc_correction_rate
            else:
                self.next_fc_correction -= 1
            self.compute_Firing_Solution()
            self.rotate_To_T_Azimut()
            if (self.t_azimut - self.azimut < 1) |\
                ((self.t_azimut - self.azimut > 359) & (self.t_azimut - self.azimut < 361)):
                if self.nextShot <= 0:
                    self.shoot()
                    self.nextShot = self.reloadTime
        else:
            self.t_azimut = self.parentShip.heading
            self.rotate_To_T_Azimut()

    def set_Target(self, targetObject):
        self.target = targetObject
        if self.target is not None:
            if (self.t_id is None) or (targetObject.shipID != self.t_id):
                self.t_id = self.target.shipID
                self.t_x_1 = self.target.pos().x()
                self.t_y_1 = self.target.pos().y()
                self.fc_error = self.base_fc_error
            else:
                self.t_v_x = self.target.pos().x() - self.t_x_1
                self.t_v_y = self.target.pos().y() - self.t_y_1
                self.t_x_1 = self.target.pos().x()
                self.t_y_1 = self.target.pos().y()

    def compute_Firing_Solution(self):
        shellSpeed = self.p_data.speeds_shellType[0] if self.shell_t == "AP" else\
            self.p_data.speeds_shellType[1]
        shellSpeed *= self.refresh_rate
        estimatedFlightTime = round(self.t_range / shellSpeed, 4)
        estimated_t_speed_x = self.fc_RNG_Error(self.t_v_x)
        estimated_t_speed_y = self.fc_RNG_Error(self.t_v_y)
        estimatedPos = QPointF(self.target.pos().x() + estimated_t_speed_x * estimatedFlightTime,
                               self.target.pos().y() + estimated_t_speed_y * estimatedFlightTime)
        estimatedCenter = self.parentShip.geometrics.parallelepiped_Center(
            estimatedPos, self.target.rect().width(), self.target.rect().height())
        self.t_range = int(self.parentShip.geometrics.distance_A_B(self.pos(), estimatedCenter))
        a_h = (estimatedCenter.x() - self.pos().x()) / self.t_range
        if a_h > 1.:
            a_h = 1
        elif a_h < -1:
            a_h = -1
        self.t_azimut = round(math.degrees(math.acos(a_h)), 4)
        if (estimatedCenter.y() - self.pos().y()) < 0:
            self.t_azimut *= -1

    def rotate_To_T_Azimut(self):
        static_gain = 1

        diff = self.parentShip.geometrics.smallestAngle(self.t_azimut,
                                                        self.azimut)
        gain = static_gain * (diff)
        if gain < -self.rot_speed:
            gain = -self.rot_speed
        elif gain > self.rot_speed:
            gain = self.rot_speed
        self.azimut += gain
        self.setTransformOriginPoint(QPointF(self.rect().width() / 2,
                                              self.rect().height() / 2))
        self.setRotation(self.azimut)

    def choose_Shell_Type(self, shell_type):
        self.shell_t = shell_type

    def gun_Dispersion(self):
        sign = random.random()
        disp = round(random.uniform(0, self.gun_acc), 4)
        return self.azimut - disp if sign < 0.5 else self.azimut + disp

    def fc_RNG_Error(self, speedInput):
        error = self.fc_error * speedInput
        speedOutput = random.uniform(speedInput - error, speedInput + error)
        return speedOutput

    def fc_Error_Reduction(self):
        self.fc_error -= self.base_fc_error * self.fc_e_reduc_rate
        if self.fc_error < 0:
            self.fc_error = 0

    def compute_SpawnsPos(self, yposOnTur, angleInRad):
        h = self.parentShip.geometrics.pythagore(self.rect().width(), yposOnTur)
        teta_offset = math.acos(self.rect().width() / h)
        teta_t = angleInRad + teta_offset
        xpos = self.x() + h * math.cos(teta_t)
        ypos = self.y() + self.rect().height() + h * math.sin(teta_t)
        spawnPos = QPointF(xpos, ypos)
        return spawnPos

    def shoot(self):
        az_rad = math.radians(self.azimut)

        if self.gun_number == 1:
            a = self.gun_Dispersion()
            shell = Projectile.Projectile(self.clock, self.gameScene, self.p_data,
                                          a, self.t_range, self.shell_s, self.shell_t)
            spawnPos = self.compute_SpawnsPos(13, az_rad)
            shell.setPos(spawnPos)

            self.gameScene.addItem(shell)

        elif self.gun_number == 2:
            a = self.gun_Dispersion()
            shell0 = Projectile.Projectile(self.clock, self.gameScene, self.p_data,
                                           a, self.t_range, self.shell_s, self.shell_t)
            spawnPos = self.compute_SpawnsPos(10, az_rad)
            shell0.setPos(spawnPos)

            a = self.gun_Dispersion()
            shell1 = Projectile.Projectile(self.clock, self.gameScene, self.p_data,
                                           a, self.t_range, self.shell_s, self.shell_t)
            spawnPos = self.compute_SpawnsPos(40, az_rad)
            shell1.setPos(spawnPos)

            self.gameScene.addItem(shell0)
            self.gameScene.addItem(shell1)

        elif self.gun_number == 3:
            a = self.gun_Dispersion()
            shell0 = Projectile.Projectile(self.clock, self.gameScene, self.p_data,
                                           a, self.t_range, self.shell_s, self.shell_t)
            spawnPos = self.compute_SpawnsPos(5, az_rad)
            shell0.setPos(spawnPos)

            a = self.gun_Dispersion()
            shell1 = Projectile.Projectile(self.clock, self.gameScene, self.p_data,
                                           a, self.t_range, self.shell_s, self.shell_t)
            spawnPos = self.compute_SpawnsPos(50, az_rad)
            shell1.setPos(spawnPos)

            a = self.gun_Dispersion()
            shell2 = Projectile.Projectile(self.clock, self.gameScene, self.p_data,
                                           a, self.t_range, self.shell_s, self.shell_t)
            spawnPos = self.compute_SpawnsPos(95, az_rad)
            shell2.setPos(spawnPos)

            self.gameScene.addItem(shell0)
            self.gameScene.addItem(shell1)
            self.gameScene.addItem(shell2)

    def set_refreshRate(self, refreshRateValue):
        self.refresh_rate = refreshRateValue

    def setDFromShipCenter(self, distanceFromCenter):
        self.d_shipCenter = distanceFromCenter

    def printInfos(self, turretType):
        print("********* GENERATED TURRET: *********")
        if turretType == "s":
            txt = "Small"
        elif turretType == "m":
            txt = "Medium"
        elif turretType == "l":
            txt = "Large"
        print("SYZE:", txt)
        print("GUNS:", str(self.gun_number))
        print("ROTATION SPEED:", str(self.rot_speed) + "°/s")
        print("RELOAD SPEED:", str(self.reloadTime) + "s")
        print("GUNS ACCURACY:", str(self.gun_acc) + "°")
        print("BASE FIRE CONTROL ERROR:", str(100 * self.base_fc_error) + "%")
        print("FC ERROR REDUCTION RATE:", str(100 * self.fc_e_reduc_rate) + "%")
        print("**************** END ****************")
        print("")

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor("darkGray")))
        painter.setPen(QPen(QColor("black"), self.thickness))
        painter.drawRect(self.rect())
