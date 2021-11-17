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
from library.configs import battleshipConfig as bb_config, destroyerConfig as dd_config
from library.utils.MathsFormulas import Geometrics as geo, Cinematics as cin


class FleetAI:
    def __init__(
        self,
        game_clock,
        game_scene,
        ship_list,
        map_size,
        map_extension,
        behavior=None,
        difficulty=None,
    ):
        self.clock = game_clock
        self.game_scene = game_scene
        self.map_size = map_size
        self.map_e = map_extension

        self.screen_rate = 199
        self.refresh_rate = 49

        self.fleet = []
        self.battleships = []
        self.cruisers = []
        self.destroyers = []
        self.submarines = []
        self.ships_coef = [12, 8, 4, 2]

        self.lead_bb = None
        self.lead_ca = None
        self.c_fleet_destination = None
        self.screening_angle = 60  # degrees, angle from creening direction. total screening area is the disc arc covered by 2 * screening angle centered on direction
        self.c_screening_dir = None

        self.detected_ennemy_ships = []
        self.ennemy_cog = QPointF(0, map_size / 2)

        for ship in ship_list:
            self.fleet.append(ship)
            if ship.naming["_type"] == "BB":
                self.battleships.append(ship)
            elif ship.naming["_type"] == "CA":
                self.cruisers.append(ship)
            elif ship.naming["_type"] == "DD":
                self.destroyers.append(ship)
            else:
                self.submarines.append(ship)

        if len(self.battleships) > 0:
            _rand = random.random()
            self.lead_bb = self.battleships[0] if _rand <= 0.4 else self.battleships[-1]
            # self.lead_ca = self.cruisers[0] if _rand <= 0.4 else self.cruisers[-1]

        self.on_start()

    def on_start(self):
        self.screen_direction()
        self.set_fleet_destination(self.random_first_heading())
        self.double_line_formation()
        self.screen()

    def fixed_update(self):
        pass

    def fleet_center_of_gravity(self):
        ship_momentums_x = 0
        ship_momentums_y = 0

        total_mass = (
            max(len(self.battleships) - 1, 0) * self.ships_coef[0]
            + max(len(self.cruisers) - 1, 0) * self.ships_coef[1]
            + max(len(self.destroyers) - 1, 0) * self.ships_coef[2]
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
        for destroyer in self.destroyers:
            momentum_x = destroyer.pos().x() * self.ships_coef[2]
            momentum_y = destroyer.pos().y() * self.ships_coef[2]
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

    def random_first_heading(self):
        s_point = QPointF(
            random.randint(0, self.map_size // 2), random.randint(0, self.map_size // 2)
        )

        while not self.game_scene.isFreeSpace(s_point):
            s_point = QPointF(
                random.randint(0, self.map_size // 2),
                random.randint(0, self.map_size // 2),
            )

        s_point.setX(min(max(s_point.x(), self.map_e), self.map_size))
        s_point.setY(min(max(s_point.y(), self.map_e), self.map_size))
        return s_point

    def select_lead_ship(self):
        pass

    def screen_direction(self):
        self.c_screening_dir = geo.angle(
            self.fleet_center_of_gravity(), self.ennemy_cog
        )

    def screen(self):
        cog = self.fleet_center_of_gravity()

        if len(self.destroyers) == 0:
            return
        else:
            screening_points = []
            screen_dist = (
                bb_config.weapons["guns_range"] + dd_config.hull["base_detection_range"]
            )
            step = int(self.screening_angle / (len(self.destroyers) // 2))
            if len(self.destroyers) % 2 != 0:
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
        destroyers = sorted(self.destroyers, key=lambda point: point.y(), reverse=True)
        for point in screening_points:
            self.game_scene.printPoint(point, 1000, "black", True)
        for i, destroyer in enumerate(destroyers):
            if self.game_scene.isFreeSpace(screening_points[i]):
                destroyer.updatePath(screening_points[i])
            else:
                destroyer.updatePath(
                    self.game_scene.alternative_point(screening_points[i])
                )

    def double_line_formation(self):
        if self.lead_bb:
            dist_to_lead = {}
            for ship in self.battleships:
                if ship == self.lead_bb:
                    continue
                else:
                    dist_to_lead[ship] = geo.distance_A_B(
                        ship.pos(), self.lead_bb.pos()
                    )
            sorted_dist_to_lead = {
                k: v for k, v in sorted(dist_to_lead.items(), key=lambda item: item[1])
            }
            sorted_ships_by_dist_to_lead = list(sorted_dist_to_lead.keys())
            for i, ship in enumerate(sorted_ships_by_dist_to_lead):
                if i == 0:
                    ship.follow(self.lead_bb)
                else:
                    ship.follow(sorted_ships_by_dist_to_lead[i - 1])

        if self.lead_ca:
            dist_to_lead = {}
            for ship in self.cruisers:
                if ship == self.lead_ca:
                    continue
                else:
                    dist_to_lead[ship] = geo.distance_A_B(
                        ship.pos(), self.lead_ca.pos()
                    )
            sorted_dist_to_lead = {
                k: v for k, v in sorted(dist_to_lead.items(), key=lambda item: item[1])
            }
            sorted_ships_by_dist_to_lead = list(sorted_dist_to_lead.keys())
            for i, ship in enumerate(sorted_ships_by_dist_to_lead):
                if i == 0:
                    ship.follow(self.lead_ca)
                else:
                    ship.follow(sorted_ships_by_dist_to_lead[i - 1])

    def set_fleet_destination(self, point: QPointF = None):
        if self.lead_bb:
            self.lead_bb.updatePath(point)
        if self.lead_ca:
            self.lead_ca.updatePath(point)
