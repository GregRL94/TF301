# -*- coding: utf-8 -*-

"""
    File name: game_controller.py
    Author: Grégory LARGANGE
    Date created: 12/11/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 12/11/2021
    Python version: 3.8.1
"""

import random

from PyQt5.QtCore import QPointF
from library.configs import battleshipConfig as bb_config


class FleetAI:
    def __init__(self, ship_list, behavior, difficulty):
        self.fleet = []
        self.battleships = []
        self.cruisers = []
        self.frigates = []
        self.submarines = []
        self.ships_coef = [12, 8, 4, 2]

        self.detected_ennemy_ships = []
        self.last_known_ennemy_position = None

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

    def fleet_center_of_mass(self):
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

        center_of_mass_x = int(ship_momentums_x / total_mass)
        center_of_mass_y = int(ship_momentums_y / total_mass)

        return QPointF(center_of_mass_x, center_of_mass_y)

    def random_starting_direction(self):
        _sin = (
            0.7  # the sinus value of a 45° angle. This value has been choosen at random
        )
        v_direction = -1 if random.random() <= 0.5 else 1
        sin = 0 if random.random() <= 0.3 else 0.7

        return sin * v_direction

    def screen(self):
        if len(self.frigates) == 0:
            return
        else:
            screening_direction = -1
            screening_angle = 120  # degrees
            effective_screen_dist = bb_config.weapons[
                "guns_range"
            ]  # + ff_config.hull["base_detection_range"]
