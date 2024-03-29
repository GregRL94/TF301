# -*- coding: utf-8 -*-

"""
    File name: BattleSetup.py
    Author: Grégory LARGANGE
    Date created: 10/06/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 17/11/2021
    Python version: 3.8.1
"""


import copy

from os import path
from PyQt5 import QtCore, QtGui, QtWidgets

from library.InGameData import TechsData as tech_dat
from library.utils.Config import Config
from library.utils.Imports import Imports
from library.displays import InteractiveList
from . import dialogsUtils


class BattleSetup:
    """

    A class to handle the creation of a new game.

    ...

    Methods
    -------
    __init__()
        Constructor of the class.

    createFleetUI()
        Displays fleet creator window.

    battleSetupUI()
        Displays battle setup window.

    setEnableRadioButtons(state: bool)
        Enables or disables radio buttons.

    shipButtonClicked(_type: str)
        Adds a ship of _type.

    updateShipCreatorUI()
        Updates the ship stats displays.

    resetShipStats():
        Reset current ship stats.

    updateShipStats():
        Update current ship stats.

    update ship cost(baseCost: int, techLevelsList: list)
        Calculate current ship cost according to techs in techLevelsList.

    updateFleetCost()
        Calculate fleet cost.

    setStatsFromList(_shipKey : int)
        Updates current ship stats and displays according to _shipKey
        returned by the list.

    resetButtonClicked()
        Resets curent ship stats.

    addShip()
        Adds a ship.

    removeShips(shipKeysList : list)
        Removes the ship(s) located at each _shipKey of shipKeysList.

    clearFleet()
        Removes all ships.

    setEnabledOtherWidget(comboBox : QtWidgets.QComboBox)
        Enables or disables some widgets depending on comboBox current text.

    resetMapConfig()
        Resets the current map configuration to its default values.

    updateMapConfig()
        Sets the values of the current map configuration.

    createFleetAccept(dialog : QtWidgets.QDialog)
        Defines the behaviour of the fleet creator window when accept button is clicked.

    battleSetupAccept(dialog : QtWidgets.QDialog)
        Defines the behaviour of the battle setup window when accept button is clicked.

    """

    def __init__(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Constructor of the class.
        Load default configs for all ship types and map generator.

        """
        bb_cfg = path.join(
            path.dirname(path.realpath(__file__)), "../configs/battleshipConfig.py"
        )
        self.bb_dict, _ = Config._file2dict(bb_cfg)

        ca_cfg = path.join(
            path.dirname(path.realpath(__file__)), "../configs/cruiserConfig.py"
        )
        self.ca_dict, _ = Config._file2dict(ca_cfg)

        dd_cfg = path.join(
            path.dirname(path.realpath(__file__)), "../configs/destroyerConfig.py"
        )
        self.dd_dict, _ = Config._file2dict(dd_cfg)

        # pt_cfg = path.join(
        #     path.dirname(path.realpath(__file__)), "../configs/corvetteConfig.py"
        # )
        # self.pt_dict, pt_txt = Config._file2dict(pt_cfg)

        tur_cfg = path.join(
            path.dirname(path.realpath(__file__)), "../configs/turretConfig.py"
        )
        self.tur_dict, _ = Config._file2dict(tur_cfg)

        map_cfg = path.join(
            path.dirname(path.realpath(__file__)), "../configs/mapGenConfig.py"
        )
        self.map_dict, _ = Config._file2dict(map_cfg)

        self.currentMapConfig = {}
        self.currentShip = {}
        self.currentTurDict = {}
        self.allShips = {}
        self.radioButtonsEnabled = False
        self.shipCounter = 0
        self.currentShipKey = 0
        self.fleetCost = 0
        self.resetMapConfig()

    def createFleetUi(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Generates fleet creator UI, binds buttons and actions to function.

        """
        fleet_setup = QtWidgets.QDialog()
        fleet_setup.setObjectName("fleet_setup")
        fleet_setup.resize(812, 660)
        fleet_setup.setMinimumSize(QtCore.QSize(812, 660))
        fleet_setup.setMaximumSize(QtCore.QSize(812, 660))
        fleet_setup.setWindowTitle("Fleet Setup")
        verticalLayoutWidget = QtWidgets.QWidget(fleet_setup)
        verticalLayoutWidget.setGeometry(QtCore.QRect(470, 10, 331, 601))
        verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        fleet_lyt = QtWidgets.QVBoxLayout(verticalLayoutWidget)
        fleet_lyt.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        fleet_lyt.setContentsMargins(0, 0, 0, 0)
        fleet_lyt.setObjectName("fleet_lyt")

        fleet_lbl = QtWidgets.QLabel(verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        fleet_lbl.setFont(font)
        fleet_lbl.setAlignment(QtCore.Qt.AlignCenter)
        fleet_lbl.setObjectName("fleet_lbl")
        fleet_lbl.setText("FLEET")
        fleet_lyt.addWidget(fleet_lbl)

        horizontalLayout_7 = QtWidgets.QHBoxLayout()
        horizontalLayout_7.setObjectName("horizontalLayout_7")

        ships_in_fleet_lbl = QtWidgets.QLabel(verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        ships_in_fleet_lbl.setFont(font)
        ships_in_fleet_lbl.setObjectName("ships_in_fleet_lbl")
        ships_in_fleet_lbl.setText("SHIPS IN FLEET")
        horizontalLayout_7.addWidget(ships_in_fleet_lbl)

        self.cur_fleet_cost_lbl = QtWidgets.QLabel(verticalLayoutWidget)
        self.cur_fleet_cost_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.cur_fleet_cost_lbl.setObjectName("cur_fleet_cost_lbl")
        self.cur_fleet_cost_lbl.setText(
            str(self.fleetCost) + "/" + str(self.currentMapConfig["funds"])
        )
        horizontalLayout_7.addWidget(self.cur_fleet_cost_lbl)

        fleet_lyt.addLayout(horizontalLayout_7)
        self.listView = InteractiveList.InteractiveListView(False, verticalLayoutWidget)
        self.listView.setObjectName("listView")
        self.listView.attachedObject = self
        self.listView.isForBattleSetup = True
        fleet_lyt.addWidget(self.listView)
        del_ship_lyt = QtWidgets.QHBoxLayout()
        del_ship_lyt.setObjectName("del_ship_lyt")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        del_ship_lyt.addItem(spacerItem)

        del_ship_but = QtWidgets.QPushButton(verticalLayoutWidget)
        del_ship_but.setObjectName("del_ship_but")
        del_ship_but.setText("Delete")
        del_ship_lyt.addWidget(del_ship_but)

        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        del_ship_lyt.addItem(spacerItem1)
        fleet_lyt.addLayout(del_ship_lyt)
        horizontalLayoutWidget_2 = QtWidgets.QWidget(fleet_setup)
        horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 630, 791, 25))
        horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        main_choices_lyt = QtWidgets.QHBoxLayout(horizontalLayoutWidget_2)
        main_choices_lyt.setContentsMargins(0, 0, 0, 0)
        main_choices_lyt.setObjectName("main_choices_lyt")
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        main_choices_lyt.addItem(spacerItem2)

        clear_fleet_but = QtWidgets.QPushButton(horizontalLayoutWidget_2)
        clear_fleet_but.setObjectName("clear_fleet_but")
        clear_fleet_but.setText("Reset Fleet")
        main_choices_lyt.addWidget(clear_fleet_but)

        load_fleet_but = QtWidgets.QPushButton(horizontalLayoutWidget_2)
        load_fleet_but.setObjectName("load_fleet_but")
        load_fleet_but.setText("Load Fleet")
        main_choices_lyt.addWidget(load_fleet_but)

        save_fleet_but = QtWidgets.QPushButton(horizontalLayoutWidget_2)
        save_fleet_but.setObjectName("save_fleet_but")
        save_fleet_but.setText("Save Fleet")
        main_choices_lyt.addWidget(save_fleet_but)

        battle_but = QtWidgets.QPushButton(horizontalLayoutWidget_2)
        battle_but.setObjectName("battle_but")
        battle_but.setText("BATTLLE !")
        main_choices_lyt.addWidget(battle_but)

        verticalLayoutWidget_2 = QtWidgets.QWidget(fleet_setup)
        verticalLayoutWidget_2.setGeometry(QtCore.QRect(9, 9, 434, 601))
        verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        ship_creator_lyt = QtWidgets.QVBoxLayout(verticalLayoutWidget_2)
        ship_creator_lyt.setContentsMargins(0, 0, 0, 0)
        ship_creator_lyt.setObjectName("ship_creator_lyt")

        ship_creator_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        ship_creator_lbl.setFont(font)
        ship_creator_lbl.setAlignment(QtCore.Qt.AlignCenter)
        ship_creator_lbl.setObjectName("ship_creator_lbl")
        ship_creator_lbl.setText("SHIP CREATOR")
        ship_creator_lyt.addWidget(ship_creator_lbl)

        type_select_lyt = QtWidgets.QVBoxLayout()
        type_select_lyt.setObjectName("type_select_lyt")

        type_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        type_lbl.setFont(font)
        type_lbl.setObjectName("type_lbl")
        type_lbl.setText("SHIP TYPE")
        type_select_lyt.addWidget(type_lbl)

        type_choices_lyt = QtWidgets.QVBoxLayout()
        type_choices_lyt.setObjectName("type_choices_lyt")
        type_buttons_lyt = QtWidgets.QHBoxLayout()
        type_buttons_lyt.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        type_buttons_lyt.setObjectName("type_buttons_lyt")

        pt_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        pt_but.setObjectName("pt_but")
        pt_but.setText("CORVETTE")
        type_buttons_lyt.addWidget(pt_but)

        dd_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        dd_but.setObjectName("dd_but")
        dd_but.setText("DESTROYER")
        type_buttons_lyt.addWidget(dd_but)

        ca_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        ca_but.setObjectName("ca_but")
        ca_but.setText("CRUISER")
        type_buttons_lyt.addWidget(ca_but)

        bb_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        bb_but.setObjectName("bb_but")
        bb_but.setText("BATTLESHIP")
        type_buttons_lyt.addWidget(bb_but)

        type_choices_lyt.addLayout(type_buttons_lyt)
        type_select_lyt.addLayout(type_choices_lyt)

        cur_type_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        cur_type_lbl.setMaximumSize(QtCore.QSize(430, 16777215))
        cur_type_lbl.setTextFormat(QtCore.Qt.PlainText)
        cur_type_lbl.setText("Type: ")
        cur_type_lbl.setObjectName("cur_type_lbl")
        type_select_lyt.addWidget(cur_type_lbl)

        ship_creator_lyt.addLayout(type_select_lyt)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        ship_creator_lyt.addItem(spacerItem3)
        tech_lyt = QtWidgets.QVBoxLayout()
        tech_lyt.setObjectName("tech_lyt")
        techs_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        techs_lbl.setFont(font)
        techs_lbl.setObjectName("techs_lbl")
        techs_lbl.setText("TECHNOLOGUES LEVEL")
        tech_lyt.addWidget(techs_lbl)

        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setObjectName("gridLayout")

        radar_tech_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        radar_tech_lbl.setFont(font)
        radar_tech_lbl.setObjectName("radar_tech_lbl")
        radar_tech_lbl.setText("Radar tech")
        gridLayout.addWidget(radar_tech_lbl, 2, 0, 1, 1)

        fc_tech_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        fc_tech_lbl.setFont(font)
        fc_tech_lbl.setObjectName("fc_tech_lbl")
        fc_tech_lbl.setText("Fire Control tech")
        gridLayout.addWidget(fc_tech_lbl, 1, 0, 1, 1)

        gun_tech_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        gun_tech_lbl.setFont(font)
        gun_tech_lbl.setObjectName("gun_tech_lbl")
        gun_tech_lbl.setText("Gun tech")
        gridLayout.addWidget(gun_tech_lbl, 0, 0, 1, 1)

        self.rdr_tech_rButtongrp = QtWidgets.QButtonGroup()
        self.fc_tech_rButtonGroup = QtWidgets.QButtonGroup()
        self.gun_tech_rButtonGroup = QtWidgets.QButtonGroup()

        self.rdr_tech_0 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.rdr_tech_0.setObjectName("rdr_tech_0")
        self.rdr_tech_0.setText("Mk I")
        self.rdr_tech_0.setChecked(True)
        self.rdr_tech_rButtongrp.addButton(self.rdr_tech_0, 0)
        gridLayout.addWidget(self.rdr_tech_0, 2, 1, 1, 1)

        self.fc_tech_0 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.fc_tech_0.setObjectName("fc_tech_0")
        self.fc_tech_0.setText("Mk I")
        self.fc_tech_0.setChecked(True)
        self.fc_tech_rButtonGroup.addButton(self.fc_tech_0, 0)
        gridLayout.addWidget(self.fc_tech_0, 1, 1, 1, 1)

        self.gun_tech_0 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.gun_tech_0.setObjectName("gun_tech_0")
        self.gun_tech_0.setText("Mk I")
        self.gun_tech_0.setChecked(True)
        self.gun_tech_rButtonGroup.addButton(self.gun_tech_0, 0)
        gridLayout.addWidget(self.gun_tech_0, 0, 1, 1, 1)

        self.rdr_tech_1 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.rdr_tech_1.setObjectName("rdr_tech_1")
        self.rdr_tech_1.setText("Mk II")
        self.rdr_tech_rButtongrp.addButton(self.rdr_tech_1, 1)
        gridLayout.addWidget(self.rdr_tech_1, 2, 2, 1, 1)

        self.fc_tech_1 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.fc_tech_1.setObjectName("fc_tech_1")
        self.fc_tech_1.setText("Mk II")
        self.fc_tech_rButtonGroup.addButton(self.fc_tech_1, 1)
        gridLayout.addWidget(self.fc_tech_1, 1, 2, 1, 1)

        self.gun_tech_1 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.gun_tech_1.setObjectName("gun_tech_1")
        self.gun_tech_1.setText("Mk II")
        self.gun_tech_rButtonGroup.addButton(self.gun_tech_1, 1)
        gridLayout.addWidget(self.gun_tech_1, 0, 2, 1, 1)

        self.rdr_tech_2 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.rdr_tech_2.setObjectName("rdr_tech_2")
        self.rdr_tech_2.setText("Mk III")
        self.rdr_tech_rButtongrp.addButton(self.rdr_tech_2, 2)
        gridLayout.addWidget(self.rdr_tech_2, 2, 3, 1, 1)

        self.fc_tech_2 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.fc_tech_2.setObjectName("fc_tech_2")
        self.fc_tech_2.setText("Mk III")
        self.fc_tech_rButtonGroup.addButton(self.fc_tech_2, 2)
        gridLayout.addWidget(self.fc_tech_2, 1, 3, 1, 1)

        self.gun_tech_2 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        self.gun_tech_2.setObjectName("gun_tech_2")
        self.gun_tech_2.setText("Mk III")
        self.gun_tech_rButtonGroup.addButton(self.gun_tech_2, 2)
        gridLayout.addWidget(self.gun_tech_2, 0, 3, 1, 1)

        tech_lyt.addLayout(gridLayout)
        ship_creator_lyt.addLayout(tech_lyt)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        ship_creator_lyt.addItem(spacerItem4)

        ship_stats_lyt = QtWidgets.QVBoxLayout()
        ship_stats_lyt.setObjectName("ship_stats_lyt")

        ship_stats_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        ship_stats_lbl.setFont(font)
        ship_stats_lbl.setObjectName("ship_stats_lbl")
        ship_stats_lbl.setText("SHIP CHARACTERISTICS")
        ship_stats_lyt.addWidget(ship_stats_lbl)

        ship_stats_lyt_2 = QtWidgets.QHBoxLayout()
        ship_stats_lyt_2.setObjectName("ship_stats_lyt_2")
        ship_stats_lyt_3 = QtWidgets.QVBoxLayout()
        ship_stats_lyt_3.setObjectName("ship_stats_lyt_3")

        general_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        general_label.setFont(font)
        general_label.setObjectName("general_label")
        general_label.setText("GENERAL")
        ship_stats_lyt_3.addWidget(general_label)

        type_lyt = QtWidgets.QHBoxLayout()
        type_lyt.setObjectName("type_lyt")
        type_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        type_label.setObjectName("type_label")
        type_label.setText("Description:")
        type_lyt.addWidget(type_label)

        self.ship_type_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_type_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_type_label.setObjectName("ship_type_label")
        self.ship_type_label.setText("")
        type_lyt.addWidget(self.ship_type_label)

        ship_stats_lyt_3.addLayout(type_lyt)
        name_lyt = QtWidgets.QHBoxLayout()
        name_lyt.setObjectName("name_lyt")
        name_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        name_label.setObjectName("name_label")
        name_label.setText("Name:")
        name_lyt.addWidget(name_label)

        self.ship_name_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_name_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_name_label.setObjectName("ship_name_label")
        self.ship_name_label.setText("")
        name_lyt.addWidget(self.ship_name_label)

        ship_stats_lyt_3.addLayout(name_lyt)
        len_lyt = QtWidgets.QHBoxLayout()
        len_lyt.setObjectName("len_lyt")
        length_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        length_lbl.setObjectName("length_lbl")
        length_lbl.setText("Length:")
        len_lyt.addWidget(length_lbl)

        self.ship_length_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_length_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_length_lbl.setObjectName("ship_length_lbl")
        self.ship_length_lbl.setText("")
        len_lyt.addWidget(self.ship_length_lbl)

        ship_stats_lyt_3.addLayout(len_lyt)
        widht_layout = QtWidgets.QHBoxLayout()
        widht_layout.setObjectName("widht_layout")

        width_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        width_lbl.setObjectName("width_lbl")
        width_lbl.setText("Width:")
        widht_layout.addWidget(width_lbl)

        self.ship_width_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_width_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_width_lbl.setObjectName("ship_width_lbl")
        self.ship_width_lbl.setText("")
        widht_layout.addWidget(self.ship_width_lbl)

        ship_stats_lyt_3.addLayout(widht_layout)
        line = QtWidgets.QFrame(verticalLayoutWidget_2)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        ship_stats_lyt_3.addWidget(line)

        weapons_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        weapons_lbl.setFont(font)
        weapons_lbl.setObjectName("weapons_lbl")
        weapons_lbl.setText("WEAPONS")
        ship_stats_lyt_3.addWidget(weapons_lbl)

        main_guns_lyt = QtWidgets.QHBoxLayout()
        main_guns_lyt.setObjectName("main_guns_lyt")

        ship_mg_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_mg_lbl.setObjectName("ship_mg_lbl")
        ship_mg_lbl.setText("Main guns:")
        main_guns_lyt.addWidget(ship_mg_lbl)

        self.ship_w_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_w_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_w_lbl.setObjectName("ship_w_lbl")
        self.ship_w_lbl.setText("")
        main_guns_lyt.addWidget(self.ship_w_lbl)

        ship_stats_lyt_3.addLayout(main_guns_lyt)
        acc_lyt = QtWidgets.QHBoxLayout()
        acc_lyt.setObjectName("acc_lyt")

        acc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        acc_lbl.setObjectName("acc_lbl")
        acc_lbl.setText("Guns accuracy:")
        acc_lyt.addWidget(acc_lbl)

        self.ship_acc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_acc_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_acc_lbl.setObjectName("ship_acc_lbl")
        self.ship_acc_lbl.setText("")
        acc_lyt.addWidget(self.ship_acc_lbl)

        ship_stats_lyt_3.addLayout(acc_lyt)
        fc_lyt = QtWidgets.QHBoxLayout()
        fc_lyt.setObjectName("fc_lyt")

        fc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        fc_lbl.setObjectName("fc_lbl")
        fc_lbl.setText("Fire control error:")
        fc_lyt.addWidget(fc_lbl)

        self.ship_fc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_fc_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_fc_lbl.setObjectName("ship_fc_lbl")
        self.ship_fc_lbl.setText("")
        fc_lyt.addWidget(self.ship_fc_lbl)

        ship_stats_lyt_3.addLayout(fc_lyt)
        err_reduc_lyt = QtWidgets.QHBoxLayout()
        err_reduc_lyt.setObjectName("err_reduc_lyt")

        w_range_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        w_range_lbl.setObjectName("w_range_lbl")
        w_range_lbl.setText("Guns range:")
        err_reduc_lyt.addWidget(w_range_lbl)

        self.ship_w_range_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_w_range_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_w_range_lbl.setObjectName("ship_w_range_lbl")
        self.ship_w_range_lbl.setText("")
        err_reduc_lyt.addWidget(self.ship_w_range_lbl)

        ship_stats_lyt_3.addLayout(err_reduc_lyt)
        ship_stats_lyt_2.addLayout(ship_stats_lyt_3)
        line_4 = QtWidgets.QFrame(verticalLayoutWidget_2)
        line_4.setFrameShape(QtWidgets.QFrame.VLine)
        line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_4.setObjectName("line_4")
        ship_stats_lyt_2.addWidget(line_4)
        hull_stats_lyt = QtWidgets.QVBoxLayout()
        hull_stats_lyt.setObjectName("hull_stats_lyt")

        hull_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        hull_label.setFont(font)
        hull_label.setObjectName("hull_label")
        hull_label.setText("HULL")
        hull_stats_lyt.addWidget(hull_label)

        hp_lyt = QtWidgets.QHBoxLayout()
        hp_lyt.setObjectName("hp_lyt")

        max_hp_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        max_hp_lbl.setObjectName("max_hp_lbl")
        max_hp_lbl.setText("HP:")
        hp_lyt.addWidget(max_hp_lbl)

        self.ship_max_hp_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_max_hp_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_max_hp_lbl.setObjectName("ship_max_hp_lbl")
        self.ship_max_hp_lbl.setText("")
        hp_lyt.addWidget(self.ship_max_hp_lbl)

        hull_stats_lyt.addLayout(hp_lyt)
        armor_lyt = QtWidgets.QHBoxLayout()
        armor_lyt.setObjectName("armor_lyt")

        armor_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        armor_lbl.setObjectName("armor_lbl")
        armor_lbl.setText("Armor:")
        armor_lyt.addWidget(armor_lbl)

        self.ship_armor_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_armor_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_armor_lbl.setObjectName("ship_armor_lbl")
        self.ship_armor_lbl.setText("")
        armor_lyt.addWidget(self.ship_armor_lbl)

        hull_stats_lyt.addLayout(armor_lyt)
        shield_lyt = QtWidgets.QHBoxLayout()
        shield_lyt.setObjectName("shield_lyt")

        shield_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        shield_lbl.setObjectName("shield_lbl")
        shield_lbl.setText("Shield:")
        shield_lyt.addWidget(shield_lbl)

        self.ship_shield_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_shield_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_shield_lbl.setObjectName("ship_shield_lbl")
        self.ship_shield_lbl.setText("")
        shield_lyt.addWidget(self.ship_shield_lbl)

        hull_stats_lyt.addLayout(shield_lyt)
        line_2 = QtWidgets.QFrame(verticalLayoutWidget_2)
        line_2.setFrameShape(QtWidgets.QFrame.HLine)
        line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_2.setObjectName("line_2")
        hull_stats_lyt.addWidget(line_2)

        mobility_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        mobility_lbl.setFont(font)
        mobility_lbl.setObjectName("mobility_lbl")
        mobility_lbl.setText("MOBILITY")
        hull_stats_lyt.addWidget(mobility_lbl)

        speed_lyt = QtWidgets.QHBoxLayout()
        speed_lyt.setObjectName("speed_lyt")

        v_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        v_lbl.setObjectName("v_lbl")
        v_lbl.setText("Speed:")
        speed_lyt.addWidget(v_lbl)

        self.ship_v_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_v_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_v_lbl.setObjectName("ship_v_lbl")
        self.ship_v_lbl.setText("")
        speed_lyt.addWidget(self.ship_v_lbl)

        hull_stats_lyt.addLayout(speed_lyt)
        accel_lyt = QtWidgets.QHBoxLayout()
        accel_lyt.setObjectName("accel_lyt")

        accel_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        accel_lbl.setObjectName("accel_lbl")
        accel_lbl.setText("Acceleration:")
        accel_lyt.addWidget(accel_lbl)

        self.ship_accel_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_accel_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_accel_lbl.setObjectName("ship_accel_lbl")
        self.ship_accel_lbl.setText("")
        accel_lyt.addWidget(self.ship_accel_lbl)

        hull_stats_lyt.addLayout(accel_lyt)
        t_rate_lyt = QtWidgets.QHBoxLayout()
        t_rate_lyt.setObjectName("t_rate_lyt")

        t_rate_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        t_rate_lbl.setObjectName("t_rate_lbl")
        t_rate_lbl.setText("Turn rate:")
        t_rate_lyt.addWidget(t_rate_lbl)

        self.ship_t_rate_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_t_rate_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_t_rate_lbl.setObjectName("ship_t_rate_lbl")
        self.ship_t_rate_lbl.setText("")
        t_rate_lyt.addWidget(self.ship_t_rate_lbl)

        hull_stats_lyt.addLayout(t_rate_lyt)
        line_3 = QtWidgets.QFrame(verticalLayoutWidget_2)
        line_3.setFrameShape(QtWidgets.QFrame.HLine)
        line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        line_3.setObjectName("line_3")
        hull_stats_lyt.addWidget(line_3)

        vnc_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        vnc_label.setFont(font)
        vnc_label.setObjectName("vnc_label")
        vnc_label.setText("VISION & CONCEALMENT")
        hull_stats_lyt.addWidget(vnc_label)

        vision_lyt = QtWidgets.QHBoxLayout()
        vision_lyt.setObjectName("vision_lyt")

        vision_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        vision_lbl.setObjectName("vision_lbl")
        vision_lbl.setText("Vision range:")
        vision_lyt.addWidget(vision_lbl)

        self.ship_vision_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_vision_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_vision_lbl.setObjectName("ship_vision_lbl")
        self.ship_vision_lbl.setText("")
        vision_lyt.addWidget(self.ship_vision_lbl)

        hull_stats_lyt.addLayout(vision_lyt)
        concl_lyt = QtWidgets.QHBoxLayout()
        concl_lyt.setObjectName("concl_lyt")

        concl_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        concl_lbl.setObjectName("concl_lbl")
        concl_lbl.setText("Concealment:")
        concl_lyt.addWidget(concl_lbl)

        self.ship_concl_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_concl_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.ship_concl_lbl.setObjectName("ship_concl_lbl")
        self.ship_concl_lbl.setText("")
        concl_lyt.addWidget(self.ship_concl_lbl)

        hull_stats_lyt.addLayout(concl_lyt)
        ship_stats_lyt_2.addLayout(hull_stats_lyt)
        ship_stats_lyt.addLayout(ship_stats_lyt_2)
        ship_creator_lyt.addLayout(ship_stats_lyt)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        ship_creator_lyt.addItem(spacerItem5)
        clear_add_but_lyt = QtWidgets.QHBoxLayout()
        clear_add_but_lyt.setObjectName("clear_add_but_lyt")

        ship_cost_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_cost_lbl.setObjectName("ship_cost_lbl")
        ship_cost_lbl.setText("SHIP COST:")
        clear_add_but_lyt.addWidget(ship_cost_lbl)

        self.ship_cost = QtWidgets.QLabel(verticalLayoutWidget_2)
        self.ship_cost.setObjectName("ship_cost")
        self.ship_cost.setText(str(0))
        clear_add_but_lyt.addWidget(self.ship_cost)

        spacerItem6 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        clear_add_but_lyt.addItem(spacerItem6)

        self.clear_ship_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        self.clear_ship_but.setObjectName("clear_ship_but")
        self.clear_ship_but.setText("Reset Ship")
        self.clear_ship_but.setEnabled(False)
        clear_add_but_lyt.addWidget(self.clear_ship_but)

        self.add_ship_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        self.add_ship_but.setObjectName("add_ship_but")
        self.add_ship_but.setText("Add Ship")
        self.add_ship_but.setEnabled(False)
        clear_add_but_lyt.addWidget(self.add_ship_but)
        ship_creator_lyt.addLayout(clear_add_but_lyt)

        QtCore.QMetaObject.connectSlotsByName(fleet_setup)
        self.setEnabledRadioButtons(False)

        ## Ship type selection button ##
        bb_but.clicked.connect(lambda: self.shipButtonClicked("BB"))
        ca_but.clicked.connect(lambda: self.shipButtonClicked("CA"))
        dd_but.clicked.connect(lambda: self.shipButtonClicked("DD"))
        pt_but.clicked.connect(lambda: self.shipButtonClicked("PT"))

        ## Updates stats when another tech is selected ##
        self.rdr_tech_0.clicked.connect(self.updateShipStats)
        self.rdr_tech_1.clicked.connect(self.updateShipStats)
        self.rdr_tech_2.clicked.connect(self.updateShipStats)

        self.fc_tech_0.clicked.connect(self.updateShipStats)
        self.fc_tech_1.clicked.connect(self.updateShipStats)
        self.fc_tech_2.clicked.connect(self.updateShipStats)

        self.gun_tech_0.clicked.connect(self.updateShipStats)
        self.gun_tech_1.clicked.connect(self.updateShipStats)
        self.gun_tech_2.clicked.connect(self.updateShipStats)

        ## Add, reset or delete current ship ##
        self.add_ship_but.clicked.connect(self.addShip)
        self.clear_ship_but.clicked.connect(self.resetButtonClicked)
        del_ship_but.clicked.connect(self.listView.removeFromList)

        ## reset, load or save fleet ##
        clear_fleet_but.clicked.connect(self.clearFleet)

        ## Battle button ##
        battle_but.clicked.connect(lambda: self.createFleetAccept(fleet_setup))
        return fleet_setup.exec()

    def battleSetupUI(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Generates battleSetup UI, binds actions and buttons to functions.

        """
        battle_setup = QtWidgets.QDialog()
        battle_setup.setObjectName("battle_setup")
        battle_setup.resize(400, 300)
        battle_setup.setMinimumSize(QtCore.QSize(400, 300))
        battle_setup.setMaximumSize(QtCore.QSize(400, 300))
        battle_setup.setWindowTitle("Battle Setup")
        gridLayout = QtWidgets.QGridLayout(battle_setup)
        gridLayout.setObjectName("gridLayout")
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        horizontalLayout.addItem(spacerItem)

        cancelButton = QtWidgets.QPushButton(battle_setup)
        cancelButton.setObjectName("cancelButton")
        cancelButton.setText("Cancel")
        horizontalLayout.addWidget(cancelButton)

        ok_button = QtWidgets.QPushButton(battle_setup)
        ok_button.setObjectName("ok_button")
        ok_button.setText("Assemble The Fleet !")
        horizontalLayout.addWidget(ok_button)

        gridLayout.addLayout(horizontalLayout, 9, 1, 1, 1)
        self.points_cmbbox = QtWidgets.QComboBox(battle_setup)
        self.points_cmbbox.setObjectName("points_cmbbox")
        self.points_cmbbox.addItem("25")
        self.points_cmbbox.addItem("50")
        self.points_cmbbox.addItem("75")
        self.points_cmbbox.setEnabled(False)
        gridLayout.addWidget(self.points_cmbbox, 7, 1, 1, 1)

        self.difficulty_cmbbox = QtWidgets.QComboBox(battle_setup)
        self.difficulty_cmbbox.setObjectName("difficulty_cmbbox")
        self.difficulty_cmbbox.addItem("Easy")
        self.difficulty_cmbbox.addItem("Normal")
        self.difficulty_cmbbox.addItem("Hard")
        self.difficulty_cmbbox.addItem("Very Hard")
        gridLayout.addWidget(self.difficulty_cmbbox, 3, 1, 1, 1)

        map_size_lbl = QtWidgets.QLabel(battle_setup)
        map_size_lbl.setObjectName("map_size_lbl")
        map_size_lbl.setText("Map size:")
        gridLayout.addWidget(map_size_lbl, 1, 0, 1, 1)

        self.funds_cmbbox = QtWidgets.QComboBox(battle_setup)
        self.funds_cmbbox.setObjectName("funds_cmbbox")
        self.funds_cmbbox.addItem("Small")
        self.funds_cmbbox.addItem("Standard")
        self.funds_cmbbox.addItem("Large")
        self.funds_cmbbox.addItem("Custom")
        gridLayout.addWidget(self.funds_cmbbox, 4, 1, 1, 1)

        funds_lbl = QtWidgets.QLabel(battle_setup)
        funds_lbl.setObjectName("funds_lbl")
        funds_lbl.setText("Funds:")
        gridLayout.addWidget(funds_lbl, 4, 0, 1, 1)

        self.maps_comboBox = QtWidgets.QComboBox(battle_setup)
        self.maps_comboBox.setObjectName("maps_comboBox")
        self.maps_comboBox.addItem("Random")
        self.maps_comboBox.addItem("Map 1")
        self.maps_comboBox.addItem("Map 2")
        gridLayout.addWidget(self.maps_comboBox, 0, 1, 1, 1)

        difficulty_lbl = QtWidgets.QLabel(battle_setup)
        difficulty_lbl.setObjectName("difficulty_lbl")
        difficulty_lbl.setText("Difficulty:")
        gridLayout.addWidget(difficulty_lbl, 3, 0, 1, 1)

        self.v_cond_cmbbox = QtWidgets.QComboBox(battle_setup)
        self.v_cond_cmbbox.setObjectName("v_cond_cmbbox")
        self.v_cond_cmbbox.addItem("Annihilation")
        self.v_cond_cmbbox.addItem("Points (%)")
        self.v_cond_cmbbox.setToolTip(
            "Choose between total destruction of the ennemy fleet or destruction of a percentage of its fleet"
        )
        gridLayout.addWidget(self.v_cond_cmbbox, 6, 1, 1, 1)

        map_obs_lbl = QtWidgets.QLabel(battle_setup)
        map_obs_lbl.setObjectName("map_obs_lbl")
        map_obs_lbl.setText("Map obstruction:")
        gridLayout.addWidget(map_obs_lbl, 2, 0, 1, 1)

        v_cond_lbl = QtWidgets.QLabel(battle_setup)
        v_cond_lbl.setObjectName("v_cond_lbl")
        v_cond_lbl.setText("Victory condition:")
        gridLayout.addWidget(v_cond_lbl, 6, 0, 1, 1)

        sel_s_map_lbl = QtWidgets.QLabel(battle_setup)
        sel_s_map_lbl.setObjectName("sel_s_map_lbl")
        sel_s_map_lbl.setText("Selected Map:")
        gridLayout.addWidget(sel_s_map_lbl, 0, 0, 1, 1)

        self.map_size_cmbbox = QtWidgets.QComboBox(battle_setup)
        self.map_size_cmbbox.setObjectName("map_size_cmbbox")
        self.map_size_cmbbox.addItem("Small")
        self.map_size_cmbbox.addItem("Medium")
        self.map_size_cmbbox.addItem("Large")
        gridLayout.addWidget(self.map_size_cmbbox, 1, 1, 1, 1)

        self.cstm_funds_l_edit = QtWidgets.QLineEdit(battle_setup)
        self.cstm_funds_l_edit.setObjectName("cstm_funds_l_edit")
        self.cstm_funds_l_edit.setEnabled(False)
        gridLayout.addWidget(self.cstm_funds_l_edit, 5, 1, 1, 1)

        self.mapObs_cmbbox = QtWidgets.QComboBox(battle_setup)
        self.mapObs_cmbbox.setObjectName("mapObs_cmbbox")
        self.mapObs_cmbbox.addItem("Open")
        self.mapObs_cmbbox.addItem("Light")
        self.mapObs_cmbbox.addItem("Medium")
        self.mapObs_cmbbox.addItem("Heavy")
        self.mapObs_cmbbox.setToolTip(
            "Defines how much of the map is covered by obstacles"
        )
        gridLayout.addWidget(self.mapObs_cmbbox, 2, 1, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        gridLayout.addItem(spacerItem1, 8, 1, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(battle_setup)
        self.updateMapConfig()

        self.maps_comboBox.currentTextChanged.connect(
            lambda: self.setEnabledOtherWidget(self.maps_comboBox)
        )
        self.funds_cmbbox.currentTextChanged.connect(
            lambda: self.setEnabledOtherWidget(self.funds_cmbbox)
        )
        self.v_cond_cmbbox.currentTextChanged.connect(
            lambda: self.setEnabledOtherWidget(self.v_cond_cmbbox)
        )
        ok_button.clicked.connect(lambda: self.battleSetupAccept(battle_setup))
        cancelButton.clicked.connect(battle_setup.reject)

        return battle_setup.exec()

    def setEnabledRadioButtons(self, state: bool):
        """

        Parameters
        ----------
        state : bool
            True enables the radio buttons, False disables.

        Returns
        -------
        None.

        Summary
        -------
        Enables or disables the radio buttons depending on state.

        """
        for radioButton in self.rdr_tech_rButtongrp.buttons():
            radioButton.setEnabled(state)

        for radioButton in self.fc_tech_rButtonGroup.buttons():
            radioButton.setEnabled(state)

        for radioButton in self.gun_tech_rButtonGroup.buttons():
            radioButton.setEnabled(state)

    def shipButtonClicked(self, _type: str):
        """

        Parameters
        ----------
        _type : string
            The type indicated by the button.

        Returns
        -------
        None

        Summary
        -------
        Add a base configuration of ship of _type to the user's fleet.

        """
        if _type == "BB":
            self.currentShip = copy.deepcopy(self.bb_dict)
            self.currentTurDict = copy.deepcopy(self.tur_dict["large"])
        elif _type == "CA":
            self.currentShip = copy.deepcopy(self.ca_dict)
            self.currentTurDict = self.tur_dict["medium"]
        elif _type == "DD":
            self.currentShip = copy.deepcopy(self.dd_dict)
            self.currentTurDict = self.tur_dict["small"]
        # elif _type == "PT":
        #     self.currentShip = copy.deepcopy(self.pt_dict)
        #     self.currentTurDict = self.tur_dict["small"]
        else:
            print("Type value error: The given type does not match any ship type.")

        if not self.clear_ship_but.isEnabled():
            self.clear_ship_but.setEnabled(True)
            self.add_ship_but.setEnabled(True)

        try:
            if not self.radioButtonsEnabled:
                self.setEnabledRadioButtons(True)
                self.radioButtonsEnabled = True
            self.resetShipStats()
            self.updateShipStats()
        except Exception as e:
            print("Could not update UI", e)

    def updateShipCreatorUI(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Update the static part of the ship creator display.

        """
        ## General section ##
        self.ship_name_label.setText(str(self.currentShip["naming"]["_name"]))
        self.ship_type_label.setText(str(self.currentShip["naming"]["_type"]))
        self.ship_length_lbl.setText(str(self.currentShip["geometry"]["_width"]))
        self.ship_width_lbl.setText(str(self.currentShip["geometry"]["_height"]))

        ## Weapons section ##
        total_guns = (
            len(self.currentShip["weapons"]["turrets_pos"])
            * self.currentTurDict["n_guns"]
        )
        guns_txt = str(total_guns) + " " + self.currentTurDict["_size"]
        self.ship_w_lbl.setText(guns_txt)
        self.ship_w_range_lbl.setText(str(self.currentShip["weapons"]["guns_range"]))

        ## Hull section ##
        self.ship_max_hp_lbl.setText(str(self.currentShip["hull"]["max_hp"]))
        self.ship_armor_lbl.setText(str(self.currentShip["hull"]["armor"]))
        self.ship_shield_lbl.setText(str(self.currentShip["hull"]["max_shield"]))

        ## Mobility section ##
        self.ship_v_lbl.setText(str(self.currentShip["hull"]["max_speed"]))
        self.ship_accel_lbl.setText(str(self.currentShip["hull"]["max_accel"]))
        self.ship_t_rate_lbl.setText(str(self.currentShip["hull"]["turn_rate"]))

        ## Vision & Concealement section ##
        self.ship_concl_lbl.setText(str(self.currentShip["hull"]["base_concealement"]))

    def set_blank_ship_stats(self):
        ## reset Tech Levels ##
        self.rdr_tech_0.setChecked(True)
        self.fc_tech_0.setChecked(True)
        self.gun_tech_0.setChecked(True)

        ## Deactivate current ship related buttons ##
        self.clear_ship_but.setEnabled(False)
        self.add_ship_but.setEnabled(False)

        ## Set current_key to None ##
        self.currentShipKey = None

        ## General section ##
        self.ship_name_label.setText("")
        self.ship_type_label.setText("")
        self.ship_length_lbl.setText("")
        self.ship_width_lbl.setText("")

        self.ship_w_lbl.setText("")
        self.ship_w_range_lbl.setText("")

        ## Hull section ##
        self.ship_max_hp_lbl.setText("")
        self.ship_armor_lbl.setText("")
        self.ship_shield_lbl.setText("")

        ## Mobility section ##
        self.ship_v_lbl.setText("")
        self.ship_accel_lbl.setText("")
        self.ship_t_rate_lbl.setText("")

        ## Vision & Concealement section ##
        self.ship_concl_lbl.setText("")

        ## Calculated stats ##
        self.ship_acc_lbl.setText("")
        self.ship_fc_lbl.setText("")
        self.ship_vision_lbl.setText("")
        self.ship_cost.setText("")

    def resetShipStats(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Set the lowest tech levels radio buttons to checked.

        """
        self.rdr_tech_0.setChecked(True)
        self.fc_tech_0.setChecked(True)
        self.gun_tech_0.setChecked(True)

        self.updateShipCreatorUI()

    def updateShipStats(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Recalculate the current ship stats and updates the dynamic displays.

        """
        a, b, c = (
            self.gun_tech_rButtonGroup.checkedId(),
            self.fc_tech_rButtonGroup.checkedId(),
            self.rdr_tech_rButtongrp.checkedId(),
        )
        self.currentShip["techs"]["guns_tech"] = a
        self.currentShip["techs"]["fc_tech"] = b
        self.currentShip["techs"]["radar_tech"] = c
        self.currentShip["naming"]["cost"] = self.updateShipCost(
            self.currentShip["naming"]["base_cost"], [a, b, c]
        )

        currentAcc = round(
            self.currentTurDict["gun_disp"] * tech_dat.gun_tech_acc[a], 4
        )
        currentVision = (
            self.currentShip["hull"]["base_detection_range"]
            + self.currentShip["hull"]["base_detection_range"]
            * tech_dat.radar_tech_aug[c]
        )

        self.ship_acc_lbl.setText(str(currentAcc))
        self.ship_fc_lbl.setText(str(tech_dat.fc_tech_e[b]))
        self.ship_vision_lbl.setText(str(currentVision))
        self.ship_cost.setText(str(self.currentShip["naming"]["cost"]))

        if self.currentShipKey in self.allShips:
            self.allShips[self.currentShipKey] = copy.deepcopy(self.currentShip)
            self.updateFleetCost()

    def updateShipCost(self, baseCost: int, techLevelsList: list):
        """

        Parameters
        ----------
        baseCost : int
            The cost of the vanilla ship.
        techLevelsList : list
            The list of the tech levels.

        Returns
        -------
        shipCost : int
            The final cost of the ship.

        Summary
        -------
        Calculates the final cost of the ship, technologies cost included.

        """
        shipCost = baseCost

        for techLevel in techLevelsList:
            if techLevel == 1:
                shipCost += tech_dat.cost_per_tech[0]
            elif techLevel == 2:
                shipCost += tech_dat.cost_per_tech[1]

        return shipCost

    def updateFleetCost(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Calculate the fleet cost according to all ships current cost.
        Updates the displays.

        """
        self.fleetCost = 0

        for ship in self.allShips.values():
            self.fleetCost += ship["naming"]["cost"]
        self.cur_fleet_cost_lbl.setText(
            str(self.fleetCost) + " / " + str(self.currentMapConfig["funds"])
        )

    def setStatsFomList(self, _shipKey: int):
        """

        Parameters
        ----------
        _shipKey : int
            The key at which the ship's data will be retrieved.

        Summary
        -------
        Goes through allShips dict.
        Load the stats and update the dispays of the ship config
        found at the key _shipKey.

        """
        for shipKey, ship in self.allShips.items():
            if shipKey == _shipKey:
                self.currentShip = copy.deepcopy(ship)
                break

        a, b, c = (
            self.currentShip["techs"]["guns_tech"],
            self.currentShip["techs"]["fc_tech"],
            self.currentShip["techs"]["radar_tech"],
        )
        self.gun_tech_rButtonGroup.button(a).setChecked(True)
        self.fc_tech_rButtonGroup.button(b).setChecked(True)
        self.rdr_tech_rButtongrp.button(c).setChecked(True)
        shipCost = self.updateShipCost(
            self.currentShip["naming"]["base_cost"], [a, b, c]
        )

        if self.currentShip["naming"]["_type"] == "BB":
            self.currentTurDict = copy.deepcopy(self.tur_dict["large"])
        elif self.currentShip["naming"]["_type"] == "CA":
            self.currentTurDict = copy.deepcopy(self.tur_dict["medium"])
        elif self.currentShip["naming"]["_type"] == "DD":
            self.currentTurDict = copy.deepcopy(self.tur_dict["small"])
        elif self.currentShip["naming"]["_type"] == "PT":
            self.currentTurDict = copy.deepcopy(self.tur_dict["small"])
        else:
            print("Could not retrieve turret informations")

        self.updateShipCreatorUI()

        currentAcc = round(
            self.currentTurDict["gun_disp"] * tech_dat.gun_tech_acc[a], 4
        )
        currentVision = (
            self.currentShip["hull"]["base_detection_range"]
            + self.currentShip["hull"]["base_detection_range"]
            * tech_dat.radar_tech_aug[c]
        )

        self.ship_acc_lbl.setText(str(currentAcc))
        self.ship_fc_lbl.setText(str(tech_dat.fc_tech_e[b]))
        self.ship_vision_lbl.setText(str(currentVision))
        self.ship_cost.setText(str(shipCost))

        self.currentShipKey = shipKey

    def resetButtonClicked(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Resets current ship stats to defaults.

        """
        self.resetShipStats()
        self.updateShipStats()

    def addShip(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Adds the currently defined ship to the all ships dictionnary,
        Adds a reference into the list.

        """
        if self.currentShip["naming"]["_type"] == "BB":
            name_file = path.join(
                path.dirname(path.realpath(__file__)),
                "../../resources/names/names_battleships.txt",
            )
        elif self.currentShip["naming"]["_type"] == "CA":
            name_file = path.join(
                path.dirname(path.realpath(__file__)),
                "../../resources/names/names_cruisers.txt",
            )
        elif self.currentShip["naming"]["_type"] == "DD":
            name_file = path.join(
                path.dirname(path.realpath(__file__)),
                "../../resources/names/names_destroyers.txt",
            )
        elif self.currentShip["naming"]["_type"] == "PT":
            name_file = path.join(
                path.dirname(path.realpath(__file__)),
                "../../resources/names/names_submarine.txt",
            )
        self.currentShip["naming"]["_name"] = Imports.random_name(name_file)
        self.allShips[self.shipCounter] = copy.deepcopy(self.currentShip)
        self.listView.addToList(
            self.shipCounter,
            self.currentShip["naming"]["_type"],
            self.currentShip["naming"]["_name"],
        )
        self.shipCounter += 1
        self.currentShipKey = self.shipCounter
        self.updateFleetCost()

    def removeShips(self, shipKeysList: list):
        """

        Parameters
        ----------
        shipKeysList : list of int
            A list of all the keys of the ship configs to remove.

        Returns
        -------
        None.

        Summary
        -------
        Removes all the pairs (_shipKey, shipConfig) for _shipKey
        in shipKeysList.

        """
        for shipKey in shipKeysList:
            try:
                self.allShips.pop(shipKey)
            except KeyError as ke:
                print("Could not find ship to delete", "\n", ke)

        self.updateFleetCost()

    def clearFleet(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Clears the current fleet from all ships.

        """
        self.allShips.clear()
        self.listView.clearList()
        self.updateFleetCost()

    def setEnabledOtherWidget(self, comboBox: QtWidgets.QComboBox):
        """

        Parameters
        ----------
        comboBox: QtWidgets.QComboBox
            The selected como box.

        Returns
        -------
        None.

        Summary
        -------
        Enables or disable other widgets according to
        the current text of combo box.

        """
        if comboBox is self.maps_comboBox:
            if str(comboBox.currentText()) != "Random":
                self.map_size_cmbbox.setEnabled(False)
                self.mapObs_cmbbox.setEnabled(False)
            else:
                self.map_size_cmbbox.setEnabled(True)
                self.mapObs_cmbbox.setEnabled(True)

        elif comboBox is self.funds_cmbbox:
            if str(comboBox.currentText()) != "Custom":
                self.cstm_funds_l_edit.setEnabled(False)
            else:
                self.cstm_funds_l_edit.setEnabled(True)

        elif comboBox is self.v_cond_cmbbox:
            if str(comboBox.currentText()) == "Annihilation":
                self.points_cmbbox.setEnabled(False)
            else:
                self.points_cmbbox.setEnabled(True)

    def resetMapConfig(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Resets the current Map config to its default values.

        """
        self.currentMapConfig.clear()

        self.currentMapConfig = {
            "presetMap": False,
            "size": 0,
            "obstruction": 0,
            "difficulty": "",
            "funds": 0,
            "victoryCondition": 0,
            "resolution": 0,
            "obstaclesSetup": [],
            "extension": 0,
        }
        self.currentMapConfig["resolution"] = self.map_dict["mapResolution"]
        self.currentMapConfig["obstaclesSetup"] = self.map_dict["obstacles"]
        self.currentMapConfig["extension"] = self.map_dict["mapExtension"]

    def updateMapConfig(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Sets the current map config according to the state of the battlesetup UI.

        """
        if self.maps_comboBox.currentText() == "Random":
            self.currentMapConfig["presetMap"] = False
        else:
            self.currentMapConfig["presetMap"] = self.maps_comboBox.currentText()

        self.currentMapConfig["size"] = self.map_dict["size"][
            self.map_size_cmbbox.currentText()
        ]
        self.currentMapConfig["obstruction"] = self.map_dict["obstruction"][
            self.mapObs_cmbbox.currentText()
        ]
        self.currentMapConfig["difficulty"] = self.difficulty_cmbbox.currentText()

        if self.funds_cmbbox.currentText() == "Custom":
            try:
                self.currentMapConfig["funds"] = int(self.cstm_funds_l_edit.text())
            except Exception:
                dialogsUtils.popMessageBox(
                    "Error", 2, "Please fill in custom funds field", 1
                )
                return 1
        else:
            self.currentMapConfig["funds"] = self.map_dict["funds"][
                self.funds_cmbbox.currentText()
            ]

        if self.v_cond_cmbbox.currentText() == "Annihilation":
            self.currentMapConfig["victoryCondition"] = 1
        else:
            self.currentMapConfig["victoryCondition"] = int(
                int(self.points_cmbbox.currentText()) / 100
            )

        return 0

    def createFleetAccept(self, dialog: QtWidgets.QDialog):
        """

        Parameters
        ----------
        dialog : QtWidgets.QDialog
            The FleetCreator Dialog.

        Returns
        -------
        None.

        Summary
        -------
        Tests if the fleet can be created. If yes, set the dialog state to accepted.

        """
        if len(self.allShips) <= 0:
            dialogsUtils.popMessageBox(
                "Error", 2, "You can't go to battle with no ships in your fleet !", 1
            )
            return

        if self.fleetCost > self.currentMapConfig["funds"]:
            dialogsUtils.popMessageBox(
                "Error",
                2,
                "Your fleet's budget is above what the Admiralty allowed you. Reduce your fleet's cost before engaging the battle.",
                1,
            )
            return

        if (self.currentMapConfig["funds"] - self.fleetCost) >= tech_dat.cost_per_tech[
            0
        ]:
            result = dialogsUtils.OkCancelDialog(
                "Warning",
                1,
                "Admiral, It looks like you still have funds left for your fleet. Do you want to engage the battle anyways ?",
            )
            if result == 4194304:
                return

        dialog.accept()

    def battleSetupAccept(self, dialog: QtWidgets.QDialog):
        if self.updateMapConfig() == 0:
            dialog.accept()
        else:
            return

    def clearBattleSetup(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Master clear of the class.

        """
        self.resetMapConfig()
        self.currentShip.clear()
        self.currentTurDict.clear()
        self.allShips.clear()
        self.radioButtonsEnabled = False
        self.shipCounter = 0
        self.currentShipKey = 0
        self.fleetCost = 0
