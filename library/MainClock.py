# -*- coding: utf-8 -*-

'''
    File name: MainClock.py
    Author: Grégory LARGANGE
    Date created: 08/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 10/12/2020
    Python version: 3.8.1
'''

from PyQt5 import QtCore
from PyQt5.QtCore import QObject


class MainClock(QObject):
    """

    A class to set up the main clock of the game.

    ...

    Attributes
    ----------
    clockSignal : QtCore.pyqtSignal
        A signal to be emmited by the timer.

    elapsedTime : float
        the total time elapsed since last start of the timer.

    Methods
    -------
    raiseTimeout()
        Emit a signal with value True on timeout.

    startClock()
        Starts the timer.

    stopClock()
        Stops the timer.

    """

    clockSignal = QtCore.pyqtSignal(bool)
    elapsedTime = 0  # in ms

    def __init__(self, period, parent=None):
        """

        Parameters
        ----------
        period : int
            The time between two signals of the timer.
        parent : QWidget, optional
            Not used. The default is None.

        Returns
        -------
        None.

        Summary
        -------
        The constructor of the class

        """
        super(MainClock, self).__init__(parent)

        self.fromStop = False
        self.clock = QtCore.QTimer()
        self.clock.setInterval(period)
        self.clock.timeout.connect(self.raiseTimeout)

    @QtCore.pyqtSlot()
    def raiseTimeout(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Emits a signal "True" on timeout.

        """
        self.clockSignal.emit(True)
        self.elapsedTime+=self.clock.interval()
        if not self.fromStop:
            self.clock.start()

    @QtCore.pyqtSlot()
    def startClock(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Starts the timer.

        """
        self.clock.start()
        self.fromStop = False

    @QtCore.pyqtSlot()
    def stopClock(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Stops the timer

        """
        self.clock.stop()
        self.fromStop = True
