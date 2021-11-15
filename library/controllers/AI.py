# -*- coding: utf-8 -*-

"""
    File name: game_controller.py
    Author: Grégory LARGANGE
    Date created: 12/11/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 12/11/2021
    Python version: 3.8.1
"""

import math
import random

from PyQt5.QtCore import QPointF
from library.configs import battleshipConfig as bb_config
from library.utils.MathsFormulas import Geometrics as geo, Cinematics as cin


class FleetAI:
    def __init__(
        self, game_clock, game_scene, ship_list, behavior, difficulty, map_height
    ):
        self.clock = game_clock
        self.game_scene = game_scene
        self.screen_rate = 199
        self.refresh_rate = 49

        self.fleet = []
        self.battleships = []
        self.cruisers = []
        self.frigates = []
        self.submarines = []
        self.ships_coef = [12, 8, 4, 2]

        self.c_fleet_heading = None
        self.c_fleet_cog = None
        self.screening_angle = 60  # degrees, angle from creening direction. total screening area is the disc arc covered by 2 * screening angle centered on direction
        self.c_screening_dir = None

        self.detected_ennemy_ships = []
        self.ennemy_cog = QPointF(0, map_height / 2)

        for ship in ship_list:
            self.fleet.append(ship)
            if ship.naming["_type"] == "BB":
                self.battleships.append(ship)
            elif ship.naming["_type"] == "CA":
                self.cruisers.append(ship)
            elif ship.naming["_type"] == "FF":
                self.frigates.append(ship)
            else:
                self.submarines.append(ship)

    def fleet_center_of_gravity(self):
        ship_momentums_x = 0
        ship_momentums_y = 0

        total_mass = (
            max(len(self.battleships) - 1, 0) * self.ships_coef[0]
            + max(len(self.cruisers) - 1, 0) * self.ships_coef[1]
            + max(len(self.frigates) - 1, 0) * self.ships_coef[2]
        )
        # max(len(self.submarines) - 1, 0) * self.ships_coef[3]

        for battleship in self.battleships:
            momentum_x = battleship.pos().x() * self.ships_coef[0]
            momentum_y = battleship.pos().y() * self.ships_coef[0]
            ship_momentums_x += momentum_x
            ship_momentums_y += momentum_y
        for cruiser in self.cruisers:
            momentum_x = cruiser.pos().x() * self.ships_coef[1]
            momentum_y = cruiser.pos().y() * self.ships_coef[1]
            ship_momentums_x += momentum_x
            ship_momentums_y += momentum_y
        for frigate in self.frigates:
            momentum_x = frigate.pos().x() * self.ships_coef[2]
            momentum_y = frigate.pos().y() * self.ships_coef[2]
            ship_momentums_x += momentum_x
            ship_momentums_y += momentum_y
        # for submarine in self.submarines:
        #     momentum_x = submarine.pos().x() * self.ships_coef[3]
        #     momentum_y = submarine.pos().y() * self.ships_coef[3]
        #     ship_momentums_x += momentum_x
        #     ship_momentums_y += momentum_y

        cog_x = int(ship_momentums_x / total_mass)
        cog_y = int(ship_momentums_y / total_mass)

        return QPointF(cog_x, cog_y)

    def random_starting_direction(self):
        _sin = (
            0.7  # the sinus value of a 45° angle. This value has been choosen at random
        )
        v_direction = -1 if random.random() <= 0.5 else 1
        sin = 0 if random.random() <= 0.3 else 0.7

        return sin * v_direction

    def screen_direction(self):
        self.c_screening_dir = geo.angle(
            self.fleet_center_of_gravity(), self.ennemy_cog
        )

    def screen(self):
        cog = self.fleet_center_of_gravity()

        if len(self.frigates) == 0:
            return
        else:
            screening_points = []
            screen_dist = bb_config.weapons[
                "guns_range"
            ]  # + ff_config.hull["base_detection_range"]
            step = int(self.screening_angle / (len(self.frigates) // 2))
            if len(self.frigates) % 2 == 0:
                screening_points.append(None)
            else:
                screening_points.append(
                    cin.movementBy(cog, screen_dist, self.c_screening_dir)
                )

            for angle in range(step // 2, self.screening_angle, step):
                screening_points.append(
                    cin.movementBy(
                        cog, screen_dist, self.c_screening_dir + math.radians(angle),
                    )
                )
                screening_points.append(
                    cin.movementBy(
                        cog, screen_dist, self.c_screening_dir - math.radians(angle),
                    )
                )

        screening_points = sorted(
            screening_points, key=lambda point: point.y(), reverse=True
        )
        frigates = sorted(self.frigates, key=lambda point: point.y(), reverse=True)

        for i, frigate in enumerate(frigates):
            if not self.game_scene.isFreeSpace(screening_points[i], True):
                for i in range(1000, 4000, 1000):
                    print("New set of points, at", i, " distance from original point")
                    point_matrix = [
                        QPointF(
                            screening_points[i].x() + i, screening_points[i].y() + i
                        ),
                        QPointF(
                            screening_points[i].x() - i, screening_points[i].y() + i
                        ),
                        QPointF(
                            screening_points[i].x() + i, screening_points[i].y() - i
                        ),
                        QPointF(
                            screening_points[i].x() - i, screening_points[i].y() - i
                        ),
                    ]
                    for point in point_matrix:
                        # If a point in the new set is NOT within an obstacle, returns it
                        if self.game_scene.isFreeSpace(point, True):
                            frigate.updatePath(point)
