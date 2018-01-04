import MyToDo
from StyleSheets import *
from PyQt5.Qt import *


def getTransLucentColor(num):
    color = QColor(0, 0, 0)
    color.setAlphaF(num)
    return color


class MyMainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.height(), self.width())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()


class ToDoItem(QWidget):
    DONE_STATE = 1
    TODO_STATE = 0

    def __init__(self, parent: QListWidget=None, todotext='no set'):
        QWidget.__init__(self, parent)
        self.hLayout = QHBoxLayout()
        self.toDoTextLabel = QLabel()
        self.toDoTextLabel.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_LABEL'))
        self.toDoTextLabel.setText(todotext)
        self.toDoTextLabel.setGraphicsEffect(StyleSheets.getShadowEffect())
        self.importanceCheckBox = QCheckBox()
        self.urgencyCheckBox = QCheckBox()
        self.doneBtn = QPushButton()
        self.doneBtn.setText('√')
        self.doneBtn.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_BTN'))
        self.delBtn = QPushButton()
        self.delBtn.setText('X')
        self.delBtn.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_BTN'))
        self.state = self.TODO_STATE
        self.hLayout.addWidget(self.doneBtn, 0)
        self.hLayout.addWidget(self.delBtn, 1)
        self.hLayout.addWidget(self.toDoTextLabel, 2)
        self.hLayout.addWidget(self.importanceCheckBox, 3)
        self.hLayout.addWidget(self.urgencyCheckBox, 4)
        self.setLayout(self.hLayout)
        parent.itemClicked.connect(self.itemClickedSlot)

    def itemClickedSlot(self):
        print(self.toDoTextLabel.text())


class MyToDoUi(QObject):
    def __init__(self, window):
        QObject.__init__(self)
        self.ui = MyToDo.Ui_MainWindow()
        self.mainWindow = window
        pal = QPalette()
        pal.setBrush(pal.Background, getTransLucentColor(0.1))
        self.ui.setupUi(self.mainWindow)
        self.ui.centralwidget.setAutoFillBackground(True)
        self.ui.centralwidget.setPalette(pal)

    def init(self):
        self.addToDoItem('ice')

    def addToDoItem(self, todotext):
        todoItem = ToDoItem(self.ui.ToDoListWidget, todotext)
        qListWidgetItem = QListWidgetItem()
        qListWidgetItem.setSizeHint(QSize(90, 40))
        self.ui.ToDoListWidget.addItem(qListWidgetItem)
        self.ui.ToDoListWidget.setItemWidget(qListWidgetItem, todoItem)

    def showMainWindow(self):
        self.mainWindow.show()
        return self
