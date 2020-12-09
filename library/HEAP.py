# -*- coding: utf-8 -*-

'''
    File name: HEAP.py
    Author: Grégory LARGANGE
    Date created: 09/12/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 09/12/2020
    Python version: 3.8.1
'''


class HEAPItem():

    def __init__(self):
        self.heapIndex = 0


class HEAP():

    def __init__(self):
        self.items = []

    def addItem(self, _heapItem):
        self.items.append(_heapItem)
        _heapItem.heapIndex = len(self.items) - 1
        self.sortUp(_heapItem)

    def updateItem(self, _heapItem):
        self.sortUp(_heapItem)

    def contains(self, _heapItem):
        return self.items[_heapItem.heapIndex] == _heapItem

    def size(self):
        return len(self.items)

    def removeFirst(self):
        firstHeapItem = self.items[0]
        self.items[0] = self.items[-1]
        self.items[0].heapIndex = 0
        if len(self.items) > 1:
            del self.items[-1]
        self.sortDown(self.items[0])
        return firstHeapItem

    def sortUp(self, _heapItem):
        parentIndex = int((_heapItem.heapIndex - 1 ) / 2)
        if parentIndex < 0:
            parentIndex = 0

        while True:
            parentItem = self.items[parentIndex]

            if _heapItem.compareTo(parentItem) > 0:
                self.swap(_heapItem, parentItem)
            else:
                break

            parentIndex = int((_heapItem.heapIndex - 1 ) / 2)
            if parentIndex < 0:
                parentIndex = 0

    def sortDown(self, _heapItem):
        while True:
            childIndexLeft = int(_heapItem.heapIndex * 2 + 1)
            childIndexRight = int(_heapItem.heapIndex * 2 + 2)
            swapIndex = 0

            if childIndexLeft < len(self.items):
                swapIndex = childIndexLeft

                if childIndexRight < len(self.items):
                    if self.items[childIndexLeft].compareTo(self.items[childIndexRight]) < 0:
                        swapIndex = childIndexRight
                if _heapItem.compareTo(self.items[swapIndex]) < 0:
                    self.swap(_heapItem, self.items[swapIndex])
                else:
                    break
            else:
                break

    def swap(self, _heapItemA, _heapItemB):
        self.items[_heapItemA.heapIndex] = _heapItemB
        self.items[_heapItemB.heapIndex] = _heapItemA
        tmp_itemAIndex = _heapItemA.heapIndex
        _heapItemA.heapIndex = _heapItemB.heapIndex
        _heapItemB.heapIndex = tmp_itemAIndex