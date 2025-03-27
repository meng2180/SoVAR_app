from frontEnd.mainPage.MainController import MainController
from frontEnd.setApiKeyPage.SetApiKeyController import SetApiKeyController
from frontEnd.setMapPage.SetMapController import SetMapController
from frontEnd.setModelPage.SetModelController import SetModelController


class PageController:
    def __init__(self):
        self.mainController = None
        self.setApiKeyController = None
        self.setMapController = None
        self.setModelController = None

    def showMainPage(self):
        self.mainController = MainController()
        self.mainController.switch_window_to_setApiKey.connect(self.showSetApiKeyPage)
        self.mainController.switch_window_to_setMap.connect(self.showSetMapPage)
        self.mainController.switch_window_to_setModel.connect(self.showSetModelPage)
        self.mainController.show()

    def showSetApiKeyPage(self):
        self.setApiKeyController = SetApiKeyController()
        self.setApiKeyController.show()

    def showSetMapPage(self):
        self.setMapController = SetMapController()
        self.setMapController.show()

    def showSetModelPage(self):
        self.setModelController = SetModelController()
        self.setModelController.show()