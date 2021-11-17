# -*- coding: utf-8 -*-

"""
    File name: destroyerConfig.py
    Author: Grégory LARGANGE
    Date created: 17/11/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 17/11/2021
    Python version: 3.8.1

    THIS FILE IS THE DEFAULT CONFIGURATION
    FOR DETROYERS OBJECTS OF SHIP CLASS.
    MODIFICATIONS ARE NOT ADVICED.
"""


naming = {"_type": "DD", "_name": "Simpson", "base_cost": 3000, "cost": 3000}

geometry = {
    "_width": 850,
    "_height": 100,
}

hull = {
    "max_hp": 7500,
    "armor": 100,
    "max_shield": 10000,
    "max_speed": 18,
    "max_accel": 1,
    "turn_rate": 0.25,
    "base_concealement": 0.35,
    "base_detection_range": 12000,
}

weapons = {
    "turrets_size": "s",
    "turrets_pos": [[15, 30], [80, 30], [145, 30], [605, 30], [675, 30]],
    "turrets_list": [],
    "laser_turrets_list": None,
    "laser_turrets_pos": None,
    "guns_range": 10000,
}

techs = {"guns_tech": 0, "fc_tech": 0, "pc_tech": 0, "radar_tech": 0}

refresh = {"refresh_rate": 9, "path_update_rate": 99, "print_point_rate": 74}

crit_components = {
    "BRIDGE": "OK",
    "ENGINE": "OK",
    "RADAR": "OK",
    "SHIELD_GENERATOR": "OK",
    "FIRES": 0,
}

det_and_range = {
    "detected_ships": None,
    "rcom_ships": None,
    "fleet_detected_ships": None,
    "det_r_angles": [-33.34, 0, 33.34],
    "det_r_range": 0,
}

coordinates = {"center": None, "r_centers": None, "heading": 0, "rot_direction": 0}

pathfinding = {
    "trajectory": None,
    "checkpoint": None,
    "sel_checkpoint_id": None,
    "targetPoint": None,
    "cp_tolerance": 500,
    "t_heading": 0,
}

displays = {
    "rangeCirclesDisp": None,
    "lineToDestination": None,
    "lineToTarget": None,
    "selected": None,
}

instant_vars = {
    "hp": 0,
    "shield": 0,
    "concealement": 0,
    "detection_range": 0,
    "speed": 0,
    "accel": 0,
}

iterators = {
    "next_path_update": 99,
    "next_radar_scan": 0,
    "next_target_lock": 0,
    "next_point_print": 0,
}

speed_params = {
    "speed_user_override": None,
    "default_speed": "FAST",
    "speed_options": {"AHEAD_FULL": 0, "FAST": 0, "SLOW": 0, "STOP": 0},
}
