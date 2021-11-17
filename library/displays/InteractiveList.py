# -*- coding: utf-8 -*-

"""
    File name: InteractiveList.py
    Author: Grégory LARGANGE
    Date created: 29/06/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 18/10/2021
    Python version: 3.8.1
"""


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QBrush, QColor
from PyQt5.QtWidgets import QListView, QAbstractItemView


class InteractiveListView(QListView):
    def __init__(self, _extendedSelection=False, parent=None):
        super(InteractiveListView, self).__init__(parent)
        if _extendedSelection:
            self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        else:
            self.setSelectionMode(QAbstractItemView.SingleSelection)
        self._model = InteractiveListModel(self)
        self.setModel(self._model)
        self.attachedObject = None
        self.isForBattleSetup = True
        self.clicked.connect(self.onClick)

    def onClick(self):
        _selectedIndexes = self.selectedIndexes()

        if self.isForBattleSetup:
            item = self._model.itemFromIndex(_selectedIndexes[0])
            self.attachedObject.setStatsFomList(item.itemId)
        else:
            ids_list = []
            for index in self.selectedIndexes():
                item = self._model.itemFromIndex(index)
                ids_list.append(item.itemId)
            self.attachedObject.select_unselect_items(ids_list)

    def addToList(self, itemId: int, itemTag: str, text: str = None):
        self._model.appendItem(itemId, itemTag, text)

    def selectInList(self, selectedItemsId: list = None):
        if not selectedItemsId:
            self.clearSelection()
        else:
            for item_id in selectedItemsId:
                for item in self._model.allItems:
                    if item.itemId == item_id:
                        item_index = item.index()
                        self.setCurrentIndex(item_index)

    def removeFromList(self, itemIdList=None):
        if itemIdList:
            for itemId in itemIdList:
                for item in self._model.allItems:
                    if item.itemId == itemId:
                        index = item.index()
                        self._model.removeItem(index)
        else:
            self.removeFromShipDict()

    def removeFromShipDict(self):
        itemIDsToRemove = []

        # remove from list first
        for index in self.selectedIndexes():
            item = self._model.itemFromIndex(index)
            itemIDsToRemove.append(item.itemId)
            self._model.removeItem(index)
        # removes from ships dictionnary in battle setup
        self.attachedObject.removeShips(itemIDsToRemove)

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
        If the key pressed is delete, calls removeFromListAndScene().

        """
        if self.isForBattleSetup:
            if keyEvent.key() == Qt.Key_Delete:
                self.removeFromShipDict()

    def mousePressEvent(self, mouse_press_event):
        if not self.indexAt(mouse_press_event.pos()).isValid():
            self.clearSelection()
            if self.isForBattleSetup:
                self.attachedObject.set_blank_ship_stats()
        super(InteractiveListView, self).mousePressEvent(mouse_press_event)

    def clearList(self):
        self._model.clearModel()


class InteractiveListModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(InteractiveListModel, self).__init__(parent)
        self.allItems = []

    def appendItem(self, itemId, itemTag, text=None):
        if text:
            itemText = itemTag + "_" + text
        else:
            itemText = itemTag
        item = CustomItem(itemText, itemId, itemTag)
        item.setData(QBrush(QColor(162, 231, 253)), Qt.BackgroundColorRole)
        self.allItems.append(item)
        self.appendRow(item)

    def removeItem(self, index):
        item = self.itemFromIndex(index)
        self.allItems.remove(item)
        self.removeRow(index.row())

    def clearModel(self):
        self.removeRows(0, self.rowCount())
        self.allItems.clear()
        self.clear()


class CustomItem(QStandardItem):
    def __init__(self, itemText, itemId, itemTag):
        super(CustomItem, self).__init__(itemText)
        self.itemId = itemId
        self.itemTag = itemTag
        self.setCheckable(False)
        self.setEditable(False)
