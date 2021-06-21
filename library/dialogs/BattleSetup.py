# -*- coding: utf-8 -*-

"""
    File name: BattleSetup.py
    Author: Grégory LARGANGE
    Date created: 10/06/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 10/06/2021
    Python version: 3.8.1
"""


from PyQt5 import QtCore, QtGui, QtWidgets


class BattleSetup:
    def createFleetUi(self):
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

        cur_fleet_cost_lbl = QtWidgets.QLabel(verticalLayoutWidget)
        cur_fleet_cost_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        cur_fleet_cost_lbl.setObjectName("cur_fleet_cost_lbl")
        cur_fleet_cost_lbl.setText("COST / MAX COST")
        horizontalLayout_7.addWidget(cur_fleet_cost_lbl)

        fleet_lyt.addLayout(horizontalLayout_7)
        listView = QtWidgets.QListView(verticalLayoutWidget)
        listView.setObjectName("listView")
        fleet_lyt.addWidget(listView)
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

        ff_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        ff_but.setObjectName("ff_but")
        ff_but.setText("FRIGATE")
        type_buttons_lyt.addWidget(ff_but)

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
        gun_tech_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        gun_tech_lbl.setFont(font)
        gun_tech_lbl.setObjectName("gun_tech_lbl")
        gun_tech_lbl.setText("Gun tech")
        gridLayout.addWidget(gun_tech_lbl, 0, 0, 1, 1)

        rdr_tech_0 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        rdr_tech_0.setObjectName("rdr_tech_0")
        rdr_tech_0.setText("Mk I")
        gridLayout.addWidget(rdr_tech_0, 2, 1, 1, 1)

        fc_tech_0 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        fc_tech_0.setObjectName("fc_tech_0")
        fc_tech_0.setText("Mk I")
        gridLayout.addWidget(fc_tech_0, 1, 1, 1, 1)

        gun_tech_1 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        gun_tech_1.setObjectName("gun_tech_1")
        gun_tech_1.setText("Mk II")
        gridLayout.addWidget(gun_tech_1, 0, 2, 1, 1)

        rdr_tech_1 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        rdr_tech_1.setObjectName("rdr_tech_1")
        rdr_tech_1.setText("Mk II")
        gridLayout.addWidget(rdr_tech_1, 2, 2, 1, 1)

        fc_tech_1 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        fc_tech_1.setObjectName("fc_tech_1")
        fc_tech_1.setText("Mk II")
        gridLayout.addWidget(fc_tech_1, 1, 2, 1, 1)

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

        gun_tech_0 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        gun_tech_0.setObjectName("gun_tech_0")
        gun_tech_0.setText("Mk I")
        gridLayout.addWidget(gun_tech_0, 0, 1, 1, 1)

        gun_tech_2 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        gun_tech_2.setObjectName("gun_tech_2")
        gun_tech_2.setText("Mk III")
        gridLayout.addWidget(gun_tech_2, 0, 3, 1, 1)

        fc_tech_2 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        fc_tech_2.setObjectName("fc_tech_2")
        fc_tech_2.setText("Mk III")
        gridLayout.addWidget(fc_tech_2, 1, 3, 1, 1)

        rdr_tech_2 = QtWidgets.QRadioButton(verticalLayoutWidget_2)
        rdr_tech_2.setObjectName("rdr_tech_2")
        rdr_tech_2.setText("Mk III")
        gridLayout.addWidget(rdr_tech_2, 2, 3, 1, 1)

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
        type_label.setText("Type:")
        type_lyt.addWidget(type_label)

        ship_type_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_type_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_type_label.setObjectName("ship_type_label")
        ship_type_label.setText("TextLabel")
        type_lyt.addWidget(ship_type_label)

        ship_stats_lyt_3.addLayout(type_lyt)
        name_lyt = QtWidgets.QHBoxLayout()
        name_lyt.setObjectName("name_lyt")
        name_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        name_label.setObjectName("name_label")
        name_label.setText("Name:")
        name_lyt.addWidget(name_label)

        ship_name_label = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_name_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_name_label.setObjectName("ship_name_label")
        ship_name_label.setText("TextLabel")
        name_lyt.addWidget(ship_name_label)

        ship_stats_lyt_3.addLayout(name_lyt)
        len_lyt = QtWidgets.QHBoxLayout()
        len_lyt.setObjectName("len_lyt")
        length_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        length_lbl.setObjectName("length_lbl")
        length_lbl.setText("Length:")
        len_lyt.addWidget(length_lbl)

        ship_length_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_length_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_length_lbl.setObjectName("ship_length_lbl")
        ship_length_lbl.setText("TextLabel")
        len_lyt.addWidget(ship_length_lbl)

        ship_stats_lyt_3.addLayout(len_lyt)
        widht_layout = QtWidgets.QHBoxLayout()
        widht_layout.setObjectName("widht_layout")

        width_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        width_lbl.setObjectName("width_lbl")
        width_lbl.setText("Width:")
        widht_layout.addWidget(width_lbl)

        ship_width_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_width_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_width_lbl.setObjectName("ship_width_lbl")
        ship_width_lbl.setText("TextLabel")
        widht_layout.addWidget(ship_width_lbl)

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

        ship_w_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_w_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_w_lbl.setObjectName("ship_w_lbl")
        ship_w_lbl.setText("TextLabel")
        main_guns_lyt.addWidget(ship_w_lbl)

        ship_stats_lyt_3.addLayout(main_guns_lyt)
        acc_lyt = QtWidgets.QHBoxLayout()
        acc_lyt.setObjectName("acc_lyt")

        acc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        acc_lbl.setObjectName("acc_lbl")
        acc_lbl.setText("Guns accuracy:")
        acc_lyt.addWidget(acc_lbl)

        ship_acc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_acc_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_acc_lbl.setObjectName("ship_acc_lbl")
        ship_acc_lbl.setText("TextLabel")
        acc_lyt.addWidget(ship_acc_lbl)

        ship_stats_lyt_3.addLayout(acc_lyt)
        fc_lyt = QtWidgets.QHBoxLayout()
        fc_lyt.setObjectName("fc_lyt")

        fc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        fc_lbl.setObjectName("fc_lbl")
        fc_lbl.setText("Fire control error:")
        fc_lyt.addWidget(fc_lbl)

        ship_fc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_fc_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_fc_lbl.setObjectName("ship_fc_lbl")
        ship_fc_lbl.setText("TextLabel")
        fc_lyt.addWidget(ship_fc_lbl)

        ship_stats_lyt_3.addLayout(fc_lyt)
        err_reduc_lyt = QtWidgets.QHBoxLayout()
        err_reduc_lyt.setObjectName("err_reduc_lyt")

        err_reduc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        err_reduc_lbl.setObjectName("err_reduc_lbl")
        err_reduc_lbl.setText("Error reduction rate:")
        err_reduc_lyt.addWidget(err_reduc_lbl)

        ship_errreduc_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_errreduc_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_errreduc_lbl.setObjectName("ship_errreduc_lbl")
        ship_errreduc_lbl.setText("TextLabel")
        err_reduc_lyt.addWidget(ship_errreduc_lbl)

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

        ship_max_hp_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_max_hp_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_max_hp_lbl.setObjectName("ship_max_hp_lbl")
        ship_max_hp_lbl.setText("TextLabel")
        hp_lyt.addWidget(ship_max_hp_lbl)

        hull_stats_lyt.addLayout(hp_lyt)
        armor_lyt = QtWidgets.QHBoxLayout()
        armor_lyt.setObjectName("armor_lyt")

        armor_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        armor_lbl.setObjectName("armor_lbl")
        armor_lbl.setText("Armor:")
        armor_lyt.addWidget(armor_lbl)

        ship_armor_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_armor_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_armor_lbl.setObjectName("ship_armor_lbl")
        ship_armor_lbl.setText("TextLabel")
        armor_lyt.addWidget(ship_armor_lbl)

        hull_stats_lyt.addLayout(armor_lyt)
        shield_lyt = QtWidgets.QHBoxLayout()
        shield_lyt.setObjectName("shield_lyt")

        shield_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        shield_lbl.setObjectName("shield_lbl")
        shield_lbl.setText("Shield:")
        shield_lyt.addWidget(shield_lbl)

        ship_shield_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_shield_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_shield_lbl.setObjectName("ship_shield_lbl")
        ship_shield_lbl.setText("TextLabel")
        shield_lyt.addWidget(ship_shield_lbl)

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

        ship_v_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_v_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_v_lbl.setObjectName("ship_v_lbl")
        ship_v_lbl.setText("TextLabel")
        speed_lyt.addWidget(ship_v_lbl)

        hull_stats_lyt.addLayout(speed_lyt)
        accel_lyt = QtWidgets.QHBoxLayout()
        accel_lyt.setObjectName("accel_lyt")

        accel_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        accel_lbl.setObjectName("accel_lbl")
        accel_lbl.setText("Acceleration:")
        accel_lyt.addWidget(accel_lbl)

        ship_accel_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_accel_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_accel_lbl.setObjectName("ship_accel_lbl")
        ship_accel_lbl.setText("TextLabel")
        accel_lyt.addWidget(ship_accel_lbl)

        hull_stats_lyt.addLayout(accel_lyt)
        t_rate_lyt = QtWidgets.QHBoxLayout()
        t_rate_lyt.setObjectName("t_rate_lyt")

        t_rate_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        t_rate_lbl.setObjectName("t_rate_lbl")
        t_rate_lbl.setText("Turn rate:")
        t_rate_lyt.addWidget(t_rate_lbl)

        ship_t_rate_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_t_rate_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_t_rate_lbl.setObjectName("ship_t_rate_lbl")
        ship_t_rate_lbl.setText("TextLabel")
        t_rate_lyt.addWidget(ship_t_rate_lbl)

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

        ship_vision_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_vision_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_vision_lbl.setObjectName("ship_vision_lbl")
        ship_vision_lbl.setText("TextLabel")
        vision_lyt.addWidget(ship_vision_lbl)

        hull_stats_lyt.addLayout(vision_lyt)
        concl_lyt = QtWidgets.QHBoxLayout()
        concl_lyt.setObjectName("concl_lyt")

        concl_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        concl_lbl.setObjectName("concl_lbl")
        concl_lbl.setText("Concealment:")
        concl_lyt.addWidget(concl_lbl)

        ship_concl_lbl = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_concl_lbl.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        ship_concl_lbl.setObjectName("ship_concl_lbl")
        ship_concl_lbl.setText("TextLabel")
        concl_lyt.addWidget(ship_concl_lbl)

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

        ship_cost = QtWidgets.QLabel(verticalLayoutWidget_2)
        ship_cost.setObjectName("ship_cost")
        ship_cost.setText("00000")
        clear_add_but_lyt.addWidget(ship_cost)

        spacerItem6 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        clear_add_but_lyt.addItem(spacerItem6)

        clear_ship_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        clear_ship_but.setObjectName("clear_ship_but")
        clear_ship_but.setText("Reset")
        clear_add_but_lyt.addWidget(clear_ship_but)

        add_ship_but = QtWidgets.QPushButton(verticalLayoutWidget_2)
        add_ship_but.setObjectName("add_ship_but")
        add_ship_but.setText("Add Ship")
        clear_add_but_lyt.addWidget(add_ship_but)

        ship_creator_lyt.addLayout(clear_add_but_lyt)

        battle_but.clicked.connect(fleet_setup.accept)
        QtCore.QMetaObject.connectSlotsByName(fleet_setup)

        return fleet_setup.exec()

    def battleSetupUI(self):
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
        points_cmbbox = QtWidgets.QComboBox(battle_setup)
        points_cmbbox.setObjectName("points_cmbbox")
        points_cmbbox.addItem("25 %")
        points_cmbbox.addItem("50 %")
        points_cmbbox.addItem("75 %")
        gridLayout.addWidget(points_cmbbox, 7, 1, 1, 1)

        difficulty_cmbbox = QtWidgets.QComboBox(battle_setup)
        difficulty_cmbbox.setObjectName("difficulty_cmbbox")
        difficulty_cmbbox.addItem("Easy")
        difficulty_cmbbox.addItem("Normal")
        difficulty_cmbbox.addItem("Hard")
        difficulty_cmbbox.addItem("Very Hard")
        gridLayout.addWidget(difficulty_cmbbox, 3, 1, 1, 1)

        map_size_lbl = QtWidgets.QLabel(battle_setup)
        map_size_lbl.setObjectName("map_size_lbl")
        map_size_lbl.setText("Map size:")
        gridLayout.addWidget(map_size_lbl, 1, 0, 1, 1)

        funds_cmbbox = QtWidgets.QComboBox(battle_setup)
        funds_cmbbox.setObjectName("funds_cmbbox")
        funds_cmbbox.addItem("Small")
        funds_cmbbox.addItem("Standard")
        funds_cmbbox.addItem("Large")
        funds_cmbbox.addItem("Custom")
        gridLayout.addWidget(funds_cmbbox, 4, 1, 1, 1)

        funds_lbl = QtWidgets.QLabel(battle_setup)
        funds_lbl.setObjectName("funds_lbl")
        funds_lbl.setText("Funds:")
        gridLayout.addWidget(funds_lbl, 4, 0, 1, 1)

        maps_comboBox = QtWidgets.QComboBox(battle_setup)
        maps_comboBox.setObjectName("maps_comboBox")
        maps_comboBox.addItem("Random")
        maps_comboBox.addItem("Map 1")
        maps_comboBox.addItem("Map 2")
        gridLayout.addWidget(maps_comboBox, 0, 1, 1, 1)

        difficulty_lbl = QtWidgets.QLabel(battle_setup)
        difficulty_lbl.setObjectName("difficulty_lbl")
        difficulty_lbl.setText("Difficulty:")
        gridLayout.addWidget(difficulty_lbl, 3, 0, 1, 1)

        v_cond_cmbbox = QtWidgets.QComboBox(battle_setup)
        v_cond_cmbbox.setObjectName("v_cond_cmbbox")
        v_cond_cmbbox.addItem("Annihilation")
        v_cond_cmbbox.addItem("Points")
        gridLayout.addWidget(v_cond_cmbbox, 6, 1, 1, 1)

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

        map_size_cmbbox = QtWidgets.QComboBox(battle_setup)
        map_size_cmbbox.setObjectName("map_size_cmbbox")
        map_size_cmbbox.addItem("Small")
        map_size_cmbbox.addItem("Medium")
        map_size_cmbbox.addItem("Large")
        gridLayout.addWidget(map_size_cmbbox, 1, 1, 1, 1)

        cstm_funds_l_edit = QtWidgets.QLineEdit(battle_setup)
        cstm_funds_l_edit.setObjectName("cstm_funds_l_edit")
        gridLayout.addWidget(cstm_funds_l_edit, 5, 1, 1, 1)

        mapObs_cmbbox = QtWidgets.QComboBox(battle_setup)
        mapObs_cmbbox.setObjectName("mapObs_cmbbox")
        mapObs_cmbbox.addItem("Open")
        mapObs_cmbbox.addItem("Light")
        mapObs_cmbbox.addItem("Medium")
        mapObs_cmbbox.addItem("Heavy")
        gridLayout.addWidget(mapObs_cmbbox, 2, 1, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        gridLayout.addItem(spacerItem1, 8, 1, 1, 1)

        ok_button.clicked.connect(battle_setup.accept)
        cancelButton.clicked.connect(battle_setup.reject)
        QtCore.QMetaObject.connectSlotsByName(battle_setup)

        return battle_setup.exec()

    def createFleetAccept(self, dialog):
        dialog.accept()

    def createFleetReject(self, dialog):
        dialog.reject()

    def battleSetupAccept(self, dialog):
        dialog.accept()

    def battleSetupReject(self, dialog):
        dialog.reject()
