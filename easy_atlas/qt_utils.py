from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import maya.cmds as cmds

from .EAGlobals import PythonVersion_Major


def parse_type(ptr):
    if PythonVersion_Major <= 2:
        return long(ptr)
    return int(ptr)


class RawWidget:
    """Auxiliary class that is used to grab widgets."""

    def __init__(self, name, type):
        self.name = name
        self.type = type


def loadQtWindow(uiFile, windowName):
    """Auxiliary method that loads .ui files under main Maya window."""
    # Delete previously loaded UI
    if (cmds.window(windowName, exists = True)):
        cmds.deleteUI(windowName)

    # Define Maya window
    global mayaMainWindow
    mayaMainWindow = None
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(parse_type(mayaMainWindowPtr), QWidget)

    # Load UI
    loader = QUiLoader()
    file = QFile(uiFile)
    file.open(QFile.ReadOnly)
    windowUI = loader.load(file, parentWidget = mayaMainWindow)
    file.close()

    return windowUI


def getControl(rawWidget):
    """Auxiliary method to grab a widget."""
    ptr = None
    if rawWidget.type == QAction:
        ptr = omui.MQtUtil.findMenuItem(rawWidget.name)
    else:
        ptr = omui.MQtUtil.findControl(rawWidget.name)
    foundControl = wrapInstance(parse_type(ptr), rawWidget.type)
    return foundControl
