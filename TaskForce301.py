# -*- coding: utf-8 -*-

"""
    File name: TaskForce301.py
    Author: Grégory LARGANGE
    Date created: 07/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 07/07/2021
    Python version: 3.8.1
"""

import sys

from os import path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGraphicsView, QMessageBox

from library import MainClock, GameScene, Mapping, InGameData
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
        self.graphicsScene = GameScene.GameScene(self.centralwidget)
        self.graphicsView = QGraphicsView(self.graphicsScene)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsScene.attachedGView = self.graphicsView
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 1, 1)
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
        self.exit_but.clicked.connect(self.exitClicked)
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
        self.inBattle = False
        self.battleState = False

    def genRandomMap(self):
        genObs = self.mapGen.generateMap()
        self.graphicsScene.displayMap(genObs)

    def debugDisp(self, mapResolution, gridOn=True, penalties=True):
        if gridOn:
            self.graphicsScene.dispGrid(mapResolution)
        if penalties:
            _penaltyMap = self.mapGen.getPenaltyMap()
            self.graphicsScene.dispPenalties(_penaltyMap, mapResolution)

    def newGame(
        self,
        playableArea: int,
        mapExtension: int,
        mapResolution: int,
        mapObstruction: float,
        obsParameters: list,
    ):
        self.graphicsScene.setSceneRect(
            0,
            0,
            int(playableArea + 2 * mapExtension),
            int(playableArea + 2 * mapExtension),
        )
        self.graphicsScene.setInnerMap(mapExtension, playableArea)
        self.graphicsView.fitInView(
            QtCore.QRectF(
                mapExtension,
                mapExtension,
                playableArea + mapExtension,
                playableArea + mapExtension,
            ),
            Qt.KeepAspectRatio,
        )
        self.mapGen = Mapping.MapGenerator(
            self.graphicsScene.width(), self.graphicsScene.height(), mapResolution
        )
        self.mapGen.setMapParameters(mapObstruction, obsParameters)
        self.genRandomMap()
        self.debugDisp(mapResolution, True, False)

        self.rComs = InGameData.RadioCommunications(self.mainClock, self.graphicsScene)

    def newGameMap(self):
        self.graphicsScene.clearMap()
        self.mapGen.resetMap()
        self.genRandomMap()
        self.debugDisp(True, False)

    def spawnShips(self, playerShipsConfigs: list, ennemyShipsConfigs=None):
        allySpawnPos = QPointF(6000, 6000)
        ennemySpawnPos = QPointF(12000, 12000)

        for i, playerShipConfig in enumerate(playerShipsConfigs):
            if playerShipConfig["naming"]["_type"] == "BB":
                currentShip = Ship._battleShip(
                    self.mainClock,
                    self.graphicsScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    allySpawnPos,
                    "ALLY",
                    playerShipConfig,
                )
            elif playerShipConfig["naming"]["_type"] == "CA":
                currentShip = Ship.cruiser(
                    self.mainClock,
                    self.graphicsScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    allySpawnPos,
                    "ALLY",
                    playerShipConfig,
                )
            elif playerShipConfig["naming"]["_type"] == "FF":
                currentShip = Ship.frigate(
                    self.mainClock,
                    self.graphicsScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    allySpawnPos,
                    "ALLY",
                    playerShipConfig,
                )
            elif playerShipConfig["naming"]["_type"] == "PT":
                currentShip = Ship.corvette(
                    self.mainClock,
                    self.graphicsScene,
                    self.mapGen.gameMap,
                    self.mapGen.mapS,
                    allySpawnPos,
                    "ALLY",
                    playerShipConfig,
                )
            else:
                print("Could not Generate ship at", i, "!")
            self.graphicsScene.addShip(currentShip)
            currentShip = None
            allySpawnPos.setX(allySpawnPos.x() + 1000)
            allySpawnPos.setY(allySpawnPos.y() + 1000)

        if ennemyShipsConfigs:
            for j, ennemyShipConfig in enumerate(ennemyShipsConfigs):
                if ennemyShipConfig["naming"]["_type"] == "BB":
                    currentShip = Ship._battleShip(
                        self.mainClock,
                        self.graphicsScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        ennemySpawnPos,
                        "ENNEMY",
                        ennemyShipConfig,
                    )
                elif ennemyShipConfig["naming"]["_type"] == "CA":
                    currentShip = Ship.cruiser(
                        self.mainClock,
                        self.graphicsScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        ennemySpawnPos,
                        "ENNEMY",
                        ennemyShipConfig,
                    )
                elif ennemyShipConfig["naming"]["_type"] == "FF":
                    currentShip = Ship.frigate(
                        self.mainClock,
                        self.graphicsScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        ennemySpawnPos,
                        "ENNEMY",
                        ennemyShipConfig,
                    )
                elif ennemyShipConfig["naming"]["_type"] == "PT":
                    currentShip = Ship.corvette(
                        self.mainClock,
                        self.graphicsScene,
                        self.mapGen.gameMap,
                        self.mapGen.mapS,
                        ennemySpawnPos,
                        "ENNEMY",
                        ennemyShipConfig,
                    )
                else:
                    print("Could not Generate ship at", j, "!")
                self.graphicsScene.addShip(currentShip)
                currentShip = None
                ennemySpawnPos.setX(allySpawnPos.x() + 1000)
                ennemySpawnPos.setY(allySpawnPos.y() + 1000)

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
                self.spawnShips(playerFleet.values())
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
                print("EXITING BATTLE")

            if battleStateAtPause:
                self.mainClock.startClock()
                self.battleState = True

    def exitClicked(self):
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
