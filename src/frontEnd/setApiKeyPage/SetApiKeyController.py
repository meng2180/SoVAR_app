from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from logicProcess.infoExtract.KeyService import saveKey, getKey
from src.frontEnd.setApiKeyPage.SetApiKeyPage import SetApiKeyPage


class SetApiKeyController(QMainWindow, SetApiKeyPage):
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
        self.lineEditNewKey.setText(getKey())

    def bind(self):
        self.pushButtonClose.clicked.connect(self.closeWindow)
        self.pushButtonSetNewKey.clicked.connect(self.setNewApiKey)

    def setNewApiKey(self):
        key = self.lineEditNewKey.text()
        if key is None or len(key) == 0:
            QMessageBox.warning(self, 'waring', 'API key must not be blank!')
        else:
            saveKey(key)
            QMessageBox.information(self, 'info', 'API Key set successfully!')

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