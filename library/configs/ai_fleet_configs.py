# -*- coding: utf-8 -*-

"""
    File name: ai_fleet_configs.py
    Author: Grégory LARGANGE
    Date created: 13/10/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 13/10/2021
    Python version: 3.8.1

    THIS FILE CONTAINS DEFAULT SETTINGS
    FOR AI FLEET GENERATION. MODIFICATIONS
    ARE NOT ADVICED.
"""

## GENERAL EXPLANATION
# This config file determines which general tactic the ai will follow, and place priorities on ships to build and tech
# levels.
# For example, the tactic juggernaut_big_guns relies on numbers and battleships. Hence focus will be placed on low tech
# battleships. The corresponding pair in the dictionary should be read as follows:
# "juggernaut_big_guns": [[3, 0, 1, 0], [0, 0, 0]]
# The 3 at index 0 indicates that Battleships have highest priority when ai buy ships.
# The 1 at index 2 indicates that ai should buy a few frigates.
# The 0s indicates that ai should not consider buying the concerned ships.
# The second list indicates the importance of getting technologies level.
# The higher the value the harder the ai will try to reach the highest possible technology level.

doctrines = {"test": [[3, 0, 0, 0], [2, 2, 2]], "test2": [[2, 1, 1, 0], [0, 0, 0]]}
