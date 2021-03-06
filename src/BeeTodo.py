import sys
from MyWidgets import MyMainWindow, MyToDoUi
from PyQt5.QtWidgets import QApplication
from StyleSheets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheets.getCSS('GLOBAL'))
    mainWindow = MyMainWindow()
    ui = MyToDoUi(mainWindow).showMainWindow()
    ui.init()
    sys.exit(app.exec_())
