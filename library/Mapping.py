# -*- coding: utf-8 -*-

'''
    File name: MapGenerator.py
    Author: Grégory LARGANGE
    Date created: 25/11/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 10/12/2020
    Python version: 3.8.1
'''

import random, time

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygonF
from library import MathsFormulas, HEAP


class MapGenerator():
    """

    A class to proceduraly generate a map of defined size. The obstacles of the
    map are randomly generated according to the map parameters.

    ...

    Attributes
    ----------
    curO : float
        The current obstruction percentage of the map.

    nObstacles : int
        The number of obstacles on the map.

    emergencyBreak : int
        The maximum number of iteration that the map geerator is allowed to do
        when generating a map.

    Methods
    -------
    __init__(mapWidth : int, mapHeight : int, mapSlicing : int)
        The constructor of the class. Defines the map size and initialize the
        map grid according to the map size.

    setMapParameters(maxObstruction : float, minObstWidth : int, maxObstWidth : int,
                     minObstHeight : int, maxObstHeight : int , minD2Obstacles : int)
        Sets up the parameters that will be used to generates random obstacles.

    resetMap()
        Reset the map Grid and deletes all obstacles. Keeps the map size.

    randomObstacle()
        Propose a random obstacle within the defined parameters.

    checkAvailableSpace(coordList : list of int)
        Checks if the proposed coordinates of a obstacle does not overlap any
        already existing obstacle.

    generateObstacle(ObsAsList : list of int)
        Generates an obstacle with the coordinates given by ObsAsList.

    generateMap()
        The main loop function to generate a procedural map.

    """

    curO = 0
    nObstacles = 0
    emergencyBreak = 500

    def __init__(self, mapWidth, mapHeight, mapSlicing):
        """

        Parameters
        ----------
        mapWidth : int
            The width of the map.
        mapHeight : int
            The height of the map.
        mapSlicing : int
            The resolution of the map.

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class.

        """
        self.geometrics = MathsFormulas.Geometrics()
        self.gameMap = []

        self.mapW = int(mapWidth / mapSlicing)
        self.mapH = int(mapHeight / mapSlicing)
        self.mapS = mapSlicing  # The "resolution" of the map.
        self.mapA = self.mapW * self.mapH  # Map area

        self.maxO = 0.0  # The maximum percentage of the map area that can be obstacles.
        self.minObsW = 0  # The minimun width of an obstacle.
        self.maxObsW = 0  # The maximum width of an obstacle.
        self.minObsH = 0  # The minimun height of an obstacle.
        self.maxObsH = 0  # The maximum height of an obstacle.
        self.minD2O = 0  # The minimum distance between two distinct obstacles.

        self.polygonsList = []  # All obstacles defining polygons.

        # Creation of the map.
        for i in range(self.mapH):
            self.gameMap.append([])
            for j in range(self.mapW):
                self.gameMap[i].append(0)

    def setMapParameters(self, maxObstruction, minObstWidth, maxObstWidth,
                         minObstHeight, maxObstHeight, minD2Obstacles):
        """

        Parameters
        ----------
        maxObstruction : float
            The maximum percentage of the map area that can be obstacles.
        minObstWidth : int
            The minimun width of an obstacle.
        maxObstWidth : int
            The maximum width of an obstacle..
        minObstHeight : int
            The minimun height of an obstacle..
        maxObstHeight : int
            The maximum height of an obstacle..
        minD2Obstacles : int
            The minimum distance between two distinct obstacles..

        Returns
        -------
        None.

        Summary
        -------
        Sets up the parameters for the procedural obstacles generation.
        For example, a random obstacle height cannot exceed maxObstHeight and
        cannot be closer to another obstacle than minD2Obstacles.

        """
        self.maxO = maxObstruction
        self.minObsW = minObstWidth
        self.maxObsW = maxObstWidth
        self.minObsH = minObstHeight
        self.maxObsH = maxObstHeight
        self.minD2O = minD2Obstacles

    def resetMap(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Deletes all obstacles. Keeps the map size defined in the __init__().

        """
        if len(self.gameMap) > 0:
            for i in range(len(self.gameMap)):
                for j in range(len(self.gameMap[0])):
                    self.gameMap[i][j] = 0

        self.curO = 0  # reset current map obstruction percentage.
        self.nObstacles = 0  # reset the number of obstacles.
        self.polygonsList.clear()  # Clear all obstacles polygons.

    def randomObstacle(self):
        """

        Returns
        -------
        list
            The coordinates of the proposed randomly generated obstacle.

        Summary
        -------
        Generates a random obstacle using the obstacle parameters as boundaries.

        """
        tlx = random.randint(0, len(self.gameMap[0]) - 1 - self.minObsW)  # Ensures that obstacle is inside the map
        tly = random.randint(0, len(self.gameMap) - 1 - self.minObsH)  # Ensures that obstacle is inside the map
        w = random.randint(self.minObsW, self.maxObsW)
        h = random.randint(self.minObsH, self.maxObsH)
        return [tlx, tly, w, h]

    def checkAvailableSpace(self, coordList):
        """

        Parameters
        ----------
        coordList : list
            A list of proposed coordinates for a random obstacle.

        Returns
        -------
        list
            The list of the checked values of a proposed obstacle coordinates.

        Summary
        -------
        Checks if the proposed obstacle coordinates are not overlapping any
        already existing obstacles.

        """
        x = coordList[0]
        y = coordList[1]
        w = coordList[2]
        h = coordList[3]

        # Left boundary
        c_tlx = x - self.minD2O
        if c_tlx < 0:
            c_tlx = 0

        # Top boundary
        c_tly = y - self.minD2O
        if c_tly < 0:
            c_tly = 0

        # Right boundary
        c_brx = x + w + self.minD2O
        if c_brx > len(self.gameMap[0]):
            c_brx = len(self.gameMap[0])
            w = c_brx - x

        # Bottom boundary
        c_bry = y + h + self.minD2O
        if c_bry > len(self.gameMap):
            c_bry = len(self.gameMap)
            h = c_bry - y

        # If the point at coordinates i, j is already an obstacle
        # (defined by the value 1), we can not place another obstacle on top.
        for i in range(c_tly, c_bry):
            for j in range(c_tlx, c_brx):
                if self.gameMap[i][j] != 0:
                    return None
        return [x, y, w, h]

    def generateObstacle(self, ObsAsList):
        """

        Parameters
        ----------
        ObsAsList : list
            The coordinates of the obstacle to generate as a list.

        Returns
        -------
        None.

        Summary
        -------
        Sets the value of each point of the grid within the obstacle to 1.
        Creates a polygon from the coordinates list, adds it to the polygonlist.

        """
        x = ObsAsList[0]
        y = ObsAsList[1]
        w = ObsAsList[2]
        h = ObsAsList[3]
        poly = QPolygonF()

        # Sets the value of each point within the polygon to one in the map grid.
        for i in range(y, y + h):
            for j in range(x, x + w):
                self.gameMap[i][j] = 1

        # Creates the polygon that will be used for display
        polyTL = QPoint(x * self.mapS, y * self.mapS)
        polyBL = QPoint(x * self.mapS, (y + h) * self.mapS)
        polyBR = QPoint((x + w) * self.mapS, (y + h) * self.mapS)
        polyTR = QPoint((x + w) * self.mapS, y * self.mapS)

        poly<<polyTL<<polyBL<<polyBR<<polyTR

        # Adds it to the polygonList holding every obstacles polygon.
        self.polygonsList.append(poly)

        # Updates the map obstruction percentage
        oA = w * h  # Obstacle area
        oP = oA / self.mapA  # the obstruction percentage of this obstacle on the map
        self.curO += oP

    def generateMap(self):
        """

        Returns
        -------
        list
            The list of all generated obstacles polygons.

        Summary
        -------
        The main cycle generating obstacles on the map.

        """
        sTime = time.time()
        safeCounter = 0

        # Continues to propose and generate obstacles as long as the maximum
        # map obstruction percentage is not reached, or as long as the number
        # of iterations does not surpass the emergency break
        while self.curO < self.maxO:
            # Proposes a random obstacle
            curObs = self.randomObstacle()
            # Checks if the proposed obstacle is valid (no overlap)
            okObs = self.checkAvailableSpace(curObs)
            if okObs is not None:
                # If it is valid, generates the obstacle
                self.generateObstacle(okObs)
                self.nObstacles += 1
            safeCounter += 1
            # Safe break to break out of the loop
            if safeCounter > self.emergencyBreak:
                break
        print("** GENERATED GAME MAP IN %s SECONDS **" % (time.time() - sTime))
        # returns a list of polygon. This list is only used for display.
        return self.polygonsList


class Node(HEAP.HEAPItem):
    """

    A class to define nodes, objects used by the pathfinding algorithm.

    ...

    Attributes
    ----------
    iGrid : int
        The position in the main list.

    jGrid : int
        The position in a sublist of the main list.

    xPos : int
        The x position in the game scene.

    yPos : int
        The y position in the game scene.

    traversible : bool
        The traversability of the node.

    gCost : int
        The cost of moving to this node.

    hCost : int
        The distance of this node to the target node.

    parent : Node
        The node we moved from to reach this node.

    Methods
    -------
    __init__(iGrid : int, jGrid : int, mapSlicing : int, traversible : bool)
        The constructor of the class.

    fCost()
        Returns the Fcost of this node.

    clearCosts()
        Clears all the costs of this node.

    compareTo(otherNode : Node)
        Compare this node to otherNode using their Fcosts.

    """

    iGrid = 0
    jGrid = 0
    xPos = 0
    yPos = 0
    traversible = True
    gCost = 0
    hCost = 0
    parent = None

    def __init__(self, iGrid, jGrid, mapSlicing, traversible):
        """

        Parameters
        ----------
        iGrid : int
            The position in the main list ([HERE][j]).
        jGrid : int
            The position in a sublist of the main list ([i][HERE]).
        mapSlicing : int
            The resolution of the map.
        traversible : bool
            True if the value of map[i][j] is 0, False otherwise.

        Returns
        -------
        None.

        Summary
        -------
        Creates a Node at the given grid position, and defines if it is traversible.

        """
        super(Node, self).__init__()

        self.iGrid = iGrid
        self.jGrid = jGrid
        self.xPos = self.jGrid * mapSlicing
        self.yPos = self.iGrid * mapSlicing
        self.traversible = traversible

    def fCost(self):
        """

        Returns
        -------
        int
            The Fcost of this node.

        Summary
        -------
        Returns the Fcost of the node. The fCost is an evaulation of how promising
        the node is to find the optimum path.

        """
        return int(self.gCost + self.hCost)

    def clearCosts(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Clears costs of the node.

        """
        self.gCost = 0
        self.hCost = 0

    def compareTo(self, otherNode):
        """

        Parameters
        ----------
        otherNode : Node
            The other node to compare this node to.

        Returns
        -------
        int
            The result of the comparison.

        Summary
        -------
        Compares the nodes according to their Fcost.
        Returns 1 if Fcost of this node is lower, -1 if higher.
        Special case if both Fcosts are equal. See function in line comments.

        """
        # If the current node has a lower Fcost than the node's Fcost it is compared to.
        if self.fCost() < otherNode.fCost():
            return 1
        # If the current node has the same Fcost as the node's Fcost it is compared to.
        elif self.fCost() == otherNode.fCost():
            if self.hCost < otherNode.hCost:
                return 1
            else:
                return -1
            return 0
        # If the current node has a higher Fcost than the node's Fcost it is compared to.
        else:
            return -1


class Astar():
    """

    A class implementing the A* algorithm to find an optimal path between two
    points of the world.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    __init__(gameMap : list of lists, mapSlicing : int)
        The constructor of the class.

    getNode(i : int, j : int)
        Gets the node at position (i, j).

    getNeighbours(node : Node)
        Gets the neighbours of node.

    distanceB2Nodes(nodeA : Node, nodeB, Node)
        Returns the distance between node A and nodeB.

    retracePath(startNode : Node, endNode : Node)
        Updates the path with a list of Nodes to go through in order to get from
        startNode to endNode.

    findPath(startPos : QPointF, targetPos : QPointF)
        Uses an A* algorithm to find the optimal path from startPos to targetPos.

    """

    def __init__(self, gameMap, mapSlicing):
        """

        Parameters
        ----------
        gameMap : list
            The gameMap as a nested list.
        mapSlicing : int
            The resolution of the map.

        Returns
        -------
        None.

        Summary
        -------
        The construtor of the class.

        """
        sTime = time.time()
        self.gridS = mapSlicing
        self.allNodes = []
        self.openList = HEAP.HEAP()  # A special set to optimize the sorting of nodes
        self.closedList = []
        self.finalPath = []
        self.currentNode = None

        for i in range(len(gameMap)):
            self.allNodes.append([])
            for j in range(len(gameMap[0])):
                traversible = True if (gameMap[i][j] == 0) else False
                self.allNodes[i].append(Node(i, j, self.gridS, traversible))

        print("***** INITIALIZED A* IN %s SECONDS *****" % (time.time() - sTime))

    def getNode(self, i, j):
        """

        Parameters
        ----------
        i : int
            The l position in the matrix gridS(l,m).
        j : int
            The m position in the matrix gridS(l,m).

        Returns
        -------
        Node
            The node at the location gridS(i, j).

        Summary
        -------
        Returns the node at the location gridS(i, j).

        """
        return self.allNodes[i][j]

    def getNeighbours(self, node):
        """

        Parameters
        ----------
        node : Node
            The node to get the neighbours of.

        Returns
        -------
        neighbours : list of Nodes
            A list of neighbours nodes of node.

        Summary
        -------
        Retrieves all neighbouring nodes of node if they exist and returns a list
        with all of them.

        """
        ##############################
        #
        # neighbour(i-1, j-1) neighbour(i-1, j) neighbour(i-1, j+1)
        # neighbour(i, j-1)       node(i, j)    neighbour(i, j+1)
        # neighbour(i+1, j-1) neighbour(i+1, j) neighbour(i+1, j+1)
        #
        ##############################
        iMin = node.iGrid - 1
        iMax = node.iGrid + 1
        jMin = node.jGrid - 1
        jMax = node.jGrid + 1
        neighbours = []

        if node.iGrid == 0:
            iMin = node.iGrid
        if node.iGrid == (len(self.allNodes) - 1):
            iMax = node.iGrid
        if node.jGrid == 0:
            jMin = node.jGrid
        if node.jGrid == (len(self.allNodes[0]) - 1):
            jMax = node.jGrid

        for i in range(iMin, iMax + 1):
            for j in range(jMin, jMax + 1):
                if (i == node.iGrid) & (j == node.jGrid):
                    # This is the actual node
                    continue
                else:
                    neighbours.append(self.allNodes[i][j])
        return neighbours

    def distanceB2Nodes(self, nodeA, nodeB):
        """

        Parameters
        ----------
        nodeA : Node
            A node.
        nodeB : Node
            A node.

        Returns
        -------
        int
            The distance between nodeA and nodeB.

        Summary
        -------
        Evaluates the distance between noddeA and nodeB.

        """
        distJ = int(abs(nodeB.jGrid - nodeA.jGrid))  # distance on X
        distI = int(abs(nodeB.iGrid - nodeA.iGrid))  # distance on Y

        if distJ > distI:
            return int(14 * distI + 10 * (distJ - distI))
        return int(14 * distJ + 10 * (distI - distJ))

    def retracePath(self, startNode, endNode):
        """

        Parameters
        ----------
        startNode : Node
            The node to start the path from.
        endNode : Node
            The end node to reach.

        Returns
        -------
        None.

        Summary
        -------
        Computes a path form startNode to startNode by retrieving the parents
        of the nodes.
        endNode leads to its parent node, whose parent node leads to its parent
        node etc... until we reach startNode.

        """
        currentNode = endNode

        while currentNode != startNode:
            self.finalPath.append(currentNode)
            currentNode = currentNode.parent

        self.finalPath.reverse()

    def findPath(self, startPos, targetPos):
        """

        Parameters
        ----------
        startPos : QPointF()
            Game scene start position for the pathfinder.
        targetPos : QPointF()
            Game scene target position for the pathfinder.

        Returns
        -------
        list of Nodes
            The list of nodes to go through to reach targetPos from startPos.

        Summary
        -------
        The main A* algorithm which computes the optimal path from startPos to
        targetPos.

        """
        sTime = time.time()
        # Converts from game scene position to grid position
        startNode = self.getNode(int(startPos.y() / self.gridS),
                                 int(startPos.x() / self.gridS))
        targetNode = self.getNode(int(targetPos.y() / self.gridS),
                                  int(targetPos.x() / self.gridS))

        # We always start by ading the startNode to the openList.
        self.openList.addItem(startNode)

        while self.openList.size() > 0:
            # We get the current best node of the open list, add it to the closed
            # list (because all neighbours will be explored further down the code)
            # and remove it from the openList
            self.currentNode = self.openList.removeFirst()
            self.closedList.append(self.currentNode)

            # If current node is the target node, bingo, we found the path !!
            if self.currentNode == targetNode:
                # We retrace the path using each nodes parents
                self.retracePath(startNode, targetNode)
                print("***** FOUND PATH IN %s SECONDS *****" % (time.time() - sTime))
                return self.finalPath
            else:
                # We get all neighbours of the node being evaluated
                neighboursList = self.getNeighbours(self.currentNode)
                for node in neighboursList:
                    # If this particular node is not taversible or already
                    # evaluated, we skip it
                    if (node.traversible is False) | (node in self.closedList):
                        continue

                    # This node gCost is the distance between him and the current
                    # node we are at
                    newMoveCost = self.currentNode.gCost + self.distanceB2Nodes(self.currentNode, node)
                    # If the new move cost is lower than the node current gCost
                    # or if it is not in the openList, we update its data
                    if (newMoveCost < node.gCost) | (node not in self.openList.items):
                        node.gCost = newMoveCost
                        node.hCost = self.distanceB2Nodes(node, targetNode)
                        node.parent = self.currentNode
                        if node not in self.openList.items:
                            self.openList.addItem(node)
