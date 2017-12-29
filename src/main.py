import sys
import MyToDo
from QCustomWidget import *


class MyMainWindow(FrameLessWindow):
    def __init__(self):
        FrameLessWindow.__init__(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.height(), self.width())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    pal = QPalette()
    color = QColor(0, 0, 0)
    color.setAlphaF(0.1)
    pal.setBrush(pal.Background, color)
    ui = MyToDo.Ui_MainWindow()
    ui.setupUi(mainWindow)
    ui.centralwidget.setAutoFillBackground(True)
    ui.centralwidget.setPalette(pal)
    mainWindow.show()
    sys.exit(app.exec_())
