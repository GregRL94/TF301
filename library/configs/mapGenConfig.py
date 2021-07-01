# -*- coding: utf-8 -*-

"""
    File name: mapGenConfig.py
    Author: Grégory LARGANGE
    Date created: 25/06/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 28/06/2021
    Python version: 3.8.1

    THIS FILE CONTAINS PARAMETERS CONFIGURATION
    FOR THE MAP GENERATOR. MODIFICATIONS AT THE
    DISCRETION OF THE USER.
"""


size = {"Small": 20000, "Medium": 40000, "Large": 60000}

obstruction = {"Open": 0.0, "Light": 0.05, "Medium": 0.1, "Heavy": 0.2}

funds = {"Small": 25000, "Standard": 50000, "Large": 75000}

mapResolution = 500

obstacles = [
    2,
    10,
    2,
    10,
    4,
]  # min obstacles width, max obstacles width, min obstacles height, max obstacles height, min distance between 2 obstacles

mapExtension = 5000
