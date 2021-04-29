# -*- coding: utf-8 -*-

"""
    File name: turretConfig.py
    Author: Grégory LARGANGE
    Date created: 27/04/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 27/04/2021
    Python version: 3.8.1

    THIS FILE CONTAINS DEFAULT CONFIGS
    FOR TURRET OBJECTS.
    MODIFICATIONS ARE NOT ADVICED.
"""


small = {
    "_size": "s",
    "_width": 75,
    "_height": 75,
    "thk": 10,  # Thickness for the painter
    "n_guns": 1,  # Number of guns
    "reload_t": 50,  # Reload speed of the guns
    "rot_speed": 3.6,  # Rotation speed
    "gun_disp": 2.8624,  # Base accuracy of a gun
    "shot_s": "s",  # Shot size
    "fc_corr_rate": 150,  # Rate at which the target pos error is reduced
}

medium = {
    "_size": "m",
    "_width": 125,
    "_height": 125,
    "thk": 10,
    "n_guns": 2,
    "reload_t": 75,
    "rot_speed": 2.4,
    "gun_disp": 4.2891,
    "shot_s": "m",
    "fc_corr_rate": 150,
}

large = {
    "_size": "l",
    "_width": 175,
    "_height": 150,
    "thk": 10,
    "n_guns": 3,
    "reload_t": 150,
    "rot_speed": 1.2,
    "gun_disp": 5.7106,
    "shot_s": "l",
    "fc_corr_rate": 150,
}
