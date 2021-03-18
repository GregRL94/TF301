# -*- coding: utf-8 -*-

'''
    File name: Gun_Turret.py
    Author: Grégory LARGANGE
    Date created: 12/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 18/03/2020
    Python version: 3.8.1
'''

import math
import random

from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from library import Projectile
from library.MathsFormulas import Geometrics as geo, Controllers as con
from library.InGameData import ProjectileData as p_dat, TurretData as tur_dat,\
    TechsData as tech_dat


class GunTurret(QGraphicsRectItem):
    """

    A class handling the creation and behaviour of turrets.

    ...

    Attributes
    ----------
    d_shipCenter : int
        The distance between the turret center and its parent ship center.

    shell_t : string
        The tag defining which shell type to fire.

    azimut : float
        The current rotation angle of the turret.

    target : Ship
        The current Ship object targeted by the turret.

    t_id : int
        The id of the Ship object being targeted.

    t_azimut : float
        The angle at which is the target in the turret referential.

    t_range : float
        The distance between the target center and the turret center.

    t_x_1 : float
        The position on the x axis of the target in the scene referential at
        time t-1 (the previous refresh).

    t_y_1 : float
        The position on the y axis of the target in the scene referential at
        time t-1 (the previous refresh).

    t_v_x : float
        The instantaneous speed of the target on the x axis.

    t_v_y : float
        The instantaneous speed of the target on the y axis.

    Methods
    -------
    __init__(clock : MainClock, gameScene : GameScene, tur_size : string,
             parent[None] : Ship)
        The constructor of the class.

    fixedUpdate()
        Called every clock signal, this function updates every aspect of the
        turret.
        Nota: The turret position is not taken care of by the turret itself, but
        by its parent.

    setTarget(targetObject : Ship)
        Sets the target of the turret to be the given Ship object.

    computeFiringSolution()
        Calculate the angle at which to rotate the turret to in order to hit the
        target.

    rotateToTAzimut()
        Rotates the turret towards target angle.

    chooseShellType(shell_type : string)
        Selects the type of shell to shoot depending on shell_type.

    gunDispersion()
        Applies a random dispersion depending on gun_acc to the azimut of an
        individual gun.

    fcREG()
        Applies a random error depending on fc_error to the input mesured target
        speed.

    fcErrorReduction()
        Gradually reduces the error fc_error depending on fc_e_reduc_rate.

    computeSpawnPos(yposOnTur : int, angleInRad : float)
        Computes the spawn position of a projectile depending on the position
        of the gun in the turret, and the current turret rotation.

    shoot()
        Spawn projectiles.

    setDFromShipCenter(distanceFromCenter : float)
        Sets the distance between the center of the turret and its parent ship
        center.

    printInfos()
        Print onfos about the turret.

    paint()
        Instructions to draw the item on the game scene.

    """

    d_shipCenter = 0
    shell_t = "HE"
    azimut = 0

    target = None
    t_id = None
    t_azimut = 0
    t_range = 0
    t_x_1 = t_v_x = 0
    t_y_1 = t_v_y = 0

    def __init__(self, clock, gameScene, tur_size, parent=None):
        """

        Parameters
        ----------
        clock : MainClock
            The main clock of the game.
        gameScene : GameScene
            The main display of the game.
        tur_size : str
            The size of the turret. See InGameData.py file for further informations.
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

        # Sets turret parameters from tur_dat according to passed tur_size #
        if tur_size == "s":
            rect = QRectF(0, 0, tur_dat.rect_values[0] * tur_dat.w_h_ratio,
                          tur_dat.rect_values[0])
            self.thickness = tur_dat.thk_values[0]
            self.rot_speed = tur_dat.rot_rate_values[0]
            self.acc_f = tur_dat.acc_f_values[0]
            self.gun_number = tur_dat.n_guns[0]
            self.reloadTime = tur_dat.reload_t_values[0]
            self.shell_s = p_dat.size_tags[0]
        elif tur_size == "m":
            rect = QRectF(0, 0, tur_dat.rect_values[1] * tur_dat.w_h_ratio,
                          tur_dat.rect_values[1])
            self.thickness = tur_dat.thk_values[1]
            self.rot_speed = tur_dat.rot_rate_values[1]
            self.acc_f = tur_dat.acc_f_values[1]
            self.gun_number = tur_dat.n_guns[1]
            self.reloadTime = tur_dat.reload_t_values[1]
            self.shell_s = p_dat.size_tags[1]
        elif tur_size == "l":
            rect = QRectF(0, 0, tur_dat.rect_values[2] * tur_dat.w_h_ratio,
                          tur_dat.rect_values[2])
            self.thickness = tur_dat.thk_values[2]
            self.rot_speed = tur_dat.rot_rate_values[2]
            self.acc_f = tur_dat.acc_f_values[2]
            self.gun_number = tur_dat.n_guns[2]
            self.reloadTime = tur_dat.reload_t_values[2]
            self.shell_s = p_dat.size_tags[2]

        # Sets gun_acc parameters from tech_dat according to parent gun_tech #
        self.gun_acc = round(tech_dat.gun_tech_acc[self.parentShip.gun_tech] * self.acc_f, 4)

        # Sets base_fc_error parameters from tech_dat according to parent fc_tech #
        self.base_fc_error = tech_dat.fc_tech_e[self.parentShip.fc_tech]
        self.fc_error = self.base_fc_error

        # Sets fc_e_reduc_rate parameters from tech_dat according to parent pc_tech #
        self.fc_e_reduc_rate = tech_dat.pc_tech_reduc[self.parentShip.pc_tech]

        self.setRect(rect)
        self.nextShot = self.reloadTime
        self.fc_corr_rate = tech_dat.fc_correction_rate
        self.next_fc_correction = self.fc_corr_rate

        self.clock.clockSignal.connect(self.fixedUpdate)
        self.printInfos(tur_size)

    def fixedUpdate(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Called at each clock signal. Updates all time bound functions like
        reloading, rotating, firing solution...

        """
        if self.nextShot > 0:
            self.nextShot -= 1
        if self.target:
            if self.next_fc_correction <= 0:
                self.fcErrorReduction()
                self.next_fc_correction = self.fc_corr_rate
            else:
                self.next_fc_correction -= 1
            self.computeFiringSolution()
            self.rotateToTAzimut()
            if (self.t_azimut - self.azimut < 1) |\
                ((self.t_azimut - self.azimut > 359) & (self.t_azimut - self.azimut < 361)):
                if self.nextShot <= 0:
                    self.shoot()
                    self.nextShot = self.reloadTime
        else:
            self.t_azimut = self.parentShip.heading
            self.rotateToTAzimut()

    def setTarget(self, targetObject):
        """

        Parameters
        ----------
        targetObject : Ship
            A Ship class object.

        Returns
        -------
        None.

        Summary
        -------
        Sets the target of the turret if any. Updates the position information
        of the target if any.

        """
        self.target = targetObject
        if self.target:
            # If there was no target before or the target has changed
            if (self.t_id is None) or (targetObject.data(0) != self.t_id):
                self.t_id = self.target.data(0)
                # Stores the position of the target
                self.t_x_1 = self.target.pos().x()
                self.t_y_1 = self.target.pos().y()
                # Resets the error on the speed estimation
                self.fc_error = self.base_fc_error
            # If the target is the same as the previously selected target
            else:
                # Get the speed from substracting the position of the target at t-1
                # from its current position (at t)
                self.t_v_x = self.target.pos().x() - self.t_x_1
                self.t_v_y = self.target.pos().y() - self.t_y_1
                # Updates the position of the target at t-1
                self.t_x_1 = self.target.pos().x()
                self.t_y_1 = self.target.pos().y()

    def computeFiringSolution(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Calculates the angle at which to rotate the turret in order to hit a
        target.

        """
        shellSpeed = p_dat.speeds_shellType[0] if self.shell_t == "AP" else p_dat.speeds_shellType[1]
        shellSpeed *= self.parentShip.refresh_rate  # We accomodate for the fact that the firing soluting is not computed every frame
        estimatedFlightTime = round(self.t_range / shellSpeed, 4)
        estimated_t_speed_x = self.fcREG(self.t_v_x)
        estimated_t_speed_y = self.fcREG(self.t_v_y)
        # See docs for more infos on the maths
        estimatedPos = QPointF(self.target.pos().x() + estimated_t_speed_x * estimatedFlightTime,
                               self.target.pos().y() + estimated_t_speed_y * estimatedFlightTime)
        estimatedCenter = geo.parallelepiped_Center(estimatedPos, self.target.rect().width(), self.target.rect().height())
        self.t_range = int(geo.distance_A_B(self.pos(), estimatedCenter))
        a_h = (estimatedCenter.x() - self.pos().x()) / self.t_range
        # Avoid non definition errors
        if a_h > 1.:
            a_h = 1
        elif a_h < -1:
            a_h = -1
        self.t_azimut = round(math.degrees(math.acos(a_h)), 4)
        # Determine the sign of the angle
        if (estimatedCenter.y() - self.pos().y()) < 0:
            self.t_azimut *= -1

    def rotateToTAzimut(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Applies a basic controller to rotate the turret from its current angle
        to the target angle.

        """
        diff = geo.smallestAngle(self.t_azimut, self.azimut)

        self.azimut += con.proportional(self.t_azimut, self.azimut, self.rot_speed, diff)
        self.setTransformOriginPoint(QPointF(self.rect().width() / 2, self.rect().height() / 2))
        self.setRotation(self.azimut)

    def chooseShellType(self, shell_type):
        """

        Parameters
        ----------
        shell_type : string
            The type of the shell.

        Returns
        -------
        None.

        Summary
        -------
        Sets the type of shell to be used by the turret.

        """
        self.shell_t = shell_type

    def gunDispersion(self):
        """

        Returns
        -------
        float
            The randomized angle.

        Summary
        -------
        Applies a random dispersion depending on gun_acc to the azimut.

        """
        sign = random.random()
        disp = round(random.uniform(0, self.gun_acc), 4)
        return self.azimut - disp if sign < 0.5 else self.azimut + disp

    def fcREG(self, speedInput):
        """

        Parameters
        ----------
        speedInput : float
            The speed og the target.

        Returns
        -------
        speedOutput : float
            The randomized speed.

        Summary
        -------
        Applies a random error depending on fc_error to the input speed.

        """
        error = self.fc_error * speedInput
        speedOutput = random.uniform(speedInput - error, speedInput + error)
        return speedOutput

    def fcErrorReduction(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Gradually reduces the error fc_error depending on fc_e_reduc_rate.

        """
        self.fc_error -= self.base_fc_error * self.fc_e_reduc_rate
        if self.fc_error < 0:
            self.fc_error = 0

    def computeSpawnPos(self, yposOnTur, angleInRad):
        """

        Parameters
        ----------
        yposOnTur : int
            The y position of the gun in the turret referential.
        angleInRad : float
            The current angle of the turret.

        Returns
        -------
        spawnPos : QPointF
            The position of the spawn.

        Summary
        -------
        Computes the spawn position of a projectile depending on the position
        of the gun in the turret, and the current turret rotation.

        """
        h = geo.pythagore(self.rect().width(), yposOnTur)
        teta_offset = math.acos(self.rect().width() / h)
        teta_t = angleInRad + teta_offset
        xpos = self.x() + h * math.cos(teta_t)
        ypos = self.y() + self.rect().height() + h * math.sin(teta_t)
        spawnPos = QPointF(xpos, ypos)
        return spawnPos

    def shoot(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Spawn projectiles.

        """
        az_rad = math.radians(self.azimut)

        # Appliable to all: setZValue defines which item will be drawn on top of another.
        # The item with the highest Z value will be on top.
        if self.gun_number == 1:
            a = self.gunDispersion()
            shell = Projectile.Projectile(self.clock, self.gameScene, a, self.t_range,
                                          self.shell_s, self.shell_t)
            spawnPos = self.computeSpawnPos(13, az_rad)
            shell.setZValue(4)
            shell.setPos(spawnPos)

            self.gameScene.addItem(shell)

        elif self.gun_number == 2:
            a = self.gunDispersion()
            shell0 = Projectile.Projectile(self.clock, self.gameScene, a, self.t_range,
                                           self.shell_s, self.shell_t)
            spawnPos = self.computeSpawnPos(10, az_rad)
            shell0.setZValue(4)
            shell0.setPos(spawnPos)

            a = self.gunDispersion()
            shell1 = Projectile.Projectile(self.clock, self.gameScene, a, self.t_range,
                                           self.shell_s, self.shell_t)
            spawnPos = self.computeSpawnPos(40, az_rad)
            shell1.setZValue(4)
            shell1.setPos(spawnPos)

            self.gameScene.addItem(shell0)
            self.gameScene.addItem(shell1)

        elif self.gun_number == 3:
            a = self.gunDispersion()
            shell0 = Projectile.Projectile(self.clock, self.gameScene, a, self.t_range,
                                           self.shell_s, self.shell_t)
            spawnPos = self.computeSpawnPos(5, az_rad)
            shell0.setZValue(4)
            shell0.setPos(spawnPos)

            a = self.gunDispersion()
            shell1 = Projectile.Projectile(self.clock, self.gameScene, a, self.t_range,
                                           self.shell_s, self.shell_t)
            spawnPos = self.computeSpawnPos(50, az_rad)
            shell1.setZValue(4)
            shell1.setPos(spawnPos)

            a = self.gunDispersion()
            shell2 = Projectile.Projectile(self.clock, self.gameScene, a, self.t_range,
                                           self.shell_s, self.shell_t)
            spawnPos = self.computeSpawnPos(95, az_rad)
            shell2.setZValue(4)
            shell2.setPos(spawnPos)

            self.gameScene.addItem(shell0)
            self.gameScene.addItem(shell1)
            self.gameScene.addItem(shell2)

    def setDFromShipCenter(self, distanceFromCenter):
        """

        Parameters
        ----------
        distanceFromCenter : int
            Distance from the turret to its parent ship center.

        Returns
        -------
        None.

        Summary
        -------
        Sets the distance between the center of the turret and its parent ship
        center.

        """
        self.d_shipCenter = distanceFromCenter

    def printInfos(self, turretSize):
        """

        Parameters
        ----------
        turretSize : string
            The size of the turret.

        Returns
        -------
        None.

        Summary
        -------
        Print onfos about the turret.

        """
        print("********* GENERATED TURRET: *********")
        if turretSize == "s":
            txt = "Small"
        elif turretSize == "m":
            txt = "Medium"
        elif turretSize == "l":
            txt = "Large"
        print("SIZE:", txt)
        print("GUNS:", str(self.gun_number))
        print("ROTATION SPEED:", str(self.rot_speed) + "°/s")
        print("RELOAD SPEED:", str(self.reloadTime) + "s")
        print("GUNS ACCURACY:", str(self.gun_acc) + "°")
        print("BASE FIRE CONTROL ERROR:", str(100 * self.base_fc_error) + "%")
        print("FC ERROR REDUCTION RATE:", str(100 * self.fc_e_reduc_rate) + "%")
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
        painter.setBrush(QBrush(QColor("darkGray")))
        painter.setPen(QPen(QColor("black"), self.thickness))
        painter.drawRect(self.rect())
