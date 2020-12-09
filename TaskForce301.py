# -*- coding: utf-8 -*-

'''
    File name: TaskForce301.py
    Author: Grégory LARGANGE
    Date created: 07/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 09/12/2020
    Python version: 3.8.1
'''

import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsView

from library import MainClock, GameScene, Battleship, InGameData, Mapping


class Ui_TSKF301MainWindow(object):

    mainClock = MainClock.MainClock(20)  #ms
    mapGen = None

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
        self.actionStart_Pause_Game = QtWidgets.QAction(TSKF301MainWindow)
        self.actionStart_Pause_Game.setObjectName("actionStart_Pause_Game")
        self.actionAstar = QtWidgets.QAction(TSKF301MainWindow)
        self.actionAstar.setObjectName("actionAstar")
        self.menuGame.addAction(self.actionNew_Game)
        self.menuGame.addAction(self.actionNew_GameMap)
        self.menuGame.addAction(self.actionStart_Pause_Game)
        self.menuGame.addAction(self.actionAstar)
        self.menubar.addAction(self.menuGame.menuAction())

        self.retranslateUi(TSKF301MainWindow)
        QtCore.QMetaObject.connectSlotsByName(TSKF301MainWindow)

        self.actionNew_Game.triggered.connect(self.newGame)
        self.actionNew_GameMap.triggered.connect(self.newGameMap)
        self.actionStart_Pause_Game.triggered.connect(self.start_Pause_Game)
        self.actionAstar.triggered.connect(self.launchAstar)

    def retranslateUi(self, TSKF301MainWindow):
        _translate = QtCore.QCoreApplication.translate
        TSKF301MainWindow.setWindowTitle(_translate("TSKF301MainWindow", "TSKF301MainWindow"))
        self.menuGame.setTitle(_translate("TSKF301MainWindow", "Game"))
        self.playerShipsDW.setWindowTitle(_translate("TSKF301MainWindow", "SHIPS"))
        self.actionNew_Game.setText(_translate("TSKF301MainWindow", "New Game"))
        self.actionNew_Game.setShortcut(_translate("TSKF301MainWindow", "N"))
        self.actionNew_GameMap.setText(_translate("TSKF301MainWindow", "New Game Map"))
        self.actionNew_GameMap.setShortcut(_translate("TSKF301MainWindow", "M"))
        self.actionStart_Pause_Game.setText(_translate("TSKF301MainWindow", "Start Game"))
        self.actionStart_Pause_Game.setShortcut(_translate("TSKF301MainWindow", "Space"))
        self.actionAstar.setText(_translate("TSKF301MainWindow", "PathFinder"))
        self.actionAstar.setShortcut(_translate("TSKF301MainWindow", "A"))

    def newGame(self):
        self.graphicsScene.setSceneRect(0, 0, 150000, 50000)
        self.graphicsView.fitInView(QtCore.QRectF(0, 0,
                                                  self.graphicsScene.width(),
                                                  self.graphicsScene.height()),
                                    Qt.KeepAspectRatio)
        self.graphicsScene.dispGrid(1000)
        self.mapGen = Mapping.MapGenerator(self.graphicsScene.width(),
                                           self.graphicsScene.height(), 1000)
        self.mapGen.setMapParameters(0.25, 2, 5, 2, 5, 2)
        self.genRandomMap()
        self.gameState = False

        self.rComs = InGameData.RadioCommunications(self.mainClock,
                                                    self.graphicsScene)

        # ship1 = Battleship.Battleship(self.mainClock, self.graphicsScene,
        #                               QtCore.QPointF(0, 0), 1, 1, 1, 0)
        # ship1.setTag("ALLY")
        # self.graphicsScene.addShip(ship1)

        # ship2 = Battleship.Battleship(self.mainClock, self.graphicsScene,
        #                               QtCore.QPointF(10000, 15000), 1, 1, 1, 0)
        # ship2.setTag("ALLY")
        # self.graphicsScene.addShip(ship2)

        # ship3 = Battleship.Battleship(self.mainClock, self.graphicsScene,
        #                               QtCore.QPointF(12000, 17000), 1, 1, 1, 0)
        # ship3.setTag("ENNEMY")
        # self.graphicsScene.addShip(ship3)

        self.rComs.updateShipLists()

    def newGameMap(self):
        self.graphicsScene.clearMap()
        self.mapGen.resetMap()
        self.genRandomMap()

    def genRandomMap(self):
        genObs = self.mapGen.generateMap()
        self.graphicsScene.displayMap(genObs)

    def launchAstar(self):
        aStar = Mapping.Astar(self.mapGen.gameMap, self.mapGen.mapS)
        nodesPath = aStar.findPath(QPointF(0, 0), QPointF(149000, 49000))
        for node in nodesPath:
            self.graphicsScene.addRect(node.xPos, node.yPos, 1000, 1000,
                                        QPen(QColor("blue")), QBrush(QColor("blue")))

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
    TSKF301MainWindow.show()
    sys.exit(app.exec_())
