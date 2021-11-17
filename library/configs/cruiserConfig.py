# -*- coding: utf-8 -*-

"""
    File name: cruiserConfig.py
    Author: Grégory LARGANGE
    Date created: 17/11/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 17/11/2021
    Python version: 3.8.1

    THIS FILE IS THE DEFAULT CONFIGURATION
    FOR CRUISERS OBJECTS OF SHIP CLASS.
    MODIFICATIONS ARE NOT ADVICED.
"""


naming = {"_type": "CA", "_name": "Constitution", "base_cost": 4500, "cost": 4500}

geometry = {
    "_width": 950,
    "_height": 175,
}

hull = {
    "max_hp": 10000,
    "armor": 250,
    "max_shield": 10000,
    "max_speed": 12,
    "max_accel": 0.75,
    "turn_rate": 0.2,
    "base_concealement": 0.3,
    "base_detection_range": 8000,
}

weapons = {
    "turrets_size": "m",
    "turrets_pos": [[55, 37], [155, 37], [600, 37], [700, 37]],
    "turrets_list": [],
    "laser_turrets_list": None,
    "laser_turrets_pos": None,
    "guns_range": 14000,
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
