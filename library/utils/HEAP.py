# -*- coding: utf-8 -*-

'''
    File name: HEAP.py
    Author: Grégory LARGANGE
    Date created: 09/12/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 10/12/2020
    Python version: 3.8.1
'''


class HEAPItem():
    """

    A class to be used with HEAP class datasets.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    __init__()
        The constructor of the class.

    """

    def __init__(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        self.heapIndex = 0


class HEAP():
    """

    A class implementing a heap dataset, aimed at optimizing the nodes
    evaluation process.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    __init__()
        The constructor of the class.

    addItem(_heapItem : HEAPItem)
        adds _heapItem to the dataset.

    updateItem(_heapItem)
        Updates an exisiting _heapItem position in the dataset

    contains(_heapItem)
        Returns True or False depending on the presence of _heapItem in the
        dataset.

    size()
        returns the lenght of the dataset.

    removeFirst()
        Removes and returns the first heapItem of the dataset.

    sortUp(_heapItem : HEAPItem)
        Moves up the dataset _heapItem according to its Priority.

    sortDown(_heapItem : HEAPItem)
        Moves down the dataset _heapItem according to its Priority.

    swap(_heapItemA : HEAPItem, _heapItemB : HEAPItem)
        Swaps the position of _heapItemA and _heapItemB in the dataset.

    clearItems()
        Clears the dataset.

    """

    def __init__(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        self.items = []

    def addItem(self, _heapItem):
        """

        Parameters
        ----------
        _heapItem : HEAPItem
            a HEAPItem to add to the HEAP Dataset.

        Returns
        -------
        None.

        Summary
        -------
        Adds _heapItem to the dataset.

        """
        self.items.append(_heapItem)
        _heapItem.heapIndex = len(self.items) - 1
        self.sortUp(_heapItem)

    def updateItem(self, _heapItem):
        """

        Parameters
        ----------
        _heapItem : HEAPItem
            The HEAPItem to update.

        Returns
        -------
        None.

        Summary
        -------
        Updates _heapItem position in the heap dataset.

        """
        self.sortUp(_heapItem)

    def contains(self, _heapItem):
        """

        Parameters
        ----------
        _heapItem : HEAPItem
            The HEAPItem to test the presence in the heap dataset.

        Returns
        -------
        bool
            True if _heapItem is present in the dataset, else False.

        """
        return self.items[_heapItem.heapIndex] == _heapItem

    def size(self):
        """

        Returns
        -------
        int
            The lenght of the dataset.

        Summary
        -------
        Returns the length of the dataset.

        """
        return len(self.items)

    def removeFirst(self):
        """

        Returns
        -------
        firstHeapItem : HEAPItem
            The first HEAPItem in the dataset.

        Summary
        -------
        Remove the first HEAPItem from the dataset and returns it.

        """
        firstHeapItem = self.items[0]
        self.items[0] = self.items[-1]
        self.items[0].heapIndex = 0
        if len(self.items) > 1:
            del self.items[-1]
        self.sortDown(self.items[0])
        return firstHeapItem

    def sortUp(self, _heapItem):
        """

        Parameters
        ----------
        _heapItem : HEAPItem
            the HEAPItem to sort up..

        Returns
        -------
        None.

        Summary
        -------
        Sort up _heapItem using its Priority. As long as its Priority is higher
        than its parent Priority, _heapItem is moved up the dataset.

        """
        # Formula to get the index of any HEAPItem parent
        parentIndex = int((_heapItem.heapIndex - 1 ) / 2)
        if parentIndex < 0:
            parentIndex = 0

        while True:
            # we get the HEAPItem at parentIndex
            parentItem = self.items[parentIndex]

            # If _heapItem has lower Fcost than its parent, we swap them
            if _heapItem.compareTo(parentItem) > 0:
                self.swap(_heapItem, parentItem)
            else:
                break

            # As long as _heapItem Fcost is moved up, we get its new parent
            parentIndex = int((_heapItem.heapIndex - 1 ) / 2)
            if parentIndex < 0:
                parentIndex = 0

    def sortDown(self, _heapItem):
        """

        Parameters
        ----------
        _heapItem : HEAPItem
            The HEAPItem to sort down.

        Returns
        -------
        None.

        Summary
        -------
        Sort down _heapItem. As long as its Priority is lower than its children
        Priority, _heapItem is moved down the dataset.

        """
        while True:
            childIndexLeft = int(_heapItem.heapIndex * 2 + 1)
            childIndexRight = int(_heapItem.heapIndex * 2 + 2)
            swapIndex = 0

            # Left child of _heapItem exists if its calculated index is within
            # the dataset.
            if childIndexLeft < len(self.items):
                swapIndex = childIndexLeft

                if childIndexRight < len(self.items):
                    # If _heapItem has both a left and a right child, we compare
                    # them to determine with which we will swap _heapItem
                    if self.items[childIndexLeft].compareTo(self.items[childIndexRight]) < 0:
                        swapIndex = childIndexRight
                if _heapItem.compareTo(self.items[swapIndex]) < 0:
                    self.swap(_heapItem, self.items[swapIndex])
                else:
                    break
            else:
                break

    def swap(self, _heapItemA, _heapItemB):
        """

        Parameters
        ----------
        _heapItemA : HEAPItem
            A HEAPItem to swap.
        _heapItemB : HEAPItem
            A HEAPItem to swap.

        Returns
        -------
        None.

        Summary
        -------
        Swaps _heapItemA and _heapItemB positions in the dataset. Updates their
        heapIndex.

        """
        self.items[_heapItemA.heapIndex] = _heapItemB
        self.items[_heapItemB.heapIndex] = _heapItemA
        tmp_itemAIndex = _heapItemA.heapIndex
        _heapItemA.heapIndex = _heapItemB.heapIndex
        _heapItemB.heapIndex = tmp_itemAIndex

    def clearItems(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Clears the dataset.

        """
        self.items.clear()
