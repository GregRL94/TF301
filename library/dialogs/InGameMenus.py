# -*- coding: utf-8 -*-

"""
    File name: dialogsUltils.py
    Author: Grégory LARGANGE
    Date created: 28/06/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 07/07/2021
    Python version: 3.8.1
"""


from PyQt5 import QtCore, QtWidgets


class PauseMenu:
    """

    A class to handle in game pause menus.

    ...

    Methods
    -------
    __init__()
        Constructor of the class.

    pauseMenu()
        Displays the pause menu.

    resumeClicked()
        Sets the return value of pauseMenu to 0.

    optionsClicked()
        Sets the return value of pauseMenu to 1.

    surrenderClicked()
        Sets the return value of pauseMenu to 2.

    """

    RESUME = 0
    OPTIONS = 1
    SURRENDER = 2

    def __init__(self):
        """

        Summary
        -------
        Constructor.

        """
        self.choice = self.RESUME

    def pauseMenuUI(self):
        """

        Returns
        -------
        None.

        Summary
        -------
        Displays the pause menu ui.

        """
        pauseMenu = QtWidgets.QDialog()
        pauseMenu.setObjectName("PauseMenu")
        pauseMenu.resize(260, 260)
        pauseMenu.setMinimumSize(QtCore.QSize(260, 260))
        pauseMenu.setMaximumSize(QtCore.QSize(260, 260))
        pauseMenu.setWindowTitle("BATTLE PAUSED")
        verticalLayout = QtWidgets.QVBoxLayout(pauseMenu)
        verticalLayout.setContentsMargins(9, 9, 9, 9)
        verticalLayout.setSpacing(6)
        verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        verticalLayout.addItem(spacerItem)
        resume_but = QtWidgets.QPushButton(pauseMenu)
        resume_but.setMinimumSize(QtCore.QSize(0, 60))
        resume_but.setObjectName("resume_but")
        resume_but.setText("RESUME")
        verticalLayout.addWidget(resume_but)
        options_but = QtWidgets.QPushButton(pauseMenu)
        options_but.setMinimumSize(QtCore.QSize(0, 60))
        options_but.setObjectName("options_but")
        options_but.setText("OPTIONS")
        verticalLayout.addWidget(options_but)
        surrender_but = QtWidgets.QPushButton(pauseMenu)
        surrender_but.setMinimumSize(QtCore.QSize(0, 60))
        surrender_but.setObjectName("surrender_but")
        surrender_but.setText("SURRENDER")
        verticalLayout.addWidget(surrender_but)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        verticalLayout.addItem(spacerItem1)

        QtCore.QMetaObject.connectSlotsByName(pauseMenu)
        resume_but.clicked.connect(lambda: self.resumeClicked(pauseMenu))
        options_but.clicked.connect(lambda: self.optionsClicked(pauseMenu))
        surrender_but.clicked.connect(lambda: self.surrenderClicked(pauseMenu))

        return (pauseMenu.exec(), self.choice)

    def resumeClicked(self, dialog):
        self.choice = self.RESUME
        dialog.accept()

    def optionsClicked(self, dialog):
        self.choice = self.OPTIONS
        dialog.accept()

    def surrenderClicked(self, dialog):
        self.choice = self.SURRENDER
        dialog.accept()
