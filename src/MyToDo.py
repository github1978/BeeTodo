# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MyToDo.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 640)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, 0, 481, 641))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.todohead_hboxlayout = QtWidgets.QHBoxLayout()
        self.todohead_hboxlayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.todohead_hboxlayout.setContentsMargins(5, 5, 5, 5)
        self.todohead_hboxlayout.setObjectName("todohead_hboxlayout")
        self.LockBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.LockBtn.setObjectName("LockBtn")
        self.todohead_hboxlayout.addWidget(self.LockBtn)
        self.TitleLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.TitleLabel.setStyleSheet("color:white;\n"
"font:bold;")
        self.TitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TitleLabel.setObjectName("TitleLabel")
        self.todohead_hboxlayout.addWidget(self.TitleLabel)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.todohead_hboxlayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.todohead_hboxlayout)
        self.todoitem_vboxlayout = QtWidgets.QVBoxLayout()
        self.todoitem_vboxlayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.todoitem_vboxlayout.setContentsMargins(5, 5, 5, 5)
        self.todoitem_vboxlayout.setObjectName("todoitem_vboxlayout")
        self.ToDoListWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.ToDoListWidget.setAutoFillBackground(True)
        self.ToDoListWidget.setStyleSheet("background-color:transparent;\n"
"border:0;")
        self.ToDoListWidget.setAutoScroll(False)
        self.ToDoListWidget.setObjectName("ToDoListWidget")
        self.todoitem_vboxlayout.addWidget(self.ToDoListWidget)
        self.DoneListWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.DoneListWidget.setStyleSheet("background-color:transparent;\n"
"border:0;")
        self.DoneListWidget.setAutoScroll(False)
        self.DoneListWidget.setObjectName("DoneListWidget")
        self.todoitem_vboxlayout.addWidget(self.DoneListWidget)
        self.verticalLayout.addLayout(self.todoitem_vboxlayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.LockBtn.setText(_translate("MainWindow", "PushButton"))
        self.TitleLabel.setText(_translate("MainWindow", "MyToDo"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

