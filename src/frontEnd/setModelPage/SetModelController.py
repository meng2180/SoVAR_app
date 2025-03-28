from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from frontEnd.setModelPage.SetModelPage import SetModelPage
from logicProcess.infoExtract.ModelService import getModelList, getModel, saveModel


class SetModelController(QMainWindow, SetModelPage):
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
        self.comboBoxModel.addItems(getModelList())
        self.showModel()

    def bind(self):
        self.pushButtonClose.clicked.connect(self.closeWindow)
        self.pushButtonSetNewModel.clicked.connect(self.setNewModel)

    def showModel(self):
        self.comboBoxModel.setCurrentText(getModel())

    def setNewModel(self):
        selectedModel = self.comboBoxModel.currentText()
        saveModel(selectedModel)
        QMessageBox.information(self, 'info', 'Model set successfully!')

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