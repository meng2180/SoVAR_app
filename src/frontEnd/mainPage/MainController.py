import json
import os
from tkinter import Tk

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QFont, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QPushButton, QLabel, QWidget, QVBoxLayout
from PyQt5 import QtGui, QtCore
from matplotlib import pyplot as plt

from logicProcess.infoExtract.InfoService import extractInfo, getInfoExtractRecord, saveInfoExtractRecord
from logicProcess.simulateTest.TestService import reconstructTest, simulateTest
from logicProcess.simulateTest.request.ReconstructRequest import ReconstructRequest
from logicProcess.simulateTest.request.SimulateRequest import SimulateRequest
from logicProcess.useCaseGenerate.MapService import getMap, searchMapInfo
from src.common.constants import ACTION_SELECTOR, DIRECTION_SELECTOR, ROAD_TYPE_SELECTOR, CAR_COUNT_SELECTOR, \
    LANE_COUNT_SELECTOR, LANE_SELECTOR, ERROR, EGO_SELECTOR, MAP_DICT, WEATHER_SELECTOR, SUNNY, STRIKER_SELECTOR, \
    IMPACT_PART_SELECTOR, ROOT_PATH

from src.entity.CrashInfo import CrashInfo
from src.frontEnd.mainPage.MainPage import MainPage
from logicProcess.useCaseGenerate.UseCaseService import generate


WINDOW_ICON_FILE_PATH = os.path.join(ROOT_PATH, "resource/icon/windowIcon.png")

COPY_ICON_FILE_PATH = os.path.join(ROOT_PATH, "resource/icon/copyIcon.png")


class MainController(QMainWindow, MainPage):
    switch_window_to_setApiKey = QtCore.pyqtSignal()
    switch_window_to_setMap = QtCore.pyqtSignal()
    switch_window_to_setModel = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.windowIconLabel = None
        self.barWidget = None
        self.pushButtonClose = None
        self.pushButtonMin = None
        self.titleLabel = None
        self.waypointList = None
        self.isFan = None
        self.isSingle = None
        self.carCount = None
        self.weatherList = [SUNNY]
        self.crashInfo = None
        self.setupUi(self)
        self.initUI()
        self.bind()

    def initUI(self):
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(self.width(), self.height())

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(16)
        font.setBold(True)

        self.pushButtonClose = QPushButton(self)
        self.pushButtonClose.setGeometry(QtCore.QRect(990, 0, 50, 44))
        self.pushButtonClose.setText("×")
        self.pushButtonClose.setFont(font)
        self.pushButtonClose.setStyleSheet("QPushButton{\ncolor:rgb(236, 236, 236);\nborder:none;\nbackground:transparent;\n}\nQPushButton::pressed\n{\nbackground-color:rgb(233,16,34);\n}")

        self.pushButtonMin = QPushButton(self)
        self.pushButtonMin.setGeometry(QtCore.QRect(940, 0, 50, 44))
        self.pushButtonMin.setText("-")
        self.pushButtonMin.setFont(font)
        self.pushButtonMin.setStyleSheet("QPushButton{\ncolor:rgb(236, 236, 236);\nborder:none;\nbackground:transparent;\n}\nQPushButton::pressed\n{\nbackground-color:rgb(20, 136, 208);\n}")

        self.windowIconLabel = QLabel(self)
        self.windowIconLabel.setGeometry(QtCore.QRect(250, 0, 44, 44))
        self.windowIconLabel.setStyleSheet("background:transparent")
        windowIcon = QIcon(WINDOW_ICON_FILE_PATH)
        self.windowIconLabel.setPixmap(windowIcon.pixmap(windowIcon.actualSize(QSize(44, 44))))

        copyIcon = QIcon(COPY_ICON_FILE_PATH)
        self.labelCopyInfoGPT.setPixmap(copyIcon.pixmap(copyIcon.actualSize(QSize(44, 44))))
        self.labelCopyWaypoint.setPixmap(copyIcon.pixmap(copyIcon.actualSize(QSize(44, 44))))
        self.labelCopyInfoGT.setPixmap(copyIcon.pixmap(copyIcon.actualSize(QSize(44, 44))))
        self.labelCopyRate.setPixmap(copyIcon.pixmap(copyIcon.actualSize(QSize(44, 44))))

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)

        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(QtCore.QRect(300, 0, 550, 44))
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setStyleSheet("background:transparent")
        self.titleLabel.setFont(font)
        self.titleLabel.setText("Automatic Driving Software Test Case Generation System")

        self.comboBoxCarCount.addItems(CAR_COUNT_SELECTOR)
        self.comboBoxRoadType.addItems(ROAD_TYPE_SELECTOR)
        self.comboBoxLaneCount.addItems(LANE_COUNT_SELECTOR)
        self.comboBoxV1Direction.addItems(DIRECTION_SELECTOR)
        self.comboBoxV1Lane.addItems(LANE_SELECTOR)
        self.comboBoxV1Action.addItems(ACTION_SELECTOR)
        self.comboBoxV1TargetLane.addItems(LANE_SELECTOR)
        self.comboBoxV2Direction.addItems(DIRECTION_SELECTOR)
        self.comboBoxV2Lane.addItems(LANE_SELECTOR)
        self.comboBoxV2Action.addItems(ACTION_SELECTOR)
        self.comboBoxV2TargetLane.addItems(LANE_SELECTOR)
        self.comboBoxEgo.addItems(EGO_SELECTOR)
        self.comboBoxWeather.addItems(WEATHER_SELECTOR)
        self.comboBoxStriker.addItems(STRIKER_SELECTOR)
        self.comboBoxImpactPart.addItems(IMPACT_PART_SELECTOR)
        self.lineEditWeather.setText(self.weatherText())
        self.comboBoxCarCount.setCurrentIndex(1)

        self.showBarFigure()

    def bind(self):
        self.actionImport.triggered.connect(self.importReport)
        self.actionGenerate.triggered.connect(self.generate)
        self.actionPreview.triggered.connect(self.preview)
        self.actionSimulate.triggered.connect(self.simulate)
        self.actionTest.triggered.connect(self.test)
        self.actionApiKey.triggered.connect(self.showSetApiKey)
        self.actionMap.triggered.connect(self.showSetMap)
        self.actionModel.triggered.connect(self.showSetModel)
        self.pushButtonClose.clicked.connect(self.closeWindow)
        self.pushButtonMin.clicked.connect(self.minWindow)
        self.comboBoxCarCount.currentIndexChanged.connect(self.handleLaneCountChanged)
        self.comboBoxWeather.activated.connect(self.handleWeatherSelected)


    def copyInfoGPT(self):
        copy(self.textBrowserInfo.toPlainText())
        self.showMsgBox('info', 'Report extraction result has been copied to the clipboard!')

    def copyInfoGT(self):
        copy(json.dumps(self.buildCrashInfoFromGT(), default=serializeCrashInfo, indent=8, ensure_ascii=False))
        self.showMsgBox('info', 'The truth configuration has been copied to the clipboard!')

    def copyWaypoint(self):
        copy(self.textBrowserWaypoint.toPlainText())
        self.showMsgBox('info', 'The test case has been copied to the clipboard!')

    def copyRate(self):
        copy(json.dumps(getInfoExtractRecord()))
        self.showMsgBox('info', 'The accuracy rate has been copied to the clipboard!')

    def importReport(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "choose report(only support txt)", "", "*.txt")
        if not filePath:
            return

        err, result = extractInfo(filePath)
        if err:
            self.showMsgBox('warning', 'Error in calling large model!\n' + result)
            return

        self.crashInfo = result
        self.textBrowserInfo.setText(json.dumps(result, default=serializeCrashInfo, indent=8, ensure_ascii=False))

        if self.checkBoxAddToRecord.isChecked():
            self.addToInfoExtractRecord(result)

        self.showMsgBox('info', 'Information extraction succeeded!')


    def addToInfoExtractRecord(self, crashInfoGPT):
        crashInfoGT = self.buildCrashInfoFromGT()

        record = getInfoExtractRecord()

        record["carCount"][1] += 1
        record["roadType"][1] += 1
        record["laneCount"][1] += 1
        record["weather"][1] += 1
        record["striker"][1] += 1
        record["impactPart"][1] += 1
        record["direction"][1] += 1
        record["lane"][1] += 1
        record["action"][1] += 1
        record["targetLane"][1] += 1

        if crashInfoGT.carCount == crashInfoGPT.carCount:
            record["carCount"][0] += 1
        if crashInfoGT.roadType == crashInfoGPT.roadType:
            record["roadType"][0] += 1
        if crashInfoGT.laneCount == crashInfoGPT.laneCount:
            record["laneCount"][0] += 1
        elif len(searchMapInfo(crashInfoGT.roadType, crashInfoGT.laneCount)) == 0 and crashInfoGPT.laneCount == 2:
            record["laneCount"][0] += 1
        if crashInfoGT.weather == crashInfoGPT.weather:
            record["weather"][0] += 1
        if crashInfoGT.striker == crashInfoGPT.striker:
            record["striker"][0] += 1
        if crashInfoGT.impactPart == crashInfoGPT.impactPart:
            record["impactPart"][0] += 1

        if crashInfoGT.v1Direction == crashInfoGPT.v1Direction:
            record["direction"][0] += 1
        if crashInfoGT.v1Lane == crashInfoGPT.v1Lane:
            record["lane"][0] += 1
        elif len(searchMapInfo(crashInfoGT.roadType, crashInfoGT.v1Lane)) == 0 and crashInfoGPT.v1Lane == 2:
            record["lane"][0] += 1
        if crashInfoGT.v1Action == crashInfoGPT.v1Action:
            record["action"][0] += 1
        if crashInfoGT.v1TargetLane == crashInfoGPT.v1TargetLane:
            record["targetLane"][0] += 1
        elif len(searchMapInfo(crashInfoGT.roadType, crashInfoGT.v1TargetLane)) == 0 and crashInfoGPT.v1TargetLane == 2:
            record["targetLane"][0] += 1

        if crashInfoGT.carCount == 2:
            record["direction"][1] += 1
            record["lane"][1] += 1
            record["action"][1] += 1
            record["targetLane"][1] += 1

            if crashInfoGT.v2Direction == crashInfoGPT.v2Direction:
                record["direction"][0] += 1
            if crashInfoGT.v2Lane == crashInfoGPT.v2Lane:
                record["lane"][0] += 1
            elif len(searchMapInfo(crashInfoGT.roadType, crashInfoGT.v2Lane)) == 0 and crashInfoGPT.v2Lane == 2:
                record["lane"][0] += 1
            if crashInfoGT.v2Action == crashInfoGPT.v2Action:
                record["action"][0] += 1
            if crashInfoGT.v2TargetLane == crashInfoGPT.v2TargetLane:
                record["targetLane"][0] += 1
            elif len(searchMapInfo(crashInfoGT.roadType, crashInfoGT.v2TargetLane)) == 0 and crashInfoGPT.v2TargetLane == 2:
                record["targetLane"][0] += 1

        saveInfoExtractRecord(str(record).replace("\'", "\""))
        self.showBarFigure()

    def weatherText(self):
        return ",".join(self.weatherList)

    def handleLaneCountChanged(self):
        if self.comboBoxCarCount.currentIndex() == 0:
            self.setV2Visible(False)
        else:
            self.setV2Visible(True)

    def handleWeatherSelected(self):
        weather = self.comboBoxWeather.currentText()
        if weather in self.weatherList:
            self.weatherList.remove(weather)
        else:
            self.weatherList.append(weather)
        self.lineEditWeather.setText(self.weatherText())

    def setV2Visible(self, visible):
        self.labelV2Direction.setVisible(visible)
        self.comboBoxV2Direction.setVisible(visible)
        self.labelV2Lane.setVisible(visible)
        self.comboBoxV2Lane.setVisible(visible)
        self.labelV2Action.setVisible(visible)
        self.comboBoxV2Action.setVisible(visible)
        self.labelV2TargetLane.setVisible(visible)
        self.comboBoxV2TargetLane.setVisible(visible)
        self.labelV2Speed.setVisible(visible)
        self.spinBoxV2Speed.setVisible(visible)

    def generate(self):
        if self.checkBoxAddToGenerate.isChecked():
            crashInfo = self.buildCrashInfoFromGT()
        else:
            if self.crashInfo is None:
                self.showMsgBox('warning', 'Please import the report first or use the true value for test case generation!')
                return
            else:
                crashInfo = self.crashInfo

        self.carCount = crashInfo.carCount
        self.waypointList, self.isFan, self.isSingle = generate(crashInfo)
        if self.waypointList == ERROR:
            self.showMsgBox('info', 'Error in information, unable to generate test case!')
        else:
            self.showWaypoint()
            self.showMsgBox('info', 'Test case generated successfully!')

    def buildCrashInfoFromGT(self):
        crashInfo = CrashInfo(None)
        crashInfo.weather = self.weatherList
        crashInfo.roadType = self.comboBoxRoadType.currentText()
        crashInfo.carCount = int(self.comboBoxCarCount.currentText())
        crashInfo.laneCount = int(self.comboBoxLaneCount.currentText())
        crashInfo.striker = self.comboBoxStriker.currentText()
        crashInfo.impactPart = self.comboBoxImpactPart.currentIndex() + 1
        crashInfo.v1Direction = self.comboBoxV1Direction.currentIndex() + 1
        crashInfo.v1Lane = int(self.comboBoxV1Lane.currentText())
        crashInfo.v1Action = self.comboBoxV1Action.currentText()
        crashInfo.v1TargetLane = int(self.comboBoxV1TargetLane.currentText())
        crashInfo.v2Direction = self.comboBoxV2Direction.currentIndex() + 1
        crashInfo.v2Lane = int(self.comboBoxV2Lane.currentText())
        crashInfo.v2Action = self.comboBoxV2Action.currentText()
        crashInfo.v2TargetLane = int(self.comboBoxV2TargetLane.currentText())
        crashInfo.v1Speed = self.spinBoxV1Speed.value()
        crashInfo.v2Speed = self.spinBoxV2Speed.value()
        return crashInfo

    def showWaypoint(self):
        self.textBrowserWaypoint.setText("V1: \n" + json.dumps(self.waypointList[0], indent=8))
        if self.carCount == 1:
            self.textBrowserWaypoint.append("\nPedestrain: \n" + json.dumps(self.waypointList[1], indent=8))
        else:
            self.textBrowserWaypoint.append("\nV2: \n" + json.dumps(self.waypointList[1], indent=8))

    def preview(self):
        if self.waypointList is None or len(self.waypointList) == 0:
            self.showMsgBox("warining", "Please generate test case first!")
            return

        fig = plt.figure()
        fig.canvas.manager.set_window_title("Test Case Preview")

        marker = ['*', 'o']
        color = ['b', 'r']
        label = ['V1']
        if self.carCount == 1:
            label.append('Pedestrain')
        else:
            label.append('V2')

        for i in range(2):
            xList = []
            yList = []
            for waypoint in self.waypointList[i]:
                xList.append(waypoint[0])
                yList.append(waypoint[1])
            plt.plot(xList, yList, label=label[i], marker=marker[i], linestyle="-", color=color[i])
        plt.legend()
        plt.axis('equal')
        plt.rcParams['font.sans-serif'] = ['simHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.show()

    def simulate(self):
        if self.waypointList is None or len(self.waypointList) == 0:
            self.showMsgBox("warning", "Please generate test case first!")
            return

        selectedMapName = getMap()
        if selectedMapName not in MAP_DICT:
            self.showMsgBox("warning", "LGSVL is not compatible with custom added maps!")
            return

        try:
            reconstructRequest = ReconstructRequest(self.waypointList, self.isFan, self.isSingle, self.weatherList, MAP_DICT[selectedMapName])
            reconstructTest(reconstructRequest)
        except Exception:
            self.showMsgBox('warning', 'Simulator connection failed!')

    def test(self):
        if self.waypointList is None or len(self.waypointList) == 0:
            self.showMsgBox("warning", "Please generate test case first!")
            return

        selectedMapName = getMap()
        if selectedMapName not in MAP_DICT:
            self.showMsgBox("warning", "LGSVL is not compatible with custom added maps!")
            return

        try:
            simulateRequest = SimulateRequest(self.waypointList, self.isFan, self.isSingle, self.weatherList, selectedMapName, MAP_DICT[selectedMapName], self.comboBoxEgo.currentText())
            simulateTest(simulateRequest)
        except BaseException:
            self.showMsgBox('warning', 'Simulator connection failed!')

    def showSetApiKey(self):
        self.switch_window_to_setApiKey.emit()

    def showSetMap(self):
        self.switch_window_to_setMap.emit()

    def showSetModel(self):
        self.switch_window_to_setModel.emit()

    def showMsgBox(self, title, content):
        msgBox = QMessageBox()
        msgBox.setStyleSheet("background-color:rgb(255,255,255)")
        QMessageBox.information(msgBox, title, content)

    def closeWindow(self):
        self.close()

    def minWindow(self):
        self.showMinimized()

    def showBarFigure(self):
        log = getInfoExtractRecord()

        data = [
            ("CarCount: ", log["carCount"][0], log["carCount"][1]),
            ("RoadType: ", log["roadType"][0], log["roadType"][1]),
            ("LaneCount: ", log["laneCount"][0], log["laneCount"][1]),
            ("Weather: ", log["weather"][0], log["weather"][1]),
            ("Striker: ", log["striker"][0], log["striker"][1]),
            ("HitPart: ", log["impactPart"][0], log["impactPart"][1]),
            ("Direction: ", log["direction"][0], log["direction"][1]),
            ("Lane: ", log["lane"][0], log["lane"][1]),
            ("Action: ", log["action"][0], log["action"][1]),
            ("TargetLane: ", log["targetLane"][0], log["targetLane"][1])
        ]

        color = QColor(20, 136, 208)
        colors = []
        for i in range(10):
            colors.append(color)

        layout = QVBoxLayout()
        layout.addWidget(HorizontalBarChart(data, colors, 1.4))

        self.barWidget.setLayout(layout)


    _startPos = None
    _endPos = None
    _isTracking = None

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        objectName = self.childAt(a0.pos().x(), a0.pos().y()).objectName()
        if a0.button() == QtCore.Qt.LeftButton:
            if objectName == "titleLabel":
                self._isTracking = True
                self._startPos = QtCore.QPoint(a0.x(), a0.y())
            if objectName == "labelCopyInfoGPT":
                self.copyInfoGPT()
            if objectName == "labelCopyInfoGT":
                self.copyInfoGT()
            if objectName == "labelCopyWaypoint":
                self.copyWaypoint()
            if objectName == "labelCopyRate":
                self.copyRate()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if a0.button() == QtCore.Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None


def caculateRate(rightCount, totalCount):
    if totalCount == 0:
        return 1
    return round(1.0 * rightCount / totalCount, 3)


def copy(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()


def serializeCrashInfo(obj):
    if isinstance(obj, CrashInfo):
        return {
            "weather": obj.weather,
            "roadType": obj.roadType,
            "carCount": obj.carCount,
            "laneCount": obj.laneCount,
            "striker": obj.striker,
            "impactPart": obj.impactPart,
            "v1Direction": obj.v1Direction,
            "v1Lane": obj.v1Lane,
            "v1Action": obj.v1Action,
            "v1TargetLane": obj.v1TargetLane,
            "v2Direction": obj.v2Direction,
            "v2Lane": obj.v2Lane,
            "v2Action": obj.v2Action,
            "v2TargetLane": obj.v2TargetLane
        }
    raise TypeError("Type not serializable")


class HorizontalBarChart(QWidget):
    def __init__(self, data, colors, max_value, parent=None):
        super().__init__(parent)
        self.data = data
        self.colors = colors
        self.max_value = max_value
        self.bar_height = 30
        self.bar_spacing = 20
        self.top_margin = 10
        self.left_margin = 115

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawBars(painter)

    def drawBars(self, painter):
        font = QFont("微软雅黑", 10)
        painter.setFont(font)

        for i, (label, curCount, total) in enumerate(self.data):
            value = caculateRate(curCount, total)
            bar_width = int((value / self.max_value) * (self.width() - self.left_margin - 20))

            painter.setBrush(QColor(self.colors[i]))
            painter.setPen(Qt.black)
            painter.drawRect(
                self.left_margin,
                self.top_margin + i * (self.bar_height + self.bar_spacing),  # y 起点
                bar_width,
                self.bar_height
            )

            painter.drawText(
                10,
                self.top_margin + i * (self.bar_height + self.bar_spacing) + int(self.bar_height * 0.75),  # y 起点
                label
            )

            painter.drawText(
                self.left_margin + bar_width + 10,
                self.top_margin + i * (self.bar_height + self.bar_spacing) + int(self.bar_height * 0.75),  # y 起点
                str(value) + "(" + str(curCount) + "/" + str(total) + ")"
            )
