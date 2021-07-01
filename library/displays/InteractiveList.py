# -*- coding: utf-8 -*-

"""
    File name: InteractiveList.py
    Author: Grégory LARGANGE
    Date created: 29/06/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 30/06/2021
    Python version: 3.8.1
"""


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QBrush, QColor
from PyQt5.QtWidgets import QListView, QAbstractItemView


class InteractiveListView(QListView):
    def __init__(self, parent=None):
        super(InteractiveListView, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self._model = InteractiveListModel(self)
        self.setModel(self._model)
        self.attachedObject = None
        self.isForBattleSetup = True
        self.clicked.connect(self.onClick)

    def onClick(self, selection):
        _selectedIndexes = self.selectedIndexes()

        if self.isForBattleSetup:
            item = self._model.itemFromIndex(_selectedIndexes[0])
            print(item, " ", item.itemId, item.itemTag)
            self.attachedObject.setStatsFomList(item.itemId)
        else:
            for index in self.selectedIndexes():
                item = self._model.itemFromIndex(index)
                self.attachedObject.setItemSelected(item.itemId)

    def addToList(self, itemId, itemTag):
        self._model.appendItem(itemId, itemTag)

    def selectInList(self, selectedItemsId=None):
        if not selectedItemsId:
            self.clearSelection()
        else:
            for itemId in selectedItemsId:
                for item in self._model.allItems:
                    if item.itemId == itemId:
                        item.setSelected(True)

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

    def clearList(self):
        self._model.clearModel()


class InteractiveListModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(InteractiveListModel, self).__init__(parent)
        self.allItems = []

    def appendItem(self, itemId, itemTag):
        itemText = itemTag  # itemText = itemTag + "_" + Names.randomName(itemTag)
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
