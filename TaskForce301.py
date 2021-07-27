# -*- coding: utf-8 -*-

"""
    File name: TaskForce301.py
    Author: Grégory LARGANGE
    Date created: 07/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 13/07/2021
    Python version: 3.8.1
"""

import sys
import copy  #### testing
from os import path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMessageBox

from library import MainClock, Mapping, InGameData
from library.displays import GameDisplay
from library.Ship import Ship
from library.dialogs import BattleSetup, InGameMenus, dialogsUtils


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
        self.shipsListView = QtWidgets.QListView(self.dockWidgetContents)
        self.shipsListView.setObjectName("shipsListView")
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
        self.debugDisp(mapResolution, True, False)

        self.rComs = InGameData.RadioCommunications(self.mainClock, self.gameScene)

    def spawnShips(
        self,
        mapSize: int,
        mapExtension: int,
        distBLines: int,
        playerShipsConfigs: list,
        ennemyShipsConfigs=None,
    ):
        a_spawnXOffset = mapExtension + 1000
        e_spawnXOffset = mapExtension + mapSize - 1000
        spawnYCenter = mapSize // 2
        a_nbBBAndCA = a_nbFF = a_nbPT = 0
        e_nbBBAndCA = e_nbFF = e_nbPT = 0
        ######
        testConfig = None
        ######
        for ship in playerShipsConfigs:
            if ship["naming"]["_type"] == "BB" or ship["naming"]["_type"] == "CA":
                a_nbBBAndCA += 1
            elif ship["naming"]["_type"] == "FF":
                a_nbFF += 1
            elif ship["naming"]["_type"] == "PT":
                a_nbPT += 1

        allySpawnPos = [
            QPoint(a_spawnXOffset, spawnYCenter - (a_nbBBAndCA // 2) * 1000),
            QPoint(a_spawnXOffset + distBLines, spawnYCenter - (a_nbFF // 2) * 1000),
            QPoint(
                a_spawnXOffset + 2 * distBLines, spawnYCenter - (a_nbPT // 2) * 1000
            ),
        ]

        for i, playerShipConfig in enumerate(playerShipsConfigs):
            ######
            testConfig = copy.deepcopy(playerShipConfig)
            ######
            if playerShipConfig["naming"]["_type"] == "BB":
                spawnPos = allySpawnPos[0]
                currentShip = Ship._battleShip(
                    self.mainClock,
                    self.gameScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    spawnPos,
                    "ALLY",
                    playerShipConfig,
                )
                allySpawnPos[0].setY(allySpawnPos[0].y() + 1000)

            elif playerShipConfig["naming"]["_type"] == "CA":
                spawnPos = allySpawnPos[0]
                currentShip = Ship.cruiser(
                    self.mainClock,
                    self.gameScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    spawnPos,
                    "ALLY",
                    playerShipConfig,
                )
                allySpawnPos[0].setY(allySpawnPos[0].y() + 1000)

            elif playerShipConfig["naming"]["_type"] == "FF":
                spawnPos = allySpawnPos[1]
                currentShip = Ship.frigate(
                    self.mainClock,
                    self.gameScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    spawnPos,
                    "ALLY",
                    playerShipConfig,
                )
                allySpawnPos[1].setY(allySpawnPos[1].y() + 1000)

            elif playerShipConfig["naming"]["_type"] == "PT":
                spawnPos = allySpawnPos[2]
                currentShip = Ship.corvette(
                    self.mainClock,
                    self.gameScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    spawnPos,
                    "ALLY",
                    playerShipConfig,
                )
                allySpawnPos[2].setY(allySpawnPos[2].y() + 1000)

            else:
                print("Could not Generate ship at:", i, "!")
            self.gameScene.addShip(currentShip)
            currentShip = None

        if ennemyShipsConfigs:
            for ship in ennemyShipsConfigs:
                if ship["naming"]["_type"] == "BB" or ship["naming"]["_type"] == "CA":
                    e_nbBBAndCA += 1
                elif ship["naming"]["_type"] == "FF":
                    e_nbFF += 1
                elif ship["naming"]["_type"] == "PT":
                    e_nbPT += 1

            ennemySpawnPos = [
                QPoint(e_spawnXOffset, spawnYCenter - (e_nbBBAndCA // 2) * 1000),
                QPoint(
                    e_spawnXOffset - distBLines, spawnYCenter - (e_nbFF // 2) * 1000
                ),
                QPoint(
                    e_spawnXOffset - 2 * distBLines,
                    spawnYCenter - (e_nbPT // 2) * 1000,
                ),
            ]

            for j, ennemyShipConfig in enumerate(ennemyShipsConfigs):
                if ennemyShipConfig["naming"]["_type"] == "BB":
                    spawnPos = ennemySpawnPos[0]
                    currentShip = Ship._battleShip(
                        self.mainClock,
                        self.gameScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        spawnPos,
                        "ENNEMY",
                        ennemyShipConfig,
                    )
                    ennemySpawnPos[0].setY(ennemySpawnPos[0].y() + 1000)

                elif ennemyShipConfig["naming"]["_type"] == "CA":
                    spawnPos = ennemySpawnPos[0]
                    currentShip = Ship.cruiser(
                        self.mainClock,
                        self.gameScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        spawnPos,
                        "ENNEMY",
                        ennemyShipConfig,
                    )
                    ennemySpawnPos[0].setY(ennemySpawnPos[0].y() + 1000)

                elif ennemyShipConfig["naming"]["_type"] == "FF":
                    spawnPos = ennemySpawnPos[1]
                    currentShip = Ship.frigate(
                        self.mainClock,
                        self.gameScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        spawnPos,
                        "ENNEMY",
                        ennemyShipConfig,
                    )
                    ennemySpawnPos[1].setY(ennemySpawnPos[1].y() + 1000)

                elif ennemyShipConfig["naming"]["_type"] == "PT":
                    spawnPos = ennemySpawnPos[2]
                    currentShip = Ship.corvette(
                        self.mainClock,
                        self.gameScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        spawnPos,
                        "ENNEMY",
                        ennemyShipConfig,
                    )
                    ennemySpawnPos[2].setY(ennemySpawnPos[2].y() + 1000)

                else:
                    print("Could not Generate ship at", j, "!")
                self.gameScene.addShip(currentShip)
                currentShip = None

        ##### TBD #####
        currentShip = Ship._battleShip(
            self.mainClock,
            self.gameScene,
            self.mapGen.gameMap,
            self.mapGen.mapS,
            QPoint(15000, 15000),
            "ENNEMY",
            testConfig,
        )
        self.gameScene.addShip(currentShip)
        currentShip = None
        ################
        self.rComs.updateShipLists()

    def createBattle(self):
        self.mainClock = MainClock.MainClock(25)  # ms
        b_setup = BattleSetup.BattleSetup()
        result = b_setup.battleSetupUI()
        if result:
            result2 = b_setup.createFleetUi()
            if result2:
                mapConfig = b_setup.currentMapConfig
                playerFleet = b_setup.allShips
                print("MAP:")
                for key, value in mapConfig.items():
                    print(key, "\n", value)
                print("")
                print("")

                print("ALL SHIPS IN FLEET")
                for shipKey, ship in playerFleet.items():
                    print(shipKey)
                    for statKey, statValue in ship.items():
                        print(statKey, "\n", statValue)
                    print("")
                self.main_buttons_frame.setVisible(False)
                self.playerShipsDW.setVisible(True)
                self.newGame(
                    mapConfig["size"],
                    mapConfig["extension"],
                    mapConfig["resolution"],
                    mapConfig["obstruction"],
                    mapConfig["obstaclesSetup"],
                )
                self.spawnShips(
                    mapConfig["size"],
                    mapConfig["extension"],
                    1500,
                    playerFleet.values(),
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
