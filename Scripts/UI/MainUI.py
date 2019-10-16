# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.memberList = QtWidgets.QListView(self.centralwidget)
        self.memberList.setGeometry(QtCore.QRect(10, 0, 171, 531))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.memberList.setFont(font)
        self.memberList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.memberList.setObjectName("memberList")
        self.calendar = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendar.setGeometry(QtCore.QRect(190, 0, 401, 431))
        self.calendar.setMinimumDate(QtCore.QDate(2019, 9, 1))
        self.calendar.setMaximumDate(QtCore.QDate(2019, 9, 30))
        self.calendar.setGridVisible(True)
        self.calendar.setObjectName("calendar")
        self.detailedInfo = QtWidgets.QTextBrowser(self.centralwidget)
        self.detailedInfo.setGeometry(QtCore.QRect(190, 430, 401, 121))
        self.detailedInfo.setObjectName("detailedInfo")
        self.leaveMember = QtWidgets.QComboBox(self.centralwidget)
        self.leaveMember.setGeometry(QtCore.QRect(600, 30, 101, 22))
        self.leaveMember.setObjectName("leaveMember")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(620, 0, 150, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.leaveEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.leaveEdit.setGeometry(QtCore.QRect(600, 50, 191, 281))
        self.leaveEdit.setObjectName("leaveEdit")
        self.saveLeaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveLeaveButton.setGeometry(QtCore.QRect(640, 340, 121, 31))
        self.saveLeaveButton.setObjectName("saveLeaveButton")
        self.saveResultLabel = QtWidgets.QLabel(self.centralwidget)
        self.saveResultLabel.setEnabled(True)
        self.saveResultLabel.setGeometry(QtCore.QRect(710, 26, 81, 20))
        self.saveResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.saveResultLabel.setObjectName("saveResultLabel")
        self.inDateEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.inDateEdit.setGeometry(QtCore.QRect(600, 430, 194, 22))
        self.inDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.inDateEdit.setObjectName("inDateEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(600, 399, 100, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(600, 450, 100, 25))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.outDateEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.outDateEdit.setGeometry(QtCore.QRect(600, 480, 194, 22))
        self.outDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.outDateEdit.setObjectName("outDateEdit")
        self.saveInOutButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveInOutButton.setGeometry(QtCore.QRect(630, 510, 121, 31))
        self.saveInOutButton.setObjectName("saveInOutButton")
        self.showOutMember = QtWidgets.QCheckBox(self.centralwidget)
        self.showOutMember.setGeometry(QtCore.QRect(20, 530, 131, 21))
        self.showOutMember.setObjectName("showOutMember")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport_File = QtWidgets.QAction(MainWindow)
        self.actionImport_File.setObjectName("actionImport_File")
        self.actionExport_File = QtWidgets.QAction(MainWindow)
        self.actionExport_File.setObjectName("actionExport_File")
        self.actionEdit_WorkTime = QtWidgets.QAction(MainWindow)
        self.actionEdit_WorkTime.setObjectName("actionEdit_WorkTime")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuFile.addAction(self.actionImport_File)
        self.menuFile.addAction(self.actionExport_File)
        self.menuFile.addAction(self.actionEdit_WorkTime)
        self.menuFile.addAction(self.actionSettings)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "考勤统计"))
        self.label.setText(_translate("MainWindow", "请假时间"))
        self.saveLeaveButton.setText(_translate("MainWindow", "保存"))
        self.saveResultLabel.setText(_translate("MainWindow", "成功"))
        self.label_2.setText(_translate("MainWindow", "入职时间"))
        self.label_3.setText(_translate("MainWindow", "离职时间"))
        self.saveInOutButton.setText(_translate("MainWindow", "保存"))
        self.showOutMember.setText(_translate("MainWindow", "显示未入职/离职人员"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionImport_File.setText(_translate("MainWindow", "Import File"))
        self.actionExport_File.setText(_translate("MainWindow", "Export File"))
        self.actionEdit_WorkTime.setText(_translate("MainWindow", "Edit WorkTime"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
