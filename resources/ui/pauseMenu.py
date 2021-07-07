# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\grl6abt\Coding_Projects\TaskForce301\resources\ui\pauseMenu.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PauseMenu(object):
    def setupUi(self, PauseMenu):
        PauseMenu.setObjectName("PauseMenu")
        PauseMenu.resize(259, 259)
        PauseMenu.setMinimumSize(QtCore.QSize(259, 259))
        PauseMenu.setMaximumSize(QtCore.QSize(259, 259))
        self.verticalLayout = QtWidgets.QVBoxLayout(PauseMenu)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.resume_but = QtWidgets.QPushButton(PauseMenu)
        self.resume_but.setMinimumSize(QtCore.QSize(0, 60))
        self.resume_but.setObjectName("resume_but")
        self.verticalLayout.addWidget(self.resume_but)
        self.options_but = QtWidgets.QPushButton(PauseMenu)
        self.options_but.setMinimumSize(QtCore.QSize(0, 60))
        self.options_but.setObjectName("options_but")
        self.verticalLayout.addWidget(self.options_but)
        self.leave_but = QtWidgets.QPushButton(PauseMenu)
        self.leave_but.setMinimumSize(QtCore.QSize(0, 60))
        self.leave_but.setObjectName("leave_but")
        self.verticalLayout.addWidget(self.leave_but)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(PauseMenu)
        QtCore.QMetaObject.connectSlotsByName(PauseMenu)

    def retranslateUi(self, PauseMenu):
        _translate = QtCore.QCoreApplication.translate
        PauseMenu.setWindowTitle(_translate("PauseMenu", "BATTLE PAUSED"))
        self.resume_but.setText(_translate("PauseMenu", "RESUME"))
        self.options_but.setText(_translate("PauseMenu", "OPTIONS"))
        self.leave_but.setText(_translate("PauseMenu", "SURRENDER"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PauseMenu = QtWidgets.QDialog()
    ui = Ui_PauseMenu()
    ui.setupUi(PauseMenu)
    PauseMenu.show()
    sys.exit(app.exec_())
