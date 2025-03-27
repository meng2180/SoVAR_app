import sys
from PyQt5.QtWidgets import QApplication
from frontEnd.PageController import PageController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = PageController()
    controller.showMainPage()
    sys.exit(app.exec_())
