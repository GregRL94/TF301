# -*- coding: utf-8 -*-

"""
    File name: game_controller.py
    Author: Grégory LARGANGE
    Date created: 12/11/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 08/12/2021
    Python version: 3.8.1
"""

import math
import random

from PyQt5.QtCore import QPoint, QPointF
from library.configs import battleshipConfig as bb_config, cruiserConfig as ca_config
from library.utils.MathsFormulas import Geometrics as geo, Cinematics as cin


class FleetAI:
    """

    The class implementing the AI that will face the player.

    ...

    Attributes
    ----------
    None.

    Methods
    -------
    __init__()
    on_start()
    fixed_update()
    fleet_center_of_gravity()
    random_destination()
    screen()
    select_lead_ship()
    double_line_formation()
    set_fleet_destination()

    """

    def __init__(
        self,
        game_clock,
        game_scene,
        radio_comms,
        ship_list,
        map_borders,
        # behavior=None,
        # difficulty=None,
    ):
        """

        Parameters
        ----------
        game_clock : MainClock
            The clock of the game.
        game_scene : GameScene
            The scene where the game is displayed.
        ship_list : list
            The list of ships to be used by the AI.
        map_borders: list
            The list of the map borders.
            0->left, 1-> right, 2 -> top, 3 -> bottom

        """
        self.clock = game_clock
        self.game_scene = game_scene
        self.r_coms = radio_comms
        self.map_borders = map_borders

        self.refresh_rate = 99
        self.next_refresh = self.refresh_rate

        self.fleet = []
        self.battleships = []
        self.cruisers = []
        self.destroyers = []
        self.submarines = []
        self.ships_coef = [12, 8, 4, 2]

        self.lead_bb = None
        self.lead_ca = None
        self.screening_angle = 60  # degrees, angle for screening direction. total screening area is the disc arc covered by 2 * screening angle centered on direction

        self.default_ennemy_cog = QPoint(0, self.map_borders[1] // 2)

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
            self.lead_bb = (
                self.battleships[0] if random.random() <= 0.4 else self.battleships[-1]
            )
        if len(self.cruisers) > 0:
            self.lead_ca = (
                self.cruisers[0] if random.random() <= 0.4 else self.cruisers[-1]
            )

        self.on_start()
        self.clock.clockSignal.connect(self.fixed_update)

    def on_start(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Called once at the very start of a game, gives the very first set of instructions
        to the ships in the fleet.

        """
        self.set_fleet_destination()
        self.double_line_formation()
        self.screen(
            self.fleet_center_of_gravity(self.fleet), None,
        )

    def fixed_update(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Called every clock step, used to update and give instructions to ships in fleet.

        """
        if self.next_refresh <= 0:
            fleet_cog = self.fleet_center_of_gravity(self.fleet)
            e_fleet_cog = self.fleet_center_of_gravity(self.r_coms.ennemyDetectedShips)
            self.set_fleet_destination(e_fleet_cog)
            self.screen(fleet_cog, e_fleet_cog)
            self.next_refresh = self.refresh_rate
        else:
            self.next_refresh -= 1

    def fleet_center_of_gravity(self, fleet: list):
        """

        Parameters
        ----------
        fleet : list
            A list of ships.

        Returns
        -------
        QPoint
            The computed enter of gravity of fleet.

        Summary
        -------
        Computes the center of gravity of fleet, according to the coef of
        every ship type.

        """
        coef = None
        ship_momentums_x = 0
        ship_momentums_y = 0
        total_mass = 0

        for ship in fleet:
            if ship.naming["_type"] == "BB":
                coef = self.ships_coef[0]
                total_mass += coef
            elif ship.naming["_type"] == "CA":
                coef = self.ships_coef[1]
                total_mass += coef
            elif ship.naming["_type"] == "DD":
                coef = self.ships_coef[2]
                total_mass += coef

            ship_momentums_x += ship.pos().x() * coef
            ship_momentums_y += ship.pos().y() * coef

        try:
            cog_x = int(ship_momentums_x / total_mass)
            cog_y = int(ship_momentums_y / total_mass)
        except ZeroDivisionError:
            return None

        self.game_scene.printPoint(QPointF(cog_x, cog_y), 1000, "black", True)
        return QPoint(cog_x, cog_y)

    def random_destination(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Generates a random point within the playable area.

        """
        s_point = QPoint(
            random.randint(self.map_borders[0], self.map_borders[1] // 2),
            random.randint(self.map_borders[2], self.map_borders[3] // 2),
        )

        while not self.game_scene.isFreeSpace(s_point):
            s_point = QPoint(
                random.randint(self.map_borders[0], self.map_borders[1] // 2),
                random.randint(self.map_borders[2], self.map_borders[3] // 2),
            )

        return s_point

    def screen(self, ego_cog: QPoint, other_cog: QPoint):
        """

        Parameters
        ----------
        ego_cog: QPoint
            The center of gravity of the ai fleet.
        other_cog: QPoint
            The center of gravity of the player's fleet.

        Returns
        -------
        None.

        Summary
        -------
        If the ai's fleet have any destroyers, place them in the space between
        ego_cog and other_cog so that they can discover the largest area possible.

        """
        if len(self.destroyers) == 0:
            return
        else:
            ennemy_cog = other_cog if other_cog else self.default_ennemy_cog
            screen_dist = bb_config.weapons["guns_range"]
            screen_dir = geo.angle(ego_cog, ennemy_cog)
            step = int(self.screening_angle / (len(self.destroyers) // 2))
            screening_points = []

            if len(self.destroyers) % 2 != 0:
                point = cin.movementBy(ego_cog, screen_dist, screen_dir)
                point.setX(
                    max(min(point.x(), self.map_borders[1]), self.map_borders[0])
                )
                point.setY(
                    max(min(point.y(), self.map_borders[3]), self.map_borders[2])
                )
                screening_points.append(point)

            for angle in range(step // 2, self.screening_angle, step):
                point = cin.movementBy(
                    ego_cog, screen_dist, screen_dir + math.radians(angle)
                )
                point.setX(
                    max(min(point.x(), self.map_borders[1]), self.map_borders[0])
                )
                point.setY(
                    max(min(point.y(), self.map_borders[3]), self.map_borders[2])
                )
                screening_points.append(point)

                point_2 = cin.movementBy(
                    ego_cog, screen_dist, screen_dir - math.radians(angle)
                )
                point_2.setX(
                    max(min(point_2.x(), self.map_borders[1]), self.map_borders[0])
                )
                point_2.setY(
                    max(min(point_2.y(), self.map_borders[3]), self.map_borders[2])
                )
                screening_points.append(point_2)

        screening_points = sorted(
            screening_points, key=lambda point: point.y(), reverse=True
        )
        destroyers = sorted(self.destroyers, key=lambda point: point.y(), reverse=True)
        for point in screening_points:
            self.game_scene.printPoint(point, 1000, "red", True)

        for i, destroyer in enumerate(destroyers):
            if self.game_scene.isFreeSpace(screening_points[i]):
                destroyer.updatePath(screening_points[i])
            else:
                destroyer.updatePath(
                    self.game_scene.alternative_point(screening_points[i])
                )

    def select_lead_ship(self):
        """
        TODO
        """

    def double_line_formation(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Organize the fleet in a double line formation, one line made of cruisers and the
        other of battleships. These lines lines follow their respective lead ships.

        """
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

    def set_fleet_destination(self, other_cog: QPoint = None):
        """

        Parameters
        ----------
        other_cog : QPoint = None
            the player's fleet center of gravity

        Returns
        -------
        None.

        Summary
        -------
        Compute destination point for the fleet according to
        the player's fleet center of gravity

        """
        ennemy_cog = other_cog if other_cog else self.default_ennemy_cog

        if self.lead_bb:
            bb_pos = self.lead_bb.pos()
            dist = geo.distance_A_B(bb_pos, ennemy_cog)
            t_range_bb = int(0.8 * bb_config.weapons["guns_range"])
            dist_to_move = int(dist - t_range_bb)
            t_dir_bb = geo.angle(bb_pos, ennemy_cog)
            t_point_bb = cin.movementBy(bb_pos, dist_to_move, t_dir_bb)
            self.lead_bb.updatePath(t_point_bb)

        if self.lead_ca:
            ca_pos = self.lead_ca.pos()
            dist = geo.distance_A_B(ca_pos, ennemy_cog)
            t_range_ca = int(0.8 * ca_config.weapons["guns_range"])
            dist_to_move = int(dist - t_range_ca)
            t_dir_ca = geo.angle(ca_pos, ennemy_cog)
            t_point_ca = cin.movementBy(ca_pos, dist_to_move, t_dir_ca)
            self.lead_ca.updatePath(t_point_ca)
