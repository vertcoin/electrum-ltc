from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class VtcTabBar(QTabBar):
    def __init__(self, parent=None):
        super(VtcTabBar, self).__init__(parent)
        self.tabSize = QSize(120, 120)

        self.borderColor = QColor(165, 162, 170)
        self.backgroundColor = QColor(30, 24, 43)
        self.firstTabColor = QColor(111, 170, 93)
        self.textColor = self.borderColor
        self.highlightTextColor = Qt.white
        self.highlightColor = QColor(148, 202, 67)

    def tabSizeHint(self, index):
        return self.tabSize

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        for index in range(self.count()):
            self.drawTab(painter, index)

        painter.end()

    def drawTab(self, painter, index):
        rect = self.tabRect(index)
        icon = self.tabIcon(index)
        text = self.tabText(index)
        is_selected = (self.currentIndex() == index)
        is_first_tab = (index == 0)

        self.drawBackground(painter, rect, is_first_tab)

        #text and highlight
        if is_first_tab:
            self.drawText(painter, rect, self.highlightTextColor, text)
        elif is_selected:
            painter.fillRect(rect.x() + 1, rect.y() + 1, 0.05 * rect.width(),
                             rect.height(), self.highlightColor)
            self.drawText(painter, rect, self.highlightTextColor, text)
        else:
            self.drawText(painter, rect, self.textColor, text)

        iconRect = QRect(rect.x() + 0.25 * rect.width(),
                         rect.y() + 0.25 * rect.height(),
                         0.5 * rect.width(),
                         0.5 * rect.height())
        icon.paint(painter, iconRect)

    def drawBackground(self, painter, rect, is_first_tab):
        painter.setPen(self.borderColor)
        if is_first_tab:
            painter.setBrush(QBrush(self.firstTabColor))
        else:
            painter.setBrush(QBrush(self.backgroundColor))
        painter.drawRect(rect)

    def drawText(self, painter, rect, color, text):
        painter.setPen(color)
        textRect = QRect(rect.x(), rect.y() + 0.75 * rect.height(),
                         rect.width(), 0.25 * rect.height())
        painter.drawText(textRect, Qt.AlignCenter, text)
