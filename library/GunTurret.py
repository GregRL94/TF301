# -*- coding: utf-8 -*-

"""
    File name: Gun_Turret.py
    Author: Grégory LARGANGE
    Date created: 12/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 21/07/2020
    Python version: 3.8.1
"""

import math
import random

from os import path

from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from library.Projectile import Projectile
from library.utils.MathsFormulas import Geometrics as geo, Controllers as con
from library.InGameData import TechsData as tech_dat
from library.utils.Config import Config


class GunTurret(QGraphicsRectItem):
    """

    A class handling the creation and behaviour of turrets.

    ...

    Attributes
    ----------
    d_shipCenter : int
        The distance between the turret center and its parent ship center.

    shot_t : string
        The tag defining which shot type to fire.

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
    __init__(clock : MainClock, gameScene : GameScene, parent[None] : Ship)
        The constructor of the class.

    __init_instance__()
        Initialize the variables of a new object of class GunTurret.

    small(clock : MainClock, gameScene : GameScene, parent[None] : Ship)
        Creates a small turret.

    medium(clock : MainClock, gameScene : GameScene, parent[None] : Ship)
        Creates a medium turret.

    large(clock : MainClock, gameScene : GameScene, parent[None] : Ship)
        Creates a large turret.

    fixedUpdate()
        Called every clock signal, this function updates every aspect of the
        turret.
        Nota: The turret position is not taken care of by the turret itself, but
        by its parent.

    setTarget(targetShip : Ship)
        Sets the target of the turret to be the given Ship object.

    computeFiringSolution()
        Calculate the angle at which to rotate the turret to in order to hit the
        target.

    rotateToTAzimut()
        Rotates the turret towards target angle.

    setShot(shot_t : string)
        Selects the type of shot to shoot depending on shot_t.

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

    printInfos()
        Print onfos about the turret.

    paint()
        Instructions to draw the item on the game scene.

    """

    cfg_dict, cfg_txt = Config._file2dict(
        path.join(path.dirname(path.realpath(__file__)), "configs", "turretConfig.py")
    )

    d_shipCenter = 0
    shot_t = "HE"
    azimut = 0

    target = None
    t_id = None
    t_azimut = 0
    t_range = 0
    t_x_1 = t_v_x = 0
    t_y_1 = t_v_y = 0

    def __init__(self, clock, gameScene, parent=None):
        """

        Parameters
        ----------
        clock : MainClock
            The main clock of the game.
        gameScene : GameScene
            The main display of the game.
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

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsRectItem.ItemIsFocusable, False)

        self.clock.clockSignal.connect(self.fixedUpdate)

    def __init_instance__(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Initialize variables for instantiation.

        """
        rect = QRectF(0, 0, self._width, self._height)
        # Sets gun_acc parameters from tech_dat according to parent guns_tech #
        self.gun_acc = round(
            self.gun_disp * tech_dat.gun_tech_acc[self.parentShip.techs["guns_tech"]], 4
        )
        # Sets base_fc_error parameters from tech_dat according to parent fc_tech #
        self.fc_error = self.base_fc_error = tech_dat.fc_tech_e[
            self.parentShip.techs["fc_tech"]
        ]
        # Sets fc_e_reduc_rate parameters from tech_dat according to parent pc_tech #
        self.fc_e_reduc_rate = tech_dat.pc_tech_reduc[self.parentShip.techs["pc_tech"]]
        self.nextShot = self.reload_t
        self.next_fc_correction = self.fc_corr_rate

        self.setRect(rect)

    @classmethod
    def small(cls, clock, gameScene, parent=None):
        """

        Parameters
        ----------
        clock : QTimer
            The main clock of the game.
        gameScene : GameScene
            The main scene of the game.
        parent : QObject
            The parent item of that item.

        Returns
        -------
        s_tur : GunTurret()

        Summary
        -------
        Create a turret using the 'small' configuration setup.

        """
        cfg_s = cls.cfg_dict["small"].copy()
        s_tur = cls(clock, gameScene, parent)
        s_tur.__dict__.update(cfg_s)
        s_tur.__init_instance__()

        return s_tur

    @classmethod
    def medium(cls, clock, gameScene, parent=None):
        """

        Parameters
        ----------
        clock : QTimer
            The main clock of the game.
        gameScene : GameScene
            The main scene of the game.
        parent : QObject
            The parent item of that item.

        Returns
        -------
        m_tur : GunTurret()

        Summary
        -------
        Create a turret using the 'medium' configuration setup.

        """
        cfg_m = cls.cfg_dict["medium"].copy()
        m_tur = cls(clock, gameScene, parent)
        m_tur.__dict__.update(cfg_m)
        m_tur.__init_instance__()

        return m_tur

    @classmethod
    def large(cls, clock, gameScene, parent=None):
        """

        Parameters
        ----------
        clock : QTimer
            The main clock of the game.
        gameScene : GameScene
            The main scene of the game.
        parent : QObject
            The parent item of that item.

        Returns
        -------
        l_tur : GunTurret()

        Summary
        -------
        Create a turret using the 'large' configuration setup.

        """
        cfg_l = cls.cfg_dict["large"].copy()
        l_tur = cls(clock, gameScene, parent)
        l_tur.__dict__.update(cfg_l)
        l_tur.__init_instance__()

        return l_tur

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
            if (self.t_azimut - self.azimut < 1) | (
                (self.t_azimut - self.azimut > 359)
                & (self.t_azimut - self.azimut < 361)
            ):
                if self.nextShot <= 0:
                    self.shoot()
                    self.nextShot = self.reload_t
        else:
            self.t_azimut = self.parentShip.coordinates["heading"]
            self.rotateToTAzimut()

    def setTarget(self, targetShip):
        """

        Parameters
        ----------
        targetShip : Ship
            A Ship class object.

        Returns
        -------
        None.

        Summary
        -------
        Sets the target of the turret if any. Updates the position information
        of the target if any.

        """
        self.target = targetShip
        if self.target:
            # If there was no target before or the target has changed
            if (self.t_id is None) or (targetShip.data(0) != self.t_id):
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
        shellSpeed = (
            tech_dat.speeds_shellType[0]
            if self.shot_t == "AP"
            else tech_dat.speeds_shellType[1]
        )
        shellSpeed *= self.parentShip.refresh[
            "refresh_rate"
        ]  # We accomodate for the fact that the firing soluting is not computed every frame
        estimatedFlightTime = round(self.t_range / shellSpeed, 4)
        estimated_t_speed_x = self.fcREG(self.t_v_x)
        estimated_t_speed_y = self.fcREG(self.t_v_y)
        # See docs for more infos on the maths
        estimatedPos = QPointF(
            self.target.pos().x() + estimated_t_speed_x * estimatedFlightTime,
            self.target.pos().y() + estimated_t_speed_y * estimatedFlightTime,
        )
        estimatedCenter = geo.parallelepiped_Center(
            estimatedPos, self.target.rect().width(), self.target.rect().height()
        )
        self.t_range = int(geo.distance_A_B(self.pos(), estimatedCenter))
        a_h = (estimatedCenter.x() - self.pos().x()) / self.t_range
        # Avoid non definition errors
        if a_h > 1.0:
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

        self.azimut += con.proportional(
            self.t_azimut, self.azimut, self.rot_speed, diff
        )
        self.setTransformOriginPoint(
            QPointF(self.rect().width() / 2, self.rect().height() / 2)
        )
        self.setRotation(self.azimut)

    def setShot(self, shot_type):
        """

        Parameters
        ----------
        shot_type : string
            The type of the shot.

        Returns
        -------
        None.

        Summary
        -------
        Sets the type of shot to be used by the turret.

        """
        self.shot_t = shot_type

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
        tag = self.parentShip.data(1)

        for pos in self.guns_pos:
            a = self.gunDispersion()

            if self.shot_s == "s":
                shot = Projectile.small(
                    self.clock, self.gameScene, tag, self.t_range, a, self.shot_t
                )
            elif self.shot_s == "m":
                shot = Projectile.medium(
                    self.clock, self.gameScene, tag, self.t_range, a, self.shot_t
                )
            elif self.shot_s == "l":
                shot = Projectile.large(
                    self.clock, self.gameScene, tag, self.t_range, a, self.shot_t
                )

            spawnPos = self.computeSpawnPos(pos, az_rad)
            shot.setZValue(4)
            shot.setPos(spawnPos)
            self.gameScene.addItem(shot)
            shot = None

    def printInfos(self):
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
        if self._size == "s":
            txt = "Small"
        elif self._size == "m":
            txt = "Medium"
        elif self._size == "l":
            txt = "Large"
        print("SIZE:", txt)
        print("GUNS:", str(self.n_guns))
        print("ROTATION SPEED:", str(self.rot_speed) + "°/s")
        print("RELOAD SPEED:", str(self.reload_t) + "s")
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
        painter.setPen(QPen(QColor("black"), self.thk))
        painter.drawRect(self.rect())
