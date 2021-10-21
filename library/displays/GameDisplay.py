# -*- coding: utf-8 -*-

"""
    File name: GameDisplay.py
    Author: Grégory LARGANGE
    Date created: 12/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 21/10/2021
    Python version: 3.8.1
"""

from library.Ship import Ship
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

from library import Island, Waypoint
from library.utils.MathsFormulas import Geometrics as geo, Cinematics as cin


class GameScene(QGraphicsScene):

    attachedGView = None
    attachedLView = None
    attachedGController = None
    nextShipID = 0
    nextIslandID = 0
    currentItem = None
    waypoints = []  # Deletable points
    trajpoints = []  # Permanent points

    def __init__(self, parent=None):
        super(GameScene, self).__init__(parent)

        self.innerBL = 0
        self.innerBR = 0
        self.innerBT = 0
        self.innerBB = 0
        self.innerArea = 0
        self.shipList = {}
        self.islandsList = []

    def mousePressEvent(self, mouseDown):
        if (self.innerBL <= int(mouseDown.scenePos().x()) <= self.innerBR) and (
            self.innerBT <= int(mouseDown.scenePos().y()) <= self.innerBB
        ):
            selected_item = self.itemAt(
                mouseDown.scenePos(), self.attachedGView.transform()
            )
            if mouseDown.button() == Qt.LeftButton:
                if selected_item:
                    self.attachedLView.selectInList([selected_item.data(0)])
                    if self.attachedGController:
                        self.attachedGController.display_current_ship_stats(
                            selected_item
                        )
                else:
                    self.attachedLView.selectInList()
                    if self.attachedGController:
                        self.attachedGController.display_current_ship_stats()
                super(GameScene, self).mousePressEvent(mouseDown)
            elif mouseDown.button() == Qt.RightButton:
                if not selected_item:
                    for item in self.selectedItems():
                        point = QPointF(
                            int(mouseDown.scenePos().x()), int(mouseDown.scenePos().y())
                        )
                        item.updatePath(point)
                        item.setTarget()
                    mouseDown.accept()
                elif selected_item:
                    if isinstance(selected_item, Ship):
                        for item in self.selectedItems():
                            if selected_item.data(1) == "ISLAND":
                                print("MOVEMENT NOT POSSIBLE")
                            elif selected_item.data(1) != item.data(1):
                                item.setTarget(selected_item)
                            elif selected_item.data(1) == item.data(1):
                                print("Follow")
                        mouseDown.accept()
                else:
                    super(GameScene, self).mousePressEvent(mouseDown)
        else:
            self.attachedLView.selectInList()
            self.attachedGController.display_current_ship_stats()
            super(GameScene, self).mousePressEvent(mouseDown)

    def setInnerMap(self, mapExtension, innerMap):
        self.innerBL = int(mapExtension)
        self.innerBR = int(innerMap + mapExtension)
        self.innerBT = int(mapExtension)
        self.innerBB = int(innerMap + mapExtension)

    def displayMap(self, obstaclesList):
        for obstacle in obstaclesList:
            self.currentItem = Island.Island(self, obstacle)
            thisIslandId = self.nextIslandID
            self.currentItem.setData(0, thisIslandId)
            self.currentItem.setData(1, "ISLAND")
            self.currentItem.setZValue(1)
            self.nextIslandID += 1
            self.addItem(self.currentItem)
            self.islandsList.append(self.currentItem)
            self.currentItem = None

    def shipsInDetectionRange(self, refShip):
        shipsInDRange = []

        for ship in self.shipList.values():
            if (ship.data(0) != refShip.data(0)) & (ship.data(1) != refShip.data(1)):
                effScanRange = (
                    refShip.instant_vars["detection_range"]
                    - (refShip.instant_vars["detection_range"] - 1000)
                    * ship.instant_vars["concealement"]
                )
                shipCenter = geo.parallelepiped_Center(
                    ship.pos(), ship.rect().width(), ship.rect().height()
                )
                refShipCenter = geo.parallelepiped_Center(
                    refShip.pos(), refShip.rect().width(), refShip.rect().height()
                )
                distance = geo.distance_A_B(refShipCenter, shipCenter)
                if distance <= effScanRange:
                    shipsInDRange.append(ship)
        return shipsInDRange

    def detectionRay(self, origin, angleInRad, distance, resolution, offset=0):
        currentPos = origin

        for i in range(offset, distance - resolution, resolution):
            currentPos = cin.movementBy(currentPos, i, angleInRad)
            # self.addLine(origin.x(), origin.y(), currentPos.x(), currentPos.y())
            _item = self.itemAt(currentPos, self.attachedGView.transform())
            if _item:
                if _item.data(2):
                    return i
        return None

    def isInLineOfSight(self, origin, target, resolution):
        currentPos = origin
        distance = int(geo.distance_A_B(origin, target))
        angleInrad = geo.angle(origin, target)

        while int(geo.distance_A_B(origin, currentPos)) < distance:
            currentPos = cin.movementBy(currentPos, resolution, angleInrad)
            _item = self.itemAt(currentPos, self.attachedGView.transform())
            if _item:
                if _item.data(1) == "ISLAND":
                    # self.addLine(
                    #     origin.x(),
                    #     origin.y(),
                    #     currentPos.x(),
                    #     currentPos.y(),
                    #     QPen(QColor("red"), 4),
                    # )
                    return False
        # self.addLine(
        #     origin.x(),
        #     origin.y(),
        #     currentPos.x(),
        #     currentPos.y(),
        #     QPen(QColor("green"), 4),
        # )
        return True

    def dispGrid(self, step):
        for i in range(0, int(self.height()), step):
            self.addLine(0, i, int(self.width()), i, QPen(QColor("black"), 4))

        for i in range(0, int(self.width()), step):
            self.addLine(i, 0, i, self.height(), QPen(QColor("black"), 4))

        self.addLine(
            self.innerBL,
            self.innerBT,
            self.innerBR,
            self.innerBT,
            QPen(QColor("black"), 20),
        )
        self.addLine(
            self.innerBL,
            self.innerBT,
            self.innerBL,
            self.innerBB,
            QPen(QColor("black"), 20),
        )
        self.addLine(
            self.innerBR,
            self.innerBT,
            self.innerBR,
            self.innerBB,
            QPen(QColor("black"), 20),
        )
        self.addLine(
            self.innerBL,
            self.innerBB,
            self.innerBR,
            self.innerBB,
            QPen(QColor("black"), 20),
        )

    def dispPenalties(self, penaltyMap, step):
        baseColor = [255, 255, 255]

        for i, line in enumerate(penaltyMap):
            for j, penalty in enumerate(line):
                c_color = QColor(
                    baseColor[0] * ((100 - penalty * 10) / 100),
                    baseColor[1] * ((100 - penalty * 10) / 100),
                    baseColor[2] * ((100 - penalty * 10) / 100),
                )
                self.addRect(
                    j * step, i * step, step, step, QPen(c_color), QBrush(c_color)
                )

    def printPoint(self, point, size, color, permanent=False):
        c_point = Waypoint.Waypoint(
            point.x() - int(size / 2), point.y() - int(size / 2), size, size, color
        )
        if permanent:
            self.trajpoints.append(c_point)
        else:
            self.waypoints.append(c_point)
        self.addItem(c_point)

    def clearWaypoints(self):
        for item in self.waypoints:
            self.removeItem(item)
        self.waypoints.clear()

    def addShip(self, shipObject):
        thisShipId = self.nextShipID
        shipObject.setData(0, thisShipId)
        shipObject.setZValue(2)
        self.shipList[thisShipId] = shipObject
        self.addItem(shipObject)
        if shipObject.data(1) == "ALLY":
            self.attachedLView.addToList(thisShipId, shipObject.naming["_type"])
        self.nextShipID += 1

    def select_unselect_items(self, item_ids_list):
        for item_id in item_ids_list:
            for item in self.items(
                self.sceneRect(),
                Qt.IntersectsItemShape,
                Qt.DescendingOrder,
                self.attachedGView.transform(),
            ):
                if item.data(0) == item_id:
                    item.setSelected(True)
                else:
                    item.setSelected(False)

    def clearMap(self):
        for item in self.islandsList:
            self.removeItem(item)
        self.islandsList.clear()
        self.nextIslandID = 0

        self.clearWaypoints()
        for item in self.trajpoints:
            self.removeItem(item)
        self.trajpoints.clear()

        self.clear()
        self.update()

    def destroyObject(self, _object):
        self.removeItem(_object)
        del _object

    def clearGameScene(self):
        for ship in self.shipList.values():
            self.removeItem(ship)
        self.nextShipID = 0
        self.clearMap()


class GameView(QGraphicsView):
    def __init__(self, parent=None):
        """

        Parameters
        ----------
        parent : QObject, optional
            The parent of the class.

        Returns
        -------
        None.

        Summary
        -------
        Constructor.

        """
        super(GameView, self).__init__(parent)
        self.gameScene = parent
        self.currentZoom = 1.0
        self.zoomInFactor = 1.1
        self.zoomOutFactor = 1 / self.zoomInFactor
        self.ctrlKeyDown = False

    def wheelEvent(self, event):
        """

        Parameters
        ----------
        event : QWheelEvent
            A signal indicating that the mouse wheel angle has changed.

        Returns
        -------
        None.

        Summary
        -------
        If the bool ctrlKeyDown is TRUE at the moment of the event, triggers
        the zoom functionnality:
        Unset anchors so that cursor is the focus of the zoom.
        Apply zoomIn or zooOut factor depending on the sign of wheel event angle
        delta.
        Translate view according to scale change.

        """
        if self.ctrlKeyDown:

            # Set Anchors
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.setResizeAnchor(QGraphicsView.NoAnchor)

            # Save the cursor position in the scene at the moment of the event
            oldPos = self.mapToScene(event.pos())

            # Zoom
            if event.angleDelta().y() > 0:
                zoomFactor = self.zoomInFactor
            else:
                zoomFactor = self.zoomOutFactor
            self.currentZoom *= zoomFactor
            # Do not apply zoom if outside of defined boundaries
            if not (self.currentZoom <= 0.1) | (self.currentZoom >= 15.0):
                self.scale(zoomFactor, zoomFactor)
            elif self.currentZoom <= 0.1:
                self.currentZoom = 0.1
            elif self.currentZoom >= 15.0:
                self.currentZoom = 15.0

            # Get the new position of the event in the scaled scene
            newPos = self.mapToScene(event.pos())

            # Move scene to old position
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())

    def keyPressEvent(self, keyEvent):
        """

        Parameters
        ----------
        keyEvent : QKeyPressEvent
            A signal indicating that a keyboard key was pressed.

        Returns
        -------
        None.

        Summary
        -------
        If the key pressed is Control, set the bool ctrlKeyDown to True.
        If the key pressed is Back, reset the transform of the GraphicView,
        along with reseting the view anchors to center and scaling it back to 1.

        """
        if keyEvent.key() == Qt.Key_Control:
            self.ctrlKeyDown = True
        if keyEvent.key() == Qt.Key_Backspace:
            self.resetZoom()
        super(GameView, self).keyPressEvent(keyEvent)

    def keyReleaseEvent(self, keyEvent):
        """

        Parameters
        ----------
        keyEvent : QKeyReleaseEvent
            A signal indicating that a keyboard key was released.

        Returns
        -------
        None.

        Summary
        -------
        If the key released is Control, set the bool ctrlKeyDown to False.

        """
        if keyEvent.key() == Qt.Key_Control:
            self.ctrlKeyDown = False

    def resetZoom(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Resets the game view to its original scale and anchor position.
        """
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.resetTransform()
        self.scale(1.0, 1.0)
        self.currentZoom = 1.0
