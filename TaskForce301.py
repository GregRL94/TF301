# -*- coding: utf-8 -*-

"""
    File name: TaskForce301.py
    Author: Grégory LARGANGE
    Date created: 07/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 28/05/2021
    Python version: 3.8.1
"""

import sys

from os import path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGraphicsView

from library import MainClock, GameScene, Mapping, InGameData
from library.Ship import Ship
from library.utils.Config import Config

from library.dialogs.BattleSetup import BattleSetup


class Ui_TSKF301MainWindow(object):
    def setupUi(self, TSKF301MainWindow):
        TSKF301MainWindow.setObjectName("TSKF301MainWindow")
        TSKF301MainWindow.resize(1280, 960)
        self.centralwidget = QtWidgets.QWidget(TSKF301MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsScene = GameScene.GameScene(self.centralwidget)
        self.graphicsView = QGraphicsView(self.graphicsScene)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsScene.attachedGView = self.graphicsView
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
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
        TSKF301MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.playerShipsDW)
        self.actionNew_Game = QtWidgets.QAction(TSKF301MainWindow)
        self.actionNew_Game.setObjectName("actionNew_Game")
        self.actionNew_GameMap = QtWidgets.QAction(TSKF301MainWindow)
        self.actionNew_GameMap.setObjectName("actionNew_GameMap")
        self.actionSpawnShips = QtWidgets.QAction(TSKF301MainWindow)
        self.actionSpawnShips.setObjectName("actionSpawnShips")
        self.actionBattleSetup = QtWidgets.QAction(TSKF301MainWindow)
        self.actionBattleSetup.setObjectName("actionBattleSetup")
        self.actionStart_Pause_Game = QtWidgets.QAction(TSKF301MainWindow)
        self.actionStart_Pause_Game.setObjectName("actionStart_Pause_Game")
        self.menuGame.addAction(self.actionNew_Game)
        self.menuGame.addAction(self.actionNew_GameMap)
        self.menuGame.addAction(self.actionSpawnShips)
        self.menuGame.addAction(self.actionBattleSetup)
        self.menuGame.addAction(self.actionStart_Pause_Game)
        self.menubar.addAction(self.menuGame.menuAction())

        self.retranslateUi(TSKF301MainWindow)
        QtCore.QMetaObject.connectSlotsByName(TSKF301MainWindow)

        self.actionNew_Game.triggered.connect(self.newGame)
        self.actionNew_GameMap.triggered.connect(self.newGameMap)
        self.actionSpawnShips.triggered.connect(self.spawnShips)
        self.actionBattleSetup.triggered.connect(self.testCreateBattle)
        self.actionStart_Pause_Game.triggered.connect(self.start_Pause_Game)

    def retranslateUi(self, TSKF301MainWindow):
        _translate = QtCore.QCoreApplication.translate
        TSKF301MainWindow.setWindowTitle(
            _translate("TSKF301MainWindow", "TSKF301MainWindow")
        )
        self.menuGame.setTitle(_translate("TSKF301MainWindow", "Game"))
        self.playerShipsDW.setWindowTitle(_translate("TSKF301MainWindow", "SHIPS"))
        self.actionNew_Game.setText(_translate("TSKF301MainWindow", "New Game"))
        self.actionNew_Game.setShortcut(_translate("TSKF301MainWindow", "N"))
        self.actionNew_GameMap.setText(_translate("TSKF301MainWindow", "New Game Map"))
        self.actionNew_GameMap.setShortcut(_translate("TSKF301MainWindow", "M"))
        self.actionBattleSetup.setText(_translate("TSKF301MainWindow", "Battle"))
        self.actionBattleSetup.setShortcut(_translate("TSKF301MainWindow", "B"))
        self.actionSpawnShips.setText(_translate("TSKF301MainWindow", "Spawn ships"))
        self.actionSpawnShips.setShortcut(_translate("TSKF301MainWindow", "S"))
        self.actionStart_Pause_Game.setText(
            _translate("TSKF301MainWindow", "Start Game")
        )
        self.actionStart_Pause_Game.setShortcut(
            _translate("TSKF301MainWindow", "Space")
        )

    def loadConfigsAsDicts(self):
        _configsDict = {}

        _bb_cfg = path.join(
            path.dirname(path.realpath(__file__)), "library/configs/battleshipConfig.py"
        )
        _bb_dict, _bb_txt = Config._file2dict(_bb_cfg)
        _configsDict["BB"] = _bb_dict

        # _ca_cfg = path.join(
        #     path.dirname(path.realpath(__file__)), "library/configs/cruiserConfig.py"
        # )
        # _ca_dict, _ca_txt = Config._file2dict(_ca_cfg)
        # configsDict["CA"] = _ca_dict

        # _ff_cfg = path.join(
        #     path.dirname(path.realpath(__file__)), "library/configs/frigateConfig.py"
        # )
        # _ff_dict, _ff_txt = Config._file2dict(_ff_cfg)
        # configsDict["FF"] = _ff_dict

        # _pt_cfg = path.join(
        #     path.dirname(path.realpath(__file__)), "library/configs/corvetteConfig.py"
        # )
        # _pt_dict, _pt_txt = Config._file2dict(_pt_cfg)
        # configsDict["PT"] = _pt_dict

        _tur_cfg = path.join(
            path.dirname(path.realpath(__file__)), "library/configs/turretConfig.py"
        )
        _tur_dict, _tur_txt = Config._file2dict(_tur_cfg)
        _configsDict["TUR"] = _tur_dict

        return _configsDict

    def initGameData(self):
        self.mainClock = MainClock.MainClock(25)  # ms
        self.configsDict = self.loadConfigsAsDicts()
        self.mapGen = None
        self.mapExtPercentage = 0.10
        self.mapRes = 500

    def genRandomMap(self):
        genObs = self.mapGen.generateMap()
        self.graphicsScene.displayMap(genObs)

    def debugDisp(self, gridOn=True, penalties=True):
        if gridOn:
            self.graphicsScene.dispGrid(self.mapRes)
        if penalties:
            _penaltyMap = self.mapGen.getPenaltyMap()
            self.graphicsScene.dispPenalties(_penaltyMap, self.mapRes)

    def newGame(self):
        playableArea = 20000
        self.graphicsScene.setSceneRect(
            0,
            0,
            int(playableArea * (1 + self.mapExtPercentage)),
            int(playableArea * (1 + self.mapExtPercentage)),
        )
        self.graphicsScene.setInnerMap(self.mapExtPercentage, playableArea)
        self.graphicsView.fitInView(
            QtCore.QRectF(0, 0, playableArea, playableArea), Qt.KeepAspectRatio
        )
        self.mapGen = Mapping.MapGenerator(
            self.graphicsScene.width(), self.graphicsScene.height(), self.mapRes
        )
        self.mapGen.setMapParameters(0.2, 4, 10, 4, 10, 4)
        self.genRandomMap()
        self.debugDisp(True, False)
        self.gameState = False

        self.rComs = InGameData.RadioCommunications(self.mainClock, self.graphicsScene)

    def newGameMap(self):
        self.graphicsScene.clearMap()
        self.mapGen.resetMap()
        self.genRandomMap()
        self.debugDisp(True, False)

    def spawnShips(self):
        _bb_cfg = path.join(
            path.dirname(path.realpath(__file__)), "library/configs/battleshipConfig.py"
        )
        _bb_dict, _bb_txt = Config._file2dict(_bb_cfg)
        ship1 = Ship._battleShip(
            self.mainClock,
            self.graphicsScene,
            self.mapGen.gameMap,
            self.mapGen.mapS,
            QPointF(2500, 2500),
            "ALLY",
            _bb_dict,
        )
        self.graphicsScene.addShip(ship1)
        _bb_dict, _bb_txt = None, None

        # _bb_dict, _bb_txt = Config._file2dict(_bb_cfg)
        # ship2 = Ship._battleShip(
        #     self.mainClock,
        #     self.graphicsScene,
        #     self.mapGen.gameMap,
        #     self.mapGen.mapS,
        #     QPointF(2500, 5000),
        #     "ALLY",
        #     _bb_dict,
        # )
        # self.graphicsScene.addShip(ship2)
        # _bb_dict, _bb_txt = None, None

        # _bb_dict, _bb_txt = Config._file2dict(_bb_cfg)
        # ship3 = Ship._battleShip(
        #     self.mainClock,
        #     self.graphicsScene,
        #     self.mapGen.gameMap,
        #     self.mapGen.mapS,
        #     QPointF(12500, 10000),
        #     "ENNEMY",
        #     _bb_dict,
        # )
        # self.graphicsScene.addShip(ship3)
        # _bb_dict, _bb_txt = None, None

        # _bb_dict, _bb_txt = Config._file2dict(_bb_cfg)
        # ship4 = Ship._battleShip(
        #     self.mainClock,
        #     self.graphicsScene,
        #     self.mapGen.gameMap,
        #     self.mapGen.mapS,
        #     QPointF(12500, 12500),
        #     "ENNEMY",
        #     _bb_dict,
        # )
        # self.graphicsScene.addShip(ship4)
        # _bb_dict, _bb_txt = None, None

        self.rComs.updateShipLists()

    def testCreateBattle(self):
        b_setup = BattleSetup(self.configsDict)
        result = b_setup.battleSetupUI()
        if result:
            result = b_setup.createFleetUi()

    def start_Pause_Game(self):
        if self.gameState:
            self.mainClock.stopClock()
            self.gameState = False
        else:
            self.mainClock.startClock()
            self.gameState = True


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
    ui.initGameData()
    TSKF301MainWindow.show()
    sys.exit(app.exec_())
