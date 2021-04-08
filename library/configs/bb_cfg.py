# -*- coding: utf-8 -*-

'''
    File name: bb_cfg.py
    Author: Grégory LARGANGE
    Date created: 07/04/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 07/04/2021
    Python version: 3.8.1
'''

#-------------- GEOMETRY ---------------#
_width = 1150
_height = 250
#---------------------------------------#

#--------- HULL CHARACTERISTICS --------#
_type = "BB"
max_hp = 10000
armor = 300
max_shield = 10000
max_speed = 9
max_accel = 0.5
turn_rate = 0.13
base_concealement = 0.1
base_detection_range = 5000
#---------------------------------------#

#-------- WEAPONS CHARACTERISTICS ------#
gun_turrets_list = None
laser_turrets_list = None
laser_turrets_pos = None
guns_range = 0
guns_tech = 0
fc_tech = 0
pc_tech = 0
radar_tech = 0
#---------------------------------------#

#-------- DETECTION AND RANGING --------#
detected_ships = None
rcom_ships = None
ships_in_range = None
#---------------------------------------#

#------------ PATHFINDING --------------#
pathUpdateRate = 99
r_centers = None
trajectory = None
checkpoint = None
sel_checkpoint_id = None
targetPoint = None
cp_tolerance = 500
heading = 0
t_heading = 0
rot_direction = 0
#---------------------------------------#

#-------------- DISPLAYS ---------------#
rangeCirclesDisp = None
#---------------------------------------#
