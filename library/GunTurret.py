# -*- coding: utf-8 -*-

'''
    File name: Gun_Turret.py
    Author: Grégory LARGANGE
    Date created: 12/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 15/10/2020
    Python version: 3.8.1
'''

import math
import random

from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from library import MathsFormulas, Projectile


class GunTurret(QGraphicsRectItem):

    rect_values = [25, 50, 100]
    thk_values = [5, 10, 10]
    d_shipCenter = 0

    refresh_rate = 10
    rot_rate_values = [3.6, 2.4, 1.2]
    acc_f_values = [0.6, 0.8, 1]
    reload_t_values = [50, 75, 150]

    shell_s_values = ["s", "m", "l"]
    shell_t = "HE"

    azimut = 0

    fc_correction_rate = 150

    target = None
    t_id = None
    t_azimut = 0
    t_range = 0
    t_x_1 = t_v_x = 0
    t_y_1 = t_v_y = 0

    def __init__(self, clock, gameScene, tur_type, gun_tech, fc_tech, pc_tech, parent=None):
        super(GunTurret, self).__init__(QRectF(0, 0, 0, 0), parent)

        self.clock = clock
        self.gameScene = gameScene
        self.parentShip = parent

        if tur_type == "s":
            rect = QRectF(0, 0, self.rect_values[0] * 1.25, self.rect_values[0])
            self.thickness = self.thk_values[0]
            self.rot_speed = self.rot_rate_values[0]
            self.acc_f = self.acc_f_values[0]
            self.gun_number = 1
            self.reloadTime = self.reload_t_values[0]
            self.shell_s = self.shell_s_values[0]
        elif tur_type == "m":
            rect = QRectF(0, 0, self.rect_values[1] * 1.25, self.rect_values[1])
            self.thickness = self.thk_values[1]
            self.rot_speed = self.rot_rate_values[1]
            self.acc_f = self.acc_f_values[1]
            self.gun_number = 2
            self.reloadTime = self.reload_t_values[1]
            self.shell_s = self.shell_s_values[1]
        elif tur_type == "l":
            rect = QRectF(0, 0, self.rect_values[2] * 1.25, self.rect_values[2])
            self.thickness = self.thk_values[2]
            self.rot_speed = self.rot_rate_values[2]
            self.acc_f = self.acc_f_values[2]
            self.gun_number = 3
            self.reloadTime = self.reload_t_values[2]
            self.shell_s = self.shell_s_values[2]

        ## For this section accuracy is in degrees for later use by the scripts.
        ## The formula is: acc(deg) = tan-1(disp(units)/range(units))
        if gun_tech == 1:
            self.gun_acc = round(5.7106 * self.acc_f, 4)  # degrees
        elif gun_tech == 2:
            self.gun_acc = round(4.2891 * self.acc_f, 4)  # degrees
        elif gun_tech == 3:
            self.gun_acc = round(2.8624 * self.acc_f, 4)  # degrees

        if fc_tech == 1:
            self.base_fc_error = 0.3
        elif fc_tech == 2:
            self.base_fc_error = 0.2
        elif fc_tech == 3:
            self.base_fc_error = 0.1
        self.fc_error = self.base_fc_error

        if pc_tech == 1:
            self.fc_e_reduc_rate = 0.1
        elif pc_tech == 2:
            self.fc_e_reduc_rate = 0.25
        elif pc_tech == 3:
            self.fc_e_reduc_rate = 0.5

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
        shellSpeed = self.parentShip.projectileData.speeds_shellType[0] if self.shell_t == "AP" else\
            self.parentShip.projectileData.speeds_shellType[1]
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
        ypos = self.y() + self.rect().height()+ h * math.sin(teta_t)
        spawnPos = QPointF(xpos, ypos)
        return spawnPos

    def shoot(self):
        az_rad = math.radians(self.azimut)
    
        if self.gun_number == 1:
            a = self.gun_Dispersion()
            shell = Projectile.Projectile(self.clock, self.gameScene,
                                      a, self.t_range, self.shell_s,
                                      self.shell_t)
            spawnPos = self.compute_SpawnsPos(13, az_rad)
            shell.setPos(spawnPos)
    
            self.gameScene.addItem(shell)
    
        elif self.gun_number == 2:
            a = self.gun_Dispersion()
            shell0 = Projectile.Projectile(self.clock, self.gameScene,
                                      a, self.t_range, self.shell_s,
                                      self.shell_t)
            spawnPos = self.compute_SpawnsPos(10, az_rad)
            shell0.setPos(spawnPos)
    
            a = self.gun_Dispersion()
            shell1 = Projectile.Projectile(self.clock, self.gameScene,
                                      a, self.t_range, self.shell_s,
                                      self.shell_t)
            spawnPos = self.compute_SpawnsPos(40, az_rad)
            shell1.setPos(spawnPos)
    
            self.gameScene.addItem(shell0)
            self.gameScene.addItem(shell1)
    
        elif self.gun_number == 3:
            a = self.gun_Dispersion()
            shell0 = Projectile.Projectile(self.clock, self.gameScene,
                                      a, self.t_range, self.shell_s,
                                      self.shell_t)
            spawnPos = self.compute_SpawnsPos(5, az_rad)
            shell0.setPos(spawnPos)
    
            a = self.gun_Dispersion()
            shell1 = Projectile.Projectile(self.clock, self.gameScene,
                                      a, self.t_range, self.shell_s,
                                      self.shell_t)
            spawnPos = self.compute_SpawnsPos(50, az_rad)
            shell1.setPos(spawnPos)
    
            a = self.gun_Dispersion()
            shell2 = Projectile.Projectile(self.clock, self.gameScene,
                                      a, self.t_range, self.shell_s,
                                      self.shell_t)
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
