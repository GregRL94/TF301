# -*- coding: utf-8 -*-

"""
    File name: TaskForce301.py
    Author: Grégory LARGANGE
    Date created: 07/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 17/11/2021
    Python version: 3.8.1
"""

import sys
from os import path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMessageBox

from library import MainClock, Mapping, InGameData
from library.displays import GameDisplay, InteractiveList
from library.Ship import Ship
from library.dialogs import BattleSetup, InGameMenus, dialogsUtils
from library.controllers import AI
from library.controllers.game_controller import GameController


class Ui_TSKF301MainWindow(object):
    def setupUi(self, TSKF301MainWindow):
        TSKF301MainWindow.setObjectName("TSKF301MainWindow")
        TSKF301MainWindow.resize(1280, 960)
        self.centralwidget = QtWidgets.QWidget(TSKF301MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(2)
        self.gameScene = GameDisplay.GameScene(self.centralwidget)
        self.gameView = GameDisplay.GameView(self.gameScene)
        self.gameView.setObjectName("gameView")
        self.gameScene.attachedGView = self.gameView
        self.gridLayout.addWidget(self.gameView, 0, 1, 1, 1)
        self.main_buttons_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_buttons_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_buttons_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_buttons_frame.setObjectName("main_buttons_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_buttons_frame)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("mainButtonsVLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)
        self.newGame_but = QtWidgets.QPushButton(self.main_buttons_frame)
        self.newGame_but.setObjectName("newGame_but")
        self.newGame_but.setText("New Game")
        self.verticalLayout.addWidget(self.newGame_but)
        self.options_but = QtWidgets.QPushButton(self.main_buttons_frame)
        self.options_but.setObjectName("options_but")
        self.options_but.setText("Options")
        self.verticalLayout.addWidget(self.options_but)
        self.exit_but = QtWidgets.QPushButton(self.main_buttons_frame)
        self.exit_but.setObjectName("exit_but")
        self.exit_but.setText("Exit")
        self.verticalLayout.addWidget(self.exit_but)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.main_buttons_frame, 0, 0, 1, 1)
        self.current_ship_frame = QtWidgets.QFrame(self.centralwidget)
        self.current_ship_frame.setMinimumSize(QtCore.QSize(900, 135))
        self.current_ship_frame.setMaximumSize(QtCore.QSize(16777215, 135))
        self.current_ship_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.current_ship_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.current_ship_frame.setObjectName("current_ship_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.current_ship_frame)
        self.verticalLayout_3.setContentsMargins(-1, 9, -1, 9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ship_hp_h_lyt = QtWidgets.QHBoxLayout()
        self.ship_hp_h_lyt.setObjectName("ship_hp_h_lyt")
        self.ship_type_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.ship_type_lbl.setObjectName("ship_type_lbl")
        self.ship_hp_h_lyt.addWidget(self.ship_type_lbl)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.ship_hp_h_lyt.addItem(spacerItem2)
        self.ship_name_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.ship_name_lbl.setObjectName("ship_name_lbl")
        self.ship_hp_h_lyt.addWidget(self.ship_name_lbl)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.ship_hp_h_lyt.addItem(spacerItem3)
        self.hp_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.hp_lbl.setObjectName("hp_lbl")
        self.hp_lbl.setText("HP:")
        self.ship_hp_h_lyt.addWidget(self.hp_lbl)
        self.hp_progress_bar = QtWidgets.QProgressBar(self.current_ship_frame)
        self.hp_progress_bar.setProperty("value", 24)
        self.hp_progress_bar.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.hp_progress_bar.setObjectName("hp_progress_bar")
        self.ship_hp_h_lyt.addWidget(self.hp_progress_bar)
        self.verticalLayout_3.addLayout(self.ship_hp_h_lyt)
        self.displays_h_lyt = QtWidgets.QHBoxLayout()
        self.displays_h_lyt.setObjectName("displays_h_lyt")
        self.gen_stats_v_lyt = QtWidgets.QVBoxLayout()
        self.gen_stats_v_lyt.setObjectName("gen_stats_v_lyt")
        self.stats_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.stats_lbl.setObjectName("stats_lbl")
        self.stats_lbl.setText("STATS")
        self.gen_stats_v_lyt.addWidget(self.stats_lbl)
        self.all_stats_v_lyt = QtWidgets.QVBoxLayout()
        self.all_stats_v_lyt.setObjectName("all_stats_v_lyt")
        self.armor_lyt = QtWidgets.QHBoxLayout()
        self.armor_lyt.setObjectName("armor_lyt")
        self.armor_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.armor_lbl.setObjectName("armor_lbl")
        self.armor_lbl.setText("Armor")
        self.armor_lyt.addWidget(self.armor_lbl)
        self.armor_value_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.armor_value_lbl.setObjectName("armor_value_lbl")
        self.armor_lyt.addWidget(self.armor_value_lbl)
        self.all_stats_v_lyt.addLayout(self.armor_lyt)
        self.g_range_lyt = QtWidgets.QHBoxLayout()
        self.g_range_lyt.setObjectName("g_range_lyt")
        self.gun_range_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.gun_range_lbl.setObjectName("gun_range_lbl")
        self.gun_range_lbl.setText("Guns Range")
        self.g_range_lyt.addWidget(self.gun_range_lbl)
        self.gun_range_value_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.gun_range_value_lbl.setObjectName("gun_range_value_lbl")
        self.g_range_lyt.addWidget(self.gun_range_value_lbl)
        self.all_stats_v_lyt.addLayout(self.g_range_lyt)
        self.accuracy_lyt = QtWidgets.QHBoxLayout()
        self.accuracy_lyt.setObjectName("accuracy_lyt")
        self.accuracy_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.accuracy_lbl.setObjectName("accuracy_lbl")
        self.accuracy_lbl.setText("Accuracy")
        self.accuracy_lyt.addWidget(self.accuracy_lbl)
        self.accuracy_value_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.accuracy_value_lbl.setObjectName("accuracy_value_lbl")
        self.accuracy_lyt.addWidget(self.accuracy_value_lbl)
        self.all_stats_v_lyt.addLayout(self.accuracy_lyt)
        self.m_d_range_lyt = QtWidgets.QHBoxLayout()
        self.m_d_range_lyt.setObjectName("m_d_range_lyt")
        self.max_det_range_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.max_det_range_lbl.setObjectName("max_det_range_lbl")
        self.max_det_range_lbl.setText("Max. Detection Range")
        self.m_d_range_lyt.addWidget(self.max_det_range_lbl)
        self.max_det_range_value_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.max_det_range_value_lbl.setObjectName("max_det_range_value_lbl")
        self.m_d_range_lyt.addWidget(self.max_det_range_value_lbl)
        self.all_stats_v_lyt.addLayout(self.m_d_range_lyt)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.all_stats_v_lyt.addItem(spacerItem4)
        self.gen_stats_v_lyt.addLayout(self.all_stats_v_lyt)
        self.displays_h_lyt.addLayout(self.gen_stats_v_lyt)
        self.eng_policy_v_lyt = QtWidgets.QVBoxLayout()
        self.eng_policy_v_lyt.setObjectName("eng_policy_v_lyt")
        self.eng_policy_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.eng_policy_lbl.setObjectName("eng_policy_lbl")
        self.eng_policy_lbl.setText("ENGAGEMENT POLICY")
        self.eng_policy_v_lyt.addWidget(self.eng_policy_lbl)
        self.choices_h_lyt = QtWidgets.QHBoxLayout()
        self.choices_h_lyt.setObjectName("choices_h_lyt")
        self.auto_radio_but = QtWidgets.QRadioButton(self.current_ship_frame)
        self.auto_radio_but.setObjectName("auto_radio_but")
        self.auto_radio_but.setText("AUTO")
        self.choices_h_lyt.addWidget(self.auto_radio_but)
        self.distance_v_lyt = QtWidgets.QVBoxLayout()
        self.distance_v_lyt.setSpacing(6)
        self.distance_v_lyt.setObjectName("distance_v_lyt")
        self.distance_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.distance_lbl.setObjectName("distance_lbl")
        self.distance_lbl.setText("Engagement Distance")
        self.distance_v_lyt.addWidget(self.distance_lbl)
        self.long_range_radio_but = QtWidgets.QRadioButton(self.current_ship_frame)
        self.long_range_radio_but.setObjectName("long_range_radio_but")
        self.long_range_radio_but.setText("Long Range")
        self.distance_v_lyt.addWidget(self.long_range_radio_but)
        self.med_range_radio_but = QtWidgets.QRadioButton(self.current_ship_frame)
        self.med_range_radio_but.setObjectName("med_range_radio_but")
        self.med_range_radio_but.setText("Medium Range")
        self.distance_v_lyt.addWidget(self.med_range_radio_but)
        self.short_range_radio_but = QtWidgets.QRadioButton(self.current_ship_frame)
        self.short_range_radio_but.setObjectName("short_range_radio_but")
        self.short_range_radio_but.setText("Short Range")
        self.distance_v_lyt.addWidget(self.short_range_radio_but)
        self.choices_h_lyt.addLayout(self.distance_v_lyt)
        self.shot_type_v_lyt = QtWidgets.QVBoxLayout()
        self.shot_type_v_lyt.setObjectName("shot_type_v_lyt")
        self.shot_type_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.shot_type_lbl.setObjectName("shot_type_lbl")
        self.shot_type_lbl.setText("Shot Type")
        self.shot_type_v_lyt.addWidget(self.shot_type_lbl)
        self.ap_radio_but = QtWidgets.QRadioButton(self.current_ship_frame)
        self.ap_radio_but.setObjectName("ap_radio_but")
        self.ap_radio_but.setText("AP")
        self.shot_type_v_lyt.addWidget(self.ap_radio_but)
        self.he_radio_but = QtWidgets.QRadioButton(self.current_ship_frame)
        self.he_radio_but.setObjectName("he_radio_but")
        self.he_radio_but.setText("HE")
        self.shot_type_v_lyt.addWidget(self.he_radio_but)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.shot_type_v_lyt.addItem(spacerItem5)
        self.choices_h_lyt.addLayout(self.shot_type_v_lyt)
        self.eng_policy_v_lyt.addLayout(self.choices_h_lyt)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.eng_policy_v_lyt.addItem(spacerItem6)
        self.displays_h_lyt.addLayout(self.eng_policy_v_lyt)
        self.components_v_lyt = QtWidgets.QVBoxLayout()
        self.components_v_lyt.setObjectName("components_v_lyt")
        self.components_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.components_lbl.setObjectName("components_lbl")
        self.components_lbl.setText("COMPONENTS")
        self.components_v_lyt.addWidget(self.components_lbl)
        spacerItem7 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.components_v_lyt.addItem(spacerItem7)
        self.sub_comp_h_lyt = QtWidgets.QHBoxLayout()
        self.sub_comp_h_lyt.setObjectName("sub_comp_h_lyt")
        self.bridge_h_lyt = QtWidgets.QHBoxLayout()
        self.bridge_h_lyt.setObjectName("bridge_h_lyt")
        self.bridge_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.bridge_lbl.setObjectName("bridge_lbl")
        self.bridge_lbl.setText("BRIDGE:")
        self.bridge_h_lyt.addWidget(self.bridge_lbl)
        self.bridge_state_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.bridge_state_lbl.setObjectName("bridge_state_lbl")
        self.bridge_state_lbl.setText("OK")
        self.bridge_h_lyt.addWidget(self.bridge_state_lbl)
        self.sub_comp_h_lyt.addLayout(self.bridge_h_lyt)
        self.engine_h_lyt = QtWidgets.QHBoxLayout()
        self.engine_h_lyt.setObjectName("engine_h_lyt")
        self.engine_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.engine_lbl.setObjectName("engine_lbl")
        self.engine_lbl.setText("ENGINE:")
        self.engine_h_lyt.addWidget(self.engine_lbl)
        self.engine_state_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.engine_state_lbl.setObjectName("engine_state_lbl")
        self.engine_state_lbl.setText("OK")
        self.engine_h_lyt.addWidget(self.engine_state_lbl)
        self.sub_comp_h_lyt.addLayout(self.engine_h_lyt)
        self.radar_h_lyt = QtWidgets.QHBoxLayout()
        self.radar_h_lyt.setObjectName("radar_h_lyt")
        self.radar_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.radar_lbl.setObjectName("radar_lbl")
        self.radar_lbl.setText("RADAR:")
        self.radar_h_lyt.addWidget(self.radar_lbl)
        self.radar_state_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.radar_state_lbl.setObjectName("radar_state_lbl")
        self.radar_state_lbl.setText("OK")
        self.radar_h_lyt.addWidget(self.radar_state_lbl)
        self.sub_comp_h_lyt.addLayout(self.radar_h_lyt)
        self.fires_h_lyt = QtWidgets.QHBoxLayout()
        self.fires_h_lyt.setObjectName("fires_h_lyt")
        self.fires_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.fires_lbl.setObjectName("fires_lbl")
        self.fires_lbl.setText("FIRES:")
        self.fires_h_lyt.addWidget(self.fires_lbl)
        self.nb_fire_lbl = QtWidgets.QLabel(self.current_ship_frame)
        self.nb_fire_lbl.setObjectName("nb_fire_lbl")
        self.nb_fire_lbl.setText("0")
        self.fires_h_lyt.addWidget(self.nb_fire_lbl)
        self.sub_comp_h_lyt.addLayout(self.fires_h_lyt)
        self.components_v_lyt.addLayout(self.sub_comp_h_lyt)
        self.repair_but = QtWidgets.QPushButton(self.current_ship_frame)
        self.repair_but.setObjectName("repair_but")
        self.repair_but.setText("REPAIR")
        self.components_v_lyt.addWidget(self.repair_but)
        spacerItem8 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.components_v_lyt.addItem(spacerItem8)
        self.displays_h_lyt.addLayout(self.components_v_lyt)
        self.verticalLayout_3.addLayout(self.displays_h_lyt)
        self.gridLayout.addWidget(self.current_ship_frame, 1, 1, 1, 1)
        self.gameScene.attachedShipStatsDisplay = self.current_ship_frame
        self.current_ship_frame.setVisible(False)
        TSKF301MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(TSKF301MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        self.menuGame = QtWidgets.QMenu(self.menubar)
        self.menuGame.setObjectName("menuGame")
        TSKF301MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(TSKF301MainWindow)
        self.statusbar.setObjectName("statusbar")
        TSKF301MainWindow.setStatusBar(self.statusbar)
        self.playerShipsDW = QtWidgets.QDockWidget(TSKF301MainWindow)
        self.playerShipsDW.setObjectName("playerShipsDW")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.shipsListView = InteractiveList.InteractiveListView(
            False, self.dockWidgetContents
        )
        self.shipsListView.setObjectName("shipsListView")
        self.shipsListView.isForBattleSetup = False
        self.shipsListView.attachedObject = self.gameScene
        self.gameScene.attachedLView = self.shipsListView
        self.gridLayout_2.addWidget(self.shipsListView, 0, 0, 1, 1)
        self.playerShipsDW.setWidget(self.dockWidgetContents)
        self.playerShipsDW.setVisible(False)
        TSKF301MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.playerShipsDW)
        self.actionInBattlePause = QtWidgets.QAction(TSKF301MainWindow)
        self.actionInBattlePause.setObjectName("actionInBattlePause")
        self.actionEscapePause = QtWidgets.QAction(TSKF301MainWindow)
        self.actionEscapePause.setObjectName("actionInBattlePause")
        self.menuGame.addAction(self.actionInBattlePause)
        self.menuGame.addAction(self.actionEscapePause)
        self.menubar.addAction(self.menuGame.menuAction())

        self.retranslateUi(TSKF301MainWindow)
        QtCore.QMetaObject.connectSlotsByName(TSKF301MainWindow)

        self.newGame_but.clicked.connect(self.createBattle)
        self.exit_but.clicked.connect(self.exitGame)
        self.actionInBattlePause.triggered.connect(self.inBattlePause)
        self.actionEscapePause.triggered.connect(self.escapePause)

    def retranslateUi(self, TSKF301MainWindow):
        _translate = QtCore.QCoreApplication.translate
        TSKF301MainWindow.setWindowTitle(
            _translate("TSKF301MainWindow", "TSKF301MainWindow")
        )
        self.menuGame.setTitle(_translate("TSKF301MainWindow", "Game"))
        self.playerShipsDW.setWindowTitle(_translate("TSKF301MainWindow", "SHIPS"))
        self.actionInBattlePause.setText(
            _translate("TSKF301MainWindow", "In Game Pause")
        )
        self.actionInBattlePause.setShortcut(_translate("TSKF301MainWindow", "Space"))
        self.actionEscapePause.setText(_translate("TSKF301MainWindow", "Pause"))
        self.actionEscapePause.setShortcut(_translate("TSKF301MainWindow", "Escape"))

    def initData(self):
        self.mainClock = None
        self.mapGen = None
        self.rComs = None
        self._game_controller = None
        self.inBattle = False
        self.battleState = False

    def debugDisp(self, mapResolution, gridOn=True, penalties=True):
        if gridOn:
            self.gameScene.dispGrid(mapResolution)
        if penalties:
            _penaltyMap = self.mapGen.getPenaltyMap()
            self.gameScene.dispPenalties(_penaltyMap, mapResolution)

    def newGame(
        self,
        playableArea: int,
        mapExtension: int,
        mapResolution: int,
        mapObstruction: float,
        obsParameters: list,
    ):
        self.gameScene.setSceneRect(
            0,
            0,
            int(playableArea + 2 * mapExtension),
            int(playableArea + 2 * mapExtension),
        )
        self.gameScene.setInnerMap(mapExtension, playableArea)
        self.gameView.fitInView(
            QtCore.QRectF(
                mapExtension,
                mapExtension,
                playableArea + mapExtension,
                playableArea + mapExtension,
            ),
            Qt.KeepAspectRatio,
        )
        self.mapGen = Mapping.MapGenerator(
            self.gameScene.width(), self.gameScene.height(), mapResolution
        )
        self.mapGen.setMapParameters(mapObstruction, obsParameters)
        self.gameScene.displayMap(self.mapGen.generateMap())
        self.debugDisp(mapResolution, False, False)

        self.rComs = InGameData.RadioCommunications(self.mainClock, self.gameScene)

    def spawnShips(
        self,
        mapSize: int,
        mapExtension: int,
        distBLines: int,
        playerShipsConfigs: list,
        ennemyShipsConfigs=None,
    ):
        ## GENERAL VARS ##
        a_spawnXOffset = mapExtension + 1000
        e_spawnXOffset = mapExtension + mapSize - 1500
        spawnYCenter = mapSize // 2
        a_nbBBAndCA = a_nbDD = a_nbPT = 0
        e_nbBBAndCA = e_nbDD = e_nbPT = 0
        ai_fleet = []
        ##################

        ## SPAWN ROUTINE FOR PLAYER ##
        # Count number of each ship type
        for ship in playerShipsConfigs:
            if ship["naming"]["_type"] == "BB" or ship["naming"]["_type"] == "CA":
                a_nbBBAndCA += 1
            elif ship["naming"]["_type"] == "DD":
                a_nbDD += 1
            elif ship["naming"]["_type"] == "PT":
                a_nbPT += 1

        # Determine ally pos according to number of each ship type
        allySpawnPos = [
            QPoint(a_spawnXOffset, spawnYCenter - (a_nbBBAndCA // 2) * 1000),
            QPoint(a_spawnXOffset + distBLines, spawnYCenter - (a_nbDD // 2) * 1000),
            QPoint(
                a_spawnXOffset + 2 * distBLines, spawnYCenter - (a_nbPT // 2) * 1000
            ),
        ]

        # Spawn routine
        for i, playerShipConfig in enumerate(playerShipsConfigs):
            if playerShipConfig["naming"]["_type"] == "BB":
                spawnPos = allySpawnPos[0]
                # Checks if space is free to spawn the ship
                while self.gameScene.isFreeSpace(spawnPos) is False:
                    allySpawnPos[0].setY(allySpawnPos[0].y() + 1000)
                    spawnPos = allySpawnPos[0]
                currentShip = Ship._battleShip(
                    self.mainClock,
                    self.gameScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    "ALLY",
                    playerShipConfig,
                    spawnPos,
                )
                allySpawnPos[0].setY(allySpawnPos[0].y() + 1000)

            elif playerShipConfig["naming"]["_type"] == "CA":
                spawnPos = allySpawnPos[0]
                # Checks if space is free to spawn the ship
                while self.gameScene.isFreeSpace(spawnPos) is False:
                    allySpawnPos[0].setY(allySpawnPos[0].y() + 1000)
                    spawnPos = allySpawnPos[0]
                currentShip = Ship.cruiser(
                    self.mainClock,
                    self.gameScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    "ALLY",
                    playerShipConfig,
                    spawnPos,
                )
                allySpawnPos[0].setY(allySpawnPos[0].y() + 1000)

            elif playerShipConfig["naming"]["_type"] == "DD":
                spawnPos = allySpawnPos[1]
                # Checks if space is free to spawn the ship
                while self.gameScene.isFreeSpace(spawnPos) is False:
                    allySpawnPos[1].setY(allySpawnPos[1].y() + 1000)
                    spawnPos = allySpawnPos[1]
                currentShip = Ship.destroyer(
                    self.mainClock,
                    self.gameScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    "ALLY",
                    playerShipConfig,
                    spawnPos,
                )
                allySpawnPos[1].setY(allySpawnPos[1].y() + 1000)

            elif playerShipConfig["naming"]["_type"] == "PT":
                spawnPos = allySpawnPos[2]
                # Checks if space is free to spawn the ship
                while self.gameScene.isFreeSpace(spawnPos) is False:
                    allySpawnPos[2].setY(allySpawnPos[2].y() + 1000)
                    spawnPos = allySpawnPos[2]
                currentShip = Ship.corvette(
                    self.mainClock,
                    self.gameScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    "ALLY",
                    playerShipConfig,
                    spawnPos,
                )
                allySpawnPos[2].setY(allySpawnPos[2].y() + 1000)

            else:
                print("Could not Generate ship at:", i, "!")
            self.gameScene.addShip(currentShip)
            currentShip = None

        ## SPAWN ROUTINE FOR IA ##
        # Count number of each ship type
        if ennemyShipsConfigs:
            for ship in ennemyShipsConfigs:
                if ship["naming"]["_type"] == "BB" or ship["naming"]["_type"] == "CA":
                    e_nbBBAndCA += 1
                elif ship["naming"]["_type"] == "DD":
                    e_nbDD += 1
                elif ship["naming"]["_type"] == "PT":
                    e_nbPT += 1

            # Determine ally pos according to number of each ship type
            ennemySpawnPos = [
                QPoint(e_spawnXOffset, spawnYCenter - (e_nbBBAndCA // 2) * 1000),
                QPoint(
                    e_spawnXOffset - distBLines, spawnYCenter - (e_nbDD // 2) * 1000
                ),
                QPoint(
                    e_spawnXOffset - 2 * distBLines,
                    spawnYCenter - (e_nbPT // 2) * 1000,
                ),
            ]

            # Spawn routine
            for j, ennemyShipConfig in enumerate(ennemyShipsConfigs):
                if ennemyShipConfig["naming"]["_type"] == "BB":
                    spawnPos = ennemySpawnPos[0]
                    # Checks if space is free to spawn the ship
                    while self.gameScene.isFreeSpace(spawnPos, True) is False:
                        ennemySpawnPos[0].setY(ennemySpawnPos[0].y() + 1000)
                        spawnPos = ennemySpawnPos[0]
                    currentShip = Ship._battleShip(
                        self.mainClock,
                        self.gameScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        "ENNEMY",
                        ennemyShipConfig,
                        spawnPos,
                        180,
                    )
                    ai_fleet.append(currentShip)
                    ennemySpawnPos[0].setY(ennemySpawnPos[0].y() + 1000)

                elif ennemyShipConfig["naming"]["_type"] == "CA":
                    spawnPos = ennemySpawnPos[0]
                    # Checks if space is free to spawn the ship
                    while self.gameScene.isFreeSpace(spawnPos, True) is False:
                        ennemySpawnPos[0].setY(ennemySpawnPos[0].y() + 1000)
                        spawnPos = ennemySpawnPos[0]
                    currentShip = Ship.cruiser(
                        self.mainClock,
                        self.gameScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        "ENNEMY",
                        ennemyShipConfig,
                        spawnPos,
                        180,
                    )
                    ai_fleet.append(currentShip)
                    ennemySpawnPos[0].setY(ennemySpawnPos[0].y() + 1000)

                elif ennemyShipConfig["naming"]["_type"] == "DD":
                    spawnPos = ennemySpawnPos[1]
                    # Checks if space is free to spawn the ship
                    while self.gameScene.isFreeSpace(spawnPos, True) is False:
                        ennemySpawnPos[1].setY(ennemySpawnPos[1].y() + 1000)
                        spawnPos = ennemySpawnPos[1]
                    currentShip = Ship.destroyer(
                        self.mainClock,
                        self.gameScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        "ENNEMY",
                        ennemyShipConfig,
                        spawnPos,
                        180,
                    )
                    ai_fleet.append(currentShip)
                    ennemySpawnPos[1].setY(ennemySpawnPos[1].y() + 1000)

                elif ennemyShipConfig["naming"]["_type"] == "PT":
                    spawnPos = ennemySpawnPos[2]
                    # Checks if space is free to spawn the ship
                    while self.gameScene.isFreeSpace(spawnPos, True) is False:
                        ennemySpawnPos[2].setY(ennemySpawnPos[2].y() + 1000)
                        spawnPos = ennemySpawnPos[2]
                    currentShip = Ship.corvette(
                        self.mainClock,
                        self.gameScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        "ENNEMY",
                        ennemyShipConfig,
                        spawnPos,
                        180,
                    )
                    ai_fleet.append(currentShip)
                    ennemySpawnPos[2].setY(ennemySpawnPos[2].y() + 1000)

                else:
                    print("Could not Generate ship at", j, "!")
                self.gameScene.addShip(currentShip)
                currentShip = None

        self.rComs.updateShipLists()
        return ai_fleet

    def createBattle(self):
        self.mainClock = MainClock.MainClock(25)  # ms
        self._game_controller = GameController(self)
        b_setup = BattleSetup.BattleSetup()
        self.gameScene.attachedGController = self._game_controller
        result = b_setup.battleSetupUI()
        if result:
            result2 = b_setup.createFleetUi()
            if result2:
                mapConfig = b_setup.currentMapConfig
                playerFleet = b_setup.allShips
                ennemyFleet = self._game_controller.generate_ai_fleet(
                    mapConfig["funds"]
                )
                ## DEBUG PRINTS ##
                # print("MAP:")
                # for key, value in mapConfig.items():
                #     print(key, "\n", value)
                # print("")
                # print("")

                # print("ALL SHIPS IN FLEET")
                # for shipKey, ship in playerFleet.items():
                #     print(shipKey)
                #     for statKey, statValue in ship.items():
                #         print(statKey, "\n", statValue)
                #     print("")
                ###################
                self.main_buttons_frame.setVisible(False)
                self.playerShipsDW.setVisible(True)
                self.newGame(
                    mapConfig["size"],
                    mapConfig["extension"],
                    mapConfig["resolution"],
                    mapConfig["obstruction"],
                    mapConfig["obstaclesSetup"],
                )
                ai_fleet = self.spawnShips(
                    mapConfig["size"],
                    mapConfig["extension"],
                    1500,
                    playerFleet.values(),
                    ennemyFleet,
                )
                ai = AI.FleetAI(
                    self.mainClock,
                    self.gameScene,
                    ai_fleet,
                    mapConfig["size"],
                    mapConfig["size"],
                )
                self.inBattle = True
                self.battleState = False

    def inBattlePause(self):
        if self.inBattle:
            if self.battleState:
                self.mainClock.stopClock()
                self.battleState = False
            else:
                self.mainClock.startClock()
                self.battleState = True

    def escapePause(self):
        battleStateAtPause = self.battleState

        if self.inBattle:
            if battleStateAtPause:
                self.mainClock.stopClock()
                self.battleState = False

            pauseMenu = InGameMenus.PauseMenu()
            result = pauseMenu.pauseMenuUI()
            if result[1] == 0:
                print("RESUMING BATTLE")
            elif result[1] == 1:
                print("OPENING OPTION MENU")
            elif result[1] == 2:
                self.exitBattle()

            if battleStateAtPause:
                try:
                    self.mainClock.startClock()
                    self.battleState = True
                except AttributeError:
                    pass

    def exitBattle(self):
        result = dialogsUtils.OkCancelDialog("Leave battle", 1, "Admit defeat ?")
        if result == QMessageBox.Ok:
            self.mainClock.stopClock()
            self.battleState = False
            self.gameScene.clearGameScene()
            self.gameView.resetZoom()
            self.shipsListView.clearList()
            self.current_ship_frame.setVisible(False)
            self.initData()
            self.main_buttons_frame.setVisible(True)
            self.playerShipsDW.setVisible(False)
            self.gameView.fitInView(self.gameScene.sceneRect(), Qt.KeepAspectRatio)

    def exitGame(self):
        result = dialogsUtils.OkCancelDialog(
            "Quit Task Force 301?", 1, "Are you sure you want to quit Task Force 301 ?"
        )
        if result == QMessageBox.Ok:
            sys.exit()
        else:
            return


if __name__ == "__main__":
    if not QtWidgets.QApplication.instance():
        # Create a new QApplication
        app = QtWidgets.QApplication(sys.argv)
    else:
        # A QApplication already exists due to a bad previous exit
        # Get it
        app = QtWidgets.QApplication.instance()
    TSKF301MainWindow = QtWidgets.QMainWindow()
    ui = Ui_TSKF301MainWindow()
    ui.setupUi(TSKF301MainWindow)
    ui.initData()
    TSKF301MainWindow.show()
    sys.exit(app.exec_())
