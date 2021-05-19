# -*- coding: utf-8 -*-

"""
    File name: projectileConfig.py
    Author: Grégory LARGANGE
    Date created: 27/04/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 19/05/2021
    Python version: 3.8.1

    THIS FILE CONTAINS DEFAULT CONFIGS
    FOR PROJECTILE OBJECTS.
    MODIFICATIONS ARE NOT ADVICED.
"""


small = {
    "_width": 30,
    "_height": 15,
    "thk": 3,
    "m_range": 7500,
    "accy": 0.0667,
    "v_AP": 150,
    "v_HE": 125,
    "colors_AP": ["lightGray", "gray"],
    "colors_HE": ["yellow", "red"],
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
    "m_range": 15000,
    "accy": 0.0834,
    "v_AP": 150,
    "v_HE": 125,
    "colors_AP": ["lightGray", "gray"],
    "colors_HE": ["yellow", "red"],
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
    "m_range": 21000,
    "accy": 0.0952,
    "v_AP": 150,
    "v_HE": 125,
    "colors_AP": ["lightGray", "gray"],
    "colors_HE": ["yellow", "red"],
    "dmg_AP": 800,
    "dmg_HE": 1200,
    "pen_AP": 400,
    "pen_HE": 100,
    "decc": 0.2,
}
