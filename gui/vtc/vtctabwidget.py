import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from . import vtctabbar
from . import icons_rc


class VtcTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(VtcTabWidget, self).__init__(parent)
        tabBar = vtctabbar.VtcTabBar(self)
        self.setTabBar(tabBar)
        self.setTabPosition(QTabWidget.West)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(100, 100, 840, 400)
    tabWidget = VtcTabWidget(window)
    tabWidget.addTab(QLabel("Test"), QIcon(":icons/electrum-vtc.png"), "Test")
    tabWidget.addTab(QLabel("Test 2"), "Test 2")
    window.setCentralWidget(tabWidget)
    window.show()
    app.exec_()
