import configparser

import win32gui
import MyToDo
import sys
import os
import time
from StyleSheets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from service import *


def getTransLucentColor(num):
    color = QColor(0, 0, 0)
    color.setAlphaF(num)
    return color


# noinspection PyAttributeOutsideInit,PyCallByClass
class MyMainWindow(QMainWindow):
    isLocked = False

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.height(), self.width())
        win32gui.SetParent(self.winId(), utils.getWindowsDeskTopHwnd())
        self.ui = QObject()

    def setUi(self, myui):
        self.ui = myui

    def focusInEvent(self, *args, **kwargs):
        pass

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


class MyDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setFixedSize(parent.width() - 100, parent.height() - 300)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.hbox_layout = QVBoxLayout()
        self.export_area = QTextEdit()
        self.export_area.setReadOnly(True)
        self.close_btn = QPushButton()
        self.close_btn.setText("关闭")
        self.close_btn.clicked.connect(self.closeDialogSlot)
        self.hbox_layout.addWidget(self.export_area)
        self.hbox_layout.addWidget(self.close_btn)
        self.setLayout(self.hbox_layout)

    def closeDialogSlot(self):
        self.hide()


class ToDoItem(QListWidgetItem):
    DONE_STATE = 1
    ALTER_STATE = 2
    TODO_STATE = 0

    def __init__(self, parent: QListWidget = None, todotext='no set', state=TODO_STATE):
        QListWidgetItem.__init__(self, parent)
        self.parent = parent
        self.state = state
        self.widget = QWidget()
        # self.widget.setStyle()
        self.hLayout = QHBoxLayout()
        self.toDoTextLabel = QLabel()
        self.toDoTextLabel.setStyleSheet(StyleSheets.getCSS('TODO_LIST_WIDGET_ITEM_LABEL'))
        self.toDoTextLabel.setText(todotext)
        self.widget.setGraphicsEffect(StyleSheets.getShadowEffect())
        if self.state == self.TODO_STATE:
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
        self.id = int(round(time.time() * 1000))
        self.todo = todotext
        self.imp = 0
        self.emg = 0
        self.state = state
        self.create_date = utils.getNowDate("%Y-%m-%d %H:%M:%S")
        self.sort = 0
        self.end_date = ""

    def setMyToDoUi(self, mytodo):
        self.mytodo = mytodo

    def setUrgency(self, boolvalue):
        self.emg = int(boolvalue)
        self.urgencyCheckBox.setChecked(False if self.emg == 0 else True)

    def setImportant(self, boolvalue):
        self.imp = int(boolvalue)
        self.importanceCheckBox.setChecked(False if self.imp == 0 else True)

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
        self.parent.takeItem(self.parent.row(self))
        self.state = self.DONE_STATE
        self.end_date = utils.getNowDate("%Y-%m-%d %H:%M:%S")
        self.mytodo.addToDoItem(
            ToDoItem(doneListWidget, self.text(), self.DONE_STATE).unserialize(self.serialize()))
        updateItems([self.serialize()])
        print(self.toDoTextLabel.text() + "已完成")

    def delBtnClickedSlot(self):
        self.delete()
        print(self.toDoTextLabel.text() + "已删除")

    def resumeBtnClickedSlot(self):
        toDoListWidget = self.mytodo.ui.ToDoListWidget
        self.parent.takeItem(self.parent.row(self))
        self.state = self.TODO_STATE
        self.mytodo.addToDoItem(
            ToDoItem(toDoListWidget, self.text()).unserialize(self.serialize()))
        updateItems([self.serialize()])
        print(self.text() + "已恢复")

    def delete(self):
        self.parent.takeItem(self.parent.row(self))
        delItems([self.serialize()])

    def importanceCheckedSlot(self, checked):
        self.setImportant(int(checked))
        updateItems([self.serialize()])
        self.mytodo.selected_item = self
        self.mytodo.reload()

    def urgencyCheckedSlot(self, checked):
        self.setUrgency(int(checked))
        updateItems([self.serialize()])
        self.mytodo.selected_item = self
        self.mytodo.reload()

    def setToDo(self, todo_text):
        self.todo = todo_text
        self.toDoTextLabel.setText(todo_text)

    def serialize(self):
        return {'id': self.id, 'todo': self.todo, 'imp': self.imp,
                'emg': self.emg, 'state': self.state, 'create_date': self.create_date,
                'sort': self.sort, 'end_date': self.end_date}

    def unserialize(self, item_data):
        self.id = item_data['id']
        self.state = item_data['state']
        self.create_date = item_data['create_date']
        self.sort = item_data['sort']
        if self.state == self.TODO_STATE:
            self.setUrgency(item_data['emg'])
            self.setImportant(item_data['imp'])
        self.setToDo(item_data['todo'])
        self.end_date = item_data['end_date']
        return self


class MyToDoUi(QObject):
    selected_item: ToDoItem = None
    cf = configparser.ConfigParser()
    normal_section = "normal"
    config_file_name = "BeeTodo.config"

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
        self.export_dialog = MyDialog(self.mainWindow)
        self.calendar_dialog_layout = QHBoxLayout()
        self.calendar_dialog = QDialog(self.mainWindow)
        self.calendar = QCalendarWidget()

    def init(self):
        self.reload()
        self.ui.HistoryItemDateEdit.dateChanged.connect(self.historyDateChangedSlot)
        self.ui.HistoryItemDateEdit.setDate(QDate.currentDate())
        self.ui.HistorySelectBtn.clicked.connect(self.historySelectBtnClickedSlot)
        self.ui.ToDoListWidget.itemDoubleClicked.connect(self.itemDoubleClickedSlot)
        self.ui.ExitBtn.clicked.connect(self.exit)
        self.ui.LockBtn.clicked.connect(self.lockPoint)
        self.ui.ExportToDay.clicked.connect(self.exportTodayDoneTodos)
        self.updateDate()
        self.timer.timeout.connect(self.updateDate)
        self.timer.start(5000)
        self.loadConfig()

    def exportTodayDoneTodos(self):
        item_count = self.ui.DoneListWidget.count()
        export_result = ""
        for row_index in range(item_count):
            export_result = export_result + str(row_index + 1) + ". " \
                            + self.ui.DoneListWidget.item(row_index).text() + "。\n"
        self.export_dialog.export_area.setText(export_result)
        self.export_dialog.exec()

    def reload(self):
        self.ui.ToDoListWidget.clear()
        self.ui.DoneListWidget.clear()
        where_sql = "and state=" + str(ToDoItem.TODO_STATE)
        for item in queryItems(where_sql):
            todo_item = ToDoItem(self.ui.ToDoListWidget)
            self.addToDoItem(todo_item.unserialize(item))

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
        todoItem.setImportant(self.ui.newitem_i_checkbox.isChecked())
        todoItem.setUrgency(self.ui.newitem_e_checkBox.isChecked())
        self.ui.NewItemEdit.clear()
        self.ui.newitem_i_checkbox.setChecked(False)
        self.ui.newitem_e_checkBox.setChecked(False)
        item_list = [tuple(todoItem.serialize().values())]
        print(item_list)
        saveItems(item_list)
        self.reload()

    def sortItem(self):
        pass

    def exit(self):
        closeDbConn()
        self.applyConfig()
        sys.exit()

    def addToDoItem(self, todoItem: ToDoItem):
        todoItem.setMyToDoUi(self)
        todoItem.setSizeHint(QSize(90, 30))
        todoItem.parent.insertItem(0, todoItem)
        if self.selected_item is not None and todoItem.id == self.selected_item.id:
            todoItem.setSelected(True)

    @staticmethod
    def itemClickedSlot(item: ToDoItem):
        item.itemClicked()

    @staticmethod
    def itemDoubleClickedSlot(item: ToDoItem):
        item.itemDoubleClicked()

    def historyDateChangedSlot(self):
        self.ui.DoneListWidget.clear()
        where_sql = "and state=" + str(ToDoItem.DONE_STATE) \
                    + " and date(end_date)='" + self.ui.HistoryItemDateEdit.text() + "'"
        for item in queryItems(where_sql):
            todo_item = ToDoItem(self.ui.DoneListWidget, item["todo"], ToDoItem.DONE_STATE)
            self.addToDoItem(todo_item.unserialize(item))

    def historySelectBtnClickedSlot(self):
        self.calendar.clicked.connect(self.historyItemCalendarClickedSlot)
        self.calendar_dialog_layout.addWidget(self.calendar)
        self.calendar_dialog.setLayout(self.calendar_dialog_layout)
        self.calendar_dialog.show()

    def historyItemCalendarClickedSlot(self):
        self.ui.HistoryItemDateEdit.setDate(self.calendar.selectedDate())
        self.calendar_dialog.hide()

    def showMainWindow(self):
        self.mainWindow.show()
        return self

    def updateDate(self):
        self.ui.InfoLabel.setText('今天是: ' + QDateTime.currentDateTime().toString("yyyy-MM-dd dddd"))

    def loadConfig(self):
        if not os.path.exists(self.config_file_name):
            self.cf.add_section(self.normal_section)
            self.cf.set(self.normal_section, "current_location", "")
            self.cf.set(self.normal_section, "lock", "False")
            with open(self.config_file_name, "w") as configFile:
                self.cf.write(configFile)
        self.cf.read(self.config_file_name)
        try:
            current_location = self.cf.get(self.normal_section, "current_location").split(",")
            if current_location[0] != "":
                self.mainWindow.move(int(current_location[0]), int(current_location[1]))
            lock = self.cf.get(self.normal_section, "lock")
            if lock is not None:
                self.mainWindow.isLocked = True if lock == "False" else False
                self.lockPoint()
        except Exception as e:
            print(e)
            pass

    def applyConfig(self):
        window_pos = self.mainWindow.pos()
        try:
            self.cf.set(self.normal_section, "current_location",
                        str(window_pos.x()) + "," + str(window_pos.y()))
            self.cf.set(self.normal_section, "lock",
                        str(self.mainWindow.isLocked))
            with open(self.config_file_name, "w") as configfile:
                self.cf.write(configfile)
        except Exception as e:
            print(e)
            pass
