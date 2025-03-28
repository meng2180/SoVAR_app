import os
import shutil

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from common.constants import ROOT_PATH
from frontEnd.setMapPage.SetMapPage import SetMapPage
from logicProcess.useCaseGenerate.MapService import getMap, saveMap, getMapList, saveMapList


class SetMapController(QMainWindow, SetMapPage):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.bind()

    def initUI(self):
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.comboBoxMap.addItems(getMapList())
        self.showMap()

    def bind(self):
        self.pushButtonClose.clicked.connect(self.closeWindow)
        self.pushButtonSetNewMap.clicked.connect(self.setNewMap)
        self.linkButtonAddMap.clicked.connect(self.addMap)

    def addMap(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "choose report(only support txt)", "", "*.xodr")
        if not filePath:
            return

        mapList = getMapList()

        fileBaseName = os.path.basename(filePath)
        fileName = fileBaseName.split(".")[0]
        if fileName in mapList:
            QMessageBox.information(self, 'warning', 'The map name is duplicate. Please modify the name!')
            return

        targetFilePath = os.path.join(os.path.join(ROOT_PATH, "resource/maps/"), fileBaseName)
        shutil.copy(filePath, targetFilePath)

        mapList.append(fileName)
        saveMapList(mapList)

        self.comboBoxMap.clear()
        self.comboBoxMap.addItems(mapList)
        QMessageBox.information(self, 'info', 'Map added successfully!')

    def showMap(self):
        self.comboBoxMap.setCurrentText(getMap())

    def setNewMap(self):
        selectedMap = self.comboBoxMap.currentText()
        try:
            saveMap(selectedMap)
        except Exception as e:
            QMessageBox.information(self, 'warning', 'Map parsing failed! ' + str(e.args[0]))
            return

        QMessageBox.information(self, 'info', 'Map set successfully!')

    def closeWindow(self):
        self.close()

    _startPos = None
    _endPos = None
    _isTracking = None

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "widget":
            if a0.button() == QtCore.Qt.LeftButton:
                self._isTracking = True
                self._startPos = QtCore.QPoint(a0.x(), a0.y())

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None