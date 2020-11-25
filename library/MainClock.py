# -*- coding: utf-8 -*-

'''
    File name: MainClock.py
    Author: Grégory LARGANGE
    Date created: 08/10/2020
    Last modified by: Grégory LARGANGE
    Date last modified: 08/10/2020
    Python version: 3.8.1
'''

from PyQt5 import QtCore
from PyQt5.QtCore import QObject


class MainClock(QObject):

    clockSignal = QtCore.pyqtSignal(bool)
    elapsedTime = 0  # in ms

    def __init__(self, period, parent=None):
        super(MainClock, self).__init__(parent)

        self.fromStop = False
        self.clock = QtCore.QTimer()
        self.clock.setInterval(period)
        self.clock.timeout.connect(self.raiseTimeout)

    @QtCore.pyqtSlot()
    def raiseTimeout(self):
        self.clockSignal.emit(True)
        self.elapsedTime+=self.clock.interval()
        if not self.fromStop:
            self.clock.start()

    @QtCore.pyqtSlot()
    def startClock(self):
        self.clock.start()
        self.fromStop = False

    @QtCore.pyqtSlot()
    def stopClock(self):
        self.clock.stop()
        self.fromStop = True
