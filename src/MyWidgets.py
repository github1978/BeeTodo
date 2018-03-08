import MyToDo
import sys
from StyleSheets import *
from PyQt5.Qt import *


def getTransLucentColor(num):
    color = QColor(0, 0, 0)
    color.setAlphaF(num)
    return color


class MyMainWindow(QMainWindow):
    isLocked = False

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.height(), self.width())
        self.ui = QObject()

    def setUi(self, myui):
        self.ui = myui

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            QApplication.postEvent(self, QEvent(174))
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def keyPressEvent(self, *args, **kwargs):
        self.ui.newItem()

    def eventFilter(self, obj, evt: QEvent):
        if obj == self:
            if evt.type() == QEvent.MouseMove:
                return True
        return QMainWindow.eventFilter(self, obj, evt)


class ToDoItem(QListWidgetItem):
    DONE_STATE = 1
    ALTER_STATE = 2
    TODO_STATE = 0

    def __init__(self, parent: QListWidget = None, todotext='no set', state=TODO_STATE):
        QListWidgetItem.__init__(self, parent)
        self.parent = parent
        self.widget = QWidget()
        # self.widget.setStyle()
        self.hLayout = QHBoxLayout()
        self.toDoTextLabel = QLabel()
        self.toDoTextLabel.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_LABEL'))
        self.toDoTextLabel.setText(todotext)
        self.widget.setGraphicsEffect(StyleSheets.getShadowEffect())
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
            self.urgencyCheckBox = QCheckBox()
            self.importanceCheckBox = QCheckBox()
            self.hLayout.addWidget(self.doneBtn, 0)
            self.hLayout.addWidget(self.delBtn, 1)
            self.hLayout.addWidget(self.toDoTextLabel, 2)
            self.hLayout.addWidget(self.importanceCheckBox, 3)
            self.hLayout.addWidget(self.urgencyCheckBox, 4)
            self.urgencyCheckBox.setText("紧")
            self.importanceCheckBox.setText("要")
            self.urgencyCheckBox.clicked.connect(self.urgencyCheckedSlot)
            self.importanceCheckBox.clicked.connect(self.importanceCheckedSlot)
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

    def setUrgency(self, boolvalue):
        self.urgencyCheckBox.setChecked(boolvalue)

    def setImportant(self, boolvalue):
        self.importanceCheckBox.setChecked(boolvalue)

    def itemClicked(self):
        print(self.toDoTextLabel.text())

    def itemDoubleClicked(self):
        if self.state != self.ALTER_STATE:
            self.hLayout.removeWidget(self.toDoTextLabel)
            self.toDoTextLabel.deleteLater()
            input = QLineEdit()
            input.setFixedSize(290, 10)
            self.hLayout.insertWidget(2, input)
            self.doneBtn.setEnabled(False)
            self.delBtn.setEnabled(False)
            self.importanceCheckBox.setEnabled(False)
            self.urgencyCheckBox.setEnabled(False)
            self.state = self.ALTER_STATE

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
    def __init__(self, window: MyMainWindow):
        QObject.__init__(self)
        self.ui = MyToDo.Ui_MainWindow()
        self.mainWindow = window
        self.mainWindow.setUi(self)
        pal = QPalette()
        pal.setBrush(pal.Background, getTransLucentColor(0.1))
        self.ui.setupUi(self.mainWindow)
        self.ui.centralwidget.setAutoFillBackground(True)
        self.ui.centralwidget.setPalette(pal)
        self.ui.ToDoListWidget.maximumHeight = 290
        self.ui.ToDoListWidget.verticalScrollBar().setStyleSheet(StyleSheets.getCSS("TODO_LIST_WIDGET_SCROLLBAR"))
        self.ui.DoneListWidget.maximumHeight = 290
        self.ui.DoneListWidget.verticalScrollBar().setStyleSheet(StyleSheets.getCSS("TODO_LIST_WIDGET_SCROLLBAR"))
        self.ui.TitleLabel.setGraphicsEffect(StyleSheets.getShadowEffect())
        self.ui.InfoLabel.setStyleSheet(StyleSheets.getCSS('INFO_LABEL'))
        self.timer = QTimer(self)
        self.ui.LockBtn.setText("已解锁")

    def init(self):
        toDoListWidget = self.ui.ToDoListWidget
        todoItem1 = ToDoItem(toDoListWidget, '业财对接支付清算余额上线')
        todoItem2 = ToDoItem(toDoListWidget, '上线')
        self.addToDoItem(todoItem1)
        self.addToDoItem(todoItem2)
        toDoListWidget.itemDoubleClicked.connect(self.itemDoubleClickedSlot)
        self.ui.ExitBtn.clicked.connect(self.exit)
        self.ui.LockBtn.clicked.connect(self.lockPoint)
        self.updateDate()
        self.timer.timeout.connect(self.updateDate)
        self.timer.start(5000)

    def lockPoint(self):
        print(self.mainWindow.isLocked)
        if self.mainWindow.isLocked:
            self.mainWindow.removeEventFilter(self.mainWindow)
            self.mainWindow.isLocked = False
            self.ui.LockBtn.setText("已解锁")
        else:
            self.ui.LockBtn.setText("已锁定")
            self.mainWindow.isLocked = True
            self.mainWindow.installEventFilter(self.mainWindow)

    def newItem(self):
        if not self.ui.NewItemEdit.text().strip():
            return
        todoItem = ToDoItem(self.ui.ToDoListWidget, self.ui.NewItemEdit.text())
        todoItem.setMyToDoUi(self)
        todoItem.setSizeHint(QSize(90, 30))
        todoItem.setImportant(self.ui.newitem_i_checkbox.isChecked())
        todoItem.setUrgency(self.ui.newitem_e_checkBox.isChecked())
        todoItem.parent.insertItem(0, todoItem)
        self.ui.NewItemEdit.clear()
        self.ui.newitem_i_checkbox.setChecked(False)
        self.ui.newitem_e_checkBox.setChecked(False)
        print(todoItem.parent.row(todoItem))

    def sortItem(self):
        pass

    def exit(self):
        sys.exit()

    def addToDoItem(self, todoItem: ToDoItem):
        todoItem.setMyToDoUi(self)
        todoItem.setSizeHint(QSize(90, 30))
        todoItem.parent.addItem(todoItem)

    def itemClickedSlot(self, item: ToDoItem):
        item.itemClicked()

    def itemDoubleClickedSlot(self, item: ToDoItem):
        item.itemDoubleClicked()

    def showMainWindow(self):
        self.mainWindow.show()
        return self

    def updateDate(self):
        self.ui.InfoLabel.setText('今天是: ' + QDateTime.currentDateTime().toString("yyyy-MM-dd dddd"))
