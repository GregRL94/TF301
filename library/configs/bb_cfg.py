# -*- coding: utf-8 -*-

'''
    File name: bb_cfg.py
    Author: Grégory LARGANGE
    Date created: 07/04/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 07/04/2021
    Python version: 3.8.1
'''


naming = {
    "_type" : "BB",
    "_name" : "Monitor"
}

geometry = {
    "_width" : 1150,
    "_height" : 250,
}

hull = {
    "max_hp" : 10000,
    "armor" : 300,
    "max_shield" : 10000,
    "max_speed" : 9,
    "max_accel" : 0.5,
    "turn_rate" : 0.13,
    "base_concealement" : 0.1,
    "base_detection_range" : 5000,
}

weapons = {
    "turrets_list" : None,
    "laser_turrets_list" : None,
    "laser_turrets_pos" : None,
    "guns_range" : 21000
}
