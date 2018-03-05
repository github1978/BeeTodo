import sys
from MyWidgets import MyMainWindow, MyToDoUi, QApplication
from StyleSheets import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheets.getCSS('GLOBAL'))
    mainWindow = MyMainWindow()
    ui = MyToDoUi(mainWindow).showMainWindow()
    ui.init()
    sys.exit(app.exec_())
