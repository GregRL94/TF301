# -*- coding: utf-8 -*-

"""
    File name: game_controller.py
    Author: Grégory LARGANGE
    Date created: 13/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 13/10/2021
    Python version: 3.8.1
"""

import random
import copy

from os import path

from library.configs import ai_fleet_configs
from library.configs import battleshipConfig
from library.InGameData import TechsData as tech_dat
from library.utils.Config import Config


class GameController:
    def __init__(self, parent):
        self.tf301_ref = parent
        self.all_doctrines = ai_fleet_configs.doctrines
        bb_cfg = path.join(
            path.dirname(path.realpath(__file__)), "../configs/battleshipConfig.py"
        )
        self.bb_dict, _ = Config._file2dict(bb_cfg)

        # ca_cfg = path.join(
        #     path.dirname(path.realpath(__file__)), "../configs/cruiserConfig.py"
        # )
        # self.ca_dict, ca_txt = Config._file2dict(ca_cfg)

        # ff_cfg = path.join(
        #     path.dirname(path.realpath(__file__)), "../configs/frigateConfig.py"
        # )
        # self.ff_dict, ff_txt = Config._file2dict(ff_cfg)

        # pt_cfg = path.join(
        #     path.dirname(path.realpath(__file__)), "../configs/corvetteConfig.py"
        # )
        # self.pt_dict, pt_txt = Config._file2dict(pt_cfg)

        tur_cfg = path.join(
            path.dirname(path.realpath(__file__)), "../configs/turretConfig.py"
        )
        self.tur_dict, _ = Config._file2dict(tur_cfg)

    def generate_ai_fleet(self, funds):
        doctrine = self.choose_random_doctrine()
        doctrine_ship_prios = self.all_doctrines[doctrine][0]
        doctrine_tech_prios = self.all_doctrines[doctrine][1]
        target_single_ship_cost = [
            battleshipConfig.naming["base_cost"],
            4000,
            2500,
            2000,
        ]
        _sum = 0
        ratios = []
        funds_per_ship_type = []
        ships_per_type = []
        funds_left = 0
        buyable_techs_per_level = []
        all_ships = []

        for prio in doctrine_ship_prios:
            _sum += prio
        for prio in doctrine_ship_prios:
            ratios.append(round(prio / _sum, 2))
        for ratio in ratios:
            funds_per_ship_type.append(int(ratio * funds))
        for i, fund in enumerate(funds_per_ship_type):
            ships_per_type.append(fund // target_single_ship_cost[i])
            funds_left += fund % target_single_ship_cost[i]
        for tech_cost in tech_dat.cost_per_tech:
            buyable_techs_per_level.append(funds_left // tech_cost)
        for i, n_ships in enumerate(ships_per_type):
            for _ in range(n_ships):
                if i == 0:
                    all_ships.append(copy.deepcopy(self.bb_dict))
                # elif i == 1:
                #     all_ships.append(copy.deepcopy(self.ca_dict))
                # elif i == 2:
                #     all_ships.append(copy.deepcopy(self.ff_dict))
                # else:
                #     all_ships.append(copy.deepcopy(self.pt_dict))

        j = 0
        for i in range(buyable_techs_per_level[0]):
            if j > len(all_ships) - 1:
                j = 0
            if all_ships[j]["techs"]["guns_tech"] == 0:
                all_ships[j]["techs"]["guns_tech"] = 1
            elif all_ships[j]["techs"]["radar_tech"] == 0:
                all_ships[j]["techs"]["radar_tech"] = 1
            elif all_ships[j]["techs"]["fc_tech"] == 0:
                all_ships[j]["techs"]["fc_tech"] = 1
            j += 1

        return all_ships

    def choose_random_doctrine(self):
        all_doct_list = list(self.all_doctrines.keys())
        _range = len(all_doct_list)
        rand_index = random.randint(0, _range - 1)
        return all_doct_list[rand_index]
        # return "test"
