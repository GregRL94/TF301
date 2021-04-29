# -*- coding: utf-8 -*-

"""
    File name: projectileConfig.py
    Author: Grégory LARGANGE
    Date created: 27/04/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 28/04/2021
    Python version: 3.8.1

    THIS FILE CONTAINS DEFAULT CONFIGS
    FOR PROJECTILE OBJECTS.
    MODIFICATIONS ARE NOT ADVICED.
"""


small = {
    "_width": 30,
    "_height": 15,
    "thk": 3,
    "range": 7500,
    "shot_disp": 0.0667,
    "speed_AP": 150,
    "speed_HE": 125,
    "color_AP": ["lightGray", "gray"],
    "color_HE": ["yellow", [255, 165, 0]],
    "dmg_AP": 240,
    "dmg_HE": 360,
    "pen_AP": 150,
    "pen_HE": 50,
    "decc": 0.2,
}

medium = {
    "_width": 50,
    "_height": 25,
    "thk": 5,
    "range": 15000,
    "shot_disp": 0.0834,
    "speed_AP": 150,
    "speed_HE": 125,
    "color_AP": ["lightGray", "gray"],
    "color_HE": ["yellow", [255, 165, 0]],
    "dmg_AP": 480,
    "dmg_HE": 720,
    "pen_AP": 300,
    "pen_HE": 75,
    "decc": 0.2,
}

large = {
    "_width": 80,
    "_height": 40,
    "thk": 10,
    "range": 21000,
    "shot_disp": 0.0952,
    "speed_AP": 150,
    "speed_HE": 125,
    "color_AP": ["lightGray", "gray"],
    "color_HE": ["yellow", [255, 165, 0]],
    "dmg_AP": 800,
    "dmg_HE": 1200,
    "pen_AP": 400,
    "pen_HE": 100,
    "decc": 0.2,
}
