import sys
from MyWidgets import MyMainWindow, MyToDoUi, QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    ui = MyToDoUi(mainWindow).showMainWindow()
    ui.init()
    sys.exit(app.exec_())
