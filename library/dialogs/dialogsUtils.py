# -*- coding: utf-8 -*-

"""
    File name: dialogsUltils.py
    Author: Grégory LARGANGE
    Date created: 28/06/2021
    Last modified by: Grégory LARGANGE
    Date last modified: 28/06/2021
    Python version: 3.8.1
"""


from PyQt5.QtWidgets import QMessageBox

# Constants for icon type
INFORMATION = 0
QUESTION = 1
CRITICAL = 2
WARNING = 3
ICON_TYPE_DICT = {
    INFORMATION: QMessageBox.Information,
    QUESTION: QMessageBox.Question,
    CRITICAL: QMessageBox.Critical,
    WARNING: QMessageBox.Warning,
}

# Constants for message box type
INFORMATION_BOX = 1
CONFIRMATION_BOX = 2


def popMessageBox(
    windowTitle: str,
    iconTypeID: int,
    messageStr: str,
    msgBoxTypeID: int,
    *func: callable
):
    """

    Parameters
    ----------
    windowTitle: string
        The text that will be displayed as title of the box.
    iconTypeID : int
        The icon to be displayed by the message box.
    messageStr : string
        The message string to be displayed by the message box.
    msgBoxTypeID : int
        The ID of the box type to use. 1 for information message box,
        (only Ok interaction) 2 for Confirmation message box (Yes / No).
    *func : function(), optional
        Function called in confirmation message box when user clicks "OK" button

    Returns
    -------
    None.

    Summary
    -------
    Pops a message box.
    Confirmation box can call a function if "Yes" is pressed.

    """
    msgBox = QMessageBox()
    msgBox.setWindowTitle(windowTitle)
    if iconTypeID not in ICON_TYPE_DICT:
        raise ValueError("iconTypeID unknown")
    msgBox.setIcon(ICON_TYPE_DICT[iconTypeID])
    msgBox.setText(messageStr)

    if msgBoxTypeID == INFORMATION_BOX:  # Information box
        msgBox.setStandardButtons(QMessageBox.Ok)
    elif msgBoxTypeID == CONFIRMATION_BOX:  # Confirmation Box
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    else:
        raise ValueError("Message Box ID unknown")

    retval = msgBox.exec_()

    if msgBoxTypeID == INFORMATION_BOX:
        if retval == QMessageBox.Ok:
            msgBox.close()
    elif msgBoxTypeID == CONFIRMATION_BOX:
        if retval == QMessageBox.Ok:
            func[0]()
        else:
            msgBox.close()
