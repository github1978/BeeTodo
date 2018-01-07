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


class ToDoItem(QListWidgetItem):
    DONE_STATE = 1
    TODO_STATE = 0

    def __init__(self, parent: QListWidget=None, todotext='no set'):
        QListWidgetItem.__init__(self, parent)
        self.parent = parent
        self.widget = QWidget()
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
        self.widget.setLayout(self.hLayout)
        self.doneBtn.clicked.connect(self.doneBtnClickedSlot)
        self.delBtn.clicked.connect(self.delBtnClickedSlot)
        self.importanceCheckBox.clicked.connect(self.importanceCheckedSlot)
        self.urgencyCheckBox.clicked.connect(self.urgencyCheckedSlot)
        self.parent.setItemWidget(self, self.widget)

    def itemClicked(self):
        print(self.toDoTextLabel.text())

    def doneBtnClickedSlot(self):
        print(self.toDoTextLabel.text()+"已完成")

    def delBtnClickedSlot(self):
        print(self.toDoTextLabel.text()+"已删除")

    def importanceCheckedSlot(self, checked):
        if checked:
            print(self.toDoTextLabel.text()+"重要的")
        else:
            print(self.toDoTextLabel.text()+"不重要的")

    def urgencyCheckedSlot(self, checked):
        if checked:
            print(self.toDoTextLabel.text()+"紧急的")
        else:
            print(self.toDoTextLabel.text()+"不紧急的")


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
        self.ui.ToDoListWidget.maximumHeight = 290
        self.ui.ToDoListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.DoneListWidget.maximumHeight = 290
        self.ui.DoneListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def init(self):
        self.addToDoItem('业财对接支付清算余额上线')
        self.addToDoItem('业财平台版本模块变更')
        self.addToDoItem('业财平台版本模块变更')
        self.addToDoItem('业财平台版本模块变更')
        self.addToDoItem('业财平台版本模块变更')
        self.addToDoItem('业财平台版本模块变更')
        self.addToDoItem('业财平台版本模块变更')
        self.addToDoItem('业财平台版本模块变更')
        self.addToDoItem('业财平台版本模块变更')
        self.ui.ToDoListWidget.itemClicked.connect(self.itemClickedSlot)

    def addToDoItem(self, todotext):
        todoItem = ToDoItem(self.ui.ToDoListWidget, todotext)
        todoItem.setSizeHint(QSize(90,40))
        self.ui.ToDoListWidget.addItem(todoItem)

    def itemClickedSlot(self, item: ToDoItem):
        item.itemClicked()

    def showMainWindow(self):
        self.mainWindow.show()
        return self
