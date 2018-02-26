import MyToDo
import sys
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

    def __init__(self, parent: QListWidget = None, todotext='no set', state=TODO_STATE):
        QListWidgetItem.__init__(self, parent)
        self.parent = parent
        self.widget = QWidget()
        self.hLayout = QHBoxLayout()
        self.toDoTextLabel = QLabel()
        self.toDoTextLabel.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_LABEL'))
        self.toDoTextLabel.setText(todotext)
        self.toDoTextLabel.setGraphicsEffect(StyleSheets.getShadowEffect())
        self.state = state
        if state == self.TODO_STATE:
            self.doneBtn = QPushButton()
            self.doneBtn.setText('√')
            self.doneBtn.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_BTN'))
            self.delBtn = QPushButton()
            self.delBtn.setText('X')
            self.delBtn.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_BTN'))
            self.doneBtn.clicked.connect(self.doneBtnClickedSlot)
            self.delBtn.clicked.connect(self.delBtnClickedSlot)
            self.importanceCheckBox = QCheckBox()
            self.urgencyCheckBox = QCheckBox()
            self.hLayout.addWidget(self.doneBtn, 0)
            self.hLayout.addWidget(self.delBtn, 1)
            self.hLayout.addWidget(self.toDoTextLabel, 2)
            self.hLayout.addWidget(self.importanceCheckBox, 3)
            self.hLayout.addWidget(self.urgencyCheckBox, 4)
            self.importanceCheckBox.clicked.connect(self.importanceCheckedSlot)
            self.urgencyCheckBox.clicked.connect(self.urgencyCheckedSlot)
        else:
            self.resumeBtn = QPushButton()
            self.resumeBtn.setText('R')
            self.resumeBtn.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_BTN'))
            self.resumeBtn.clicked.connect(self.resumeBtnClickedSlot)
            self.hLayout.addWidget(self.resumeBtn, 0)
            self.hLayout.addWidget(self.toDoTextLabel, 1)
        self.widget.setLayout(self.hLayout)
        self.parent.setItemWidget(self, self.widget)

    def setMyToDoUi(self, mytodo):
        self.mytodo = mytodo

    def itemClicked(self):
        print(self.toDoTextLabel.text())

    def text(self):
        return self.toDoTextLabel.text()

    def doneBtnClickedSlot(self):
        doneListWidget = self.mytodo.ui.DoneListWidget
        self.delete()
        self.mytodo.addToDoItem(ToDoItem(doneListWidget, self.text(), self.DONE_STATE))
        print(self.toDoTextLabel.text() + "已完成")

    def delBtnClickedSlot(self):
        self.delete()
        print(self.toDoTextLabel.text() + "已删除")

    def resumeBtnClickedSlot(self):
        toDoListWidget = self.mytodo.ui.ToDoListWidget
        self.delete()
        self.mytodo.addToDoItem(ToDoItem(toDoListWidget, self.text(), self.TODO_STATE))
        print(self.text() + "已恢复")

    def delete(self):
        self.parent.takeItem(self.parent.row(self))

    def importanceCheckedSlot(self, checked):
        if checked:
            print(self.toDoTextLabel.text() + "重要的")
        else:
            print(self.toDoTextLabel.text() + "不重要的")

    def urgencyCheckedSlot(self, checked):
        if checked:
            print(self.toDoTextLabel.text() + "紧急的")
        else:
            print(self.toDoTextLabel.text() + "不紧急的")


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
        self.ui.TitleLabel.setGraphicsEffect(StyleSheets.getShadowEffect())
        self.ui.InfoLabel.setStyleSheet(StyleSheets.getCSS('INFO_LABEL'))
        self.ui.InfoLabel.setText('今天是: ' + utils.getNowDate())

    def init(self):
        toDoListWidget = self.ui.ToDoListWidget
        todoItem1 = ToDoItem(toDoListWidget, '业财对接支付清算余额上线')
        todoItem2 = ToDoItem(toDoListWidget, '上线')
        self.addToDoItem(todoItem1)
        self.addToDoItem(todoItem2)
        toDoListWidget.itemClicked.connect(self.itemClickedSlot)
        self.ui.ExitBtn.clicked.connect(self.exit)
        self.ui.NewItemEdit.returnPressed.connect(self.newItem)

    def newItem(self):
        if not self.ui.NewItemEdit.text().strip():
            return
        todoItem = ToDoItem(self.ui.ToDoListWidget, self.ui.NewItemEdit.text())
        todoItem.setMyToDoUi(self)
        todoItem.setSizeHint(QSize(90, 30))
        todoItem.parent.insertItem(0, todoItem)
        self.ui.NewItemEdit.clear()
        print(todoItem.parent.row(todoItem))

    def exit(self):
        sys.exit()

    def addToDoItem(self, todoItem: ToDoItem):
        todoItem.setMyToDoUi(self)
        todoItem.setSizeHint(QSize(90, 30))
        todoItem.parent.addItem(todoItem)

    def itemClickedSlot(self, item: ToDoItem):
        item.itemClicked()

    def showMainWindow(self):
        self.mainWindow.show()
        return self
