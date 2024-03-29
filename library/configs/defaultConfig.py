# -*- coding: utf-8 -*-

'''
    File name: default_cfg.py
    Author: Grégory LARGANGE
    Date created: 09/04/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 12/04/2021
    Python version: 3.8.1

    THIS FILE IS THE DEFAULT CONFIGURATION
    FOR ANY OBJECTS OF SHIP CLASS. MODIFICATIONS
    ARE NOT ADVICED.
'''


naming = {
    "_type" : "",
    "_name" : ""
}

geometry = {
    "_width" : 0,
    "_height" : 0,
}

hull = {
    "max_hp" : 0,
    "armor" : 0,
    "max_shield" : 0,
    "max_speed" : 0,
    "max_accel" : 0,
    "turn_rate" : 0,
    "base_concealement" : 0,
    "base_detection_range" : 0,
}

weapons = {
    "turrets_list" : None,
    "laser_turrets_list" : None,
    "guns_range" : 0
}

techs = {
    "guns_tech" : 0,
    "fc_tech" : 0,
    "pc_tech" : 0,
    "radar_tech" : 0
}

refresh = {
    "refresh_rate" : 9,
    "path_update_rate" : 99,
    "print_point_rate" : 74
}

crit_components = {
    "bridge_state" : "OK",
    "engine_state" : "OK",
    "radar_state" : "OK",
    "shield_generator_state" : "OK"
}

det_and_range = {
    "detected_ships" : None,
    "rcom_ships" : None,
    "ships_in_range" : None,
}

coordinates = {
    "center" : None,
    "r_centers" : None,
    "heading" : 0,
    "rot_direction" : 0
}

pathfinding = {
    "trajectory" : None,
    "checkpoint" : None,
    "sel_checkpoint_id" : None,
    "targetPoint" : None,
    "cp_tolerance" : 500,
    "t_heading" : 0,
}

displays = {
    "rangeCirclesDisp" : None
}

instant_vars = {
    "hp" : 0,
    "shield" : 0,
    "concealement" : 0,
    "detection_range" : 0,
    "speed" : 0,
    "accel" : 0
}

iterators = {
    "next_path_update" : 99,
    "next_radar_scan" : 0,
    "next_target_lock" : 0,
    "next_point_print" : 0,
}

speed_params = {
    "speed_user_override" : None,
    "default_speed" : "FAST",
    "speed_options" : {
        "AHEAD_FULL": 0,
        "FAST": 0,
        "SLOW": 0,
        "STOP": 0
    }
}
