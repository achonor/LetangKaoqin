# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EditWorkTimeUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EditWorkTime(object):
    def setupUi(self, EditWorkTime):
        EditWorkTime.setObjectName("EditWorkTime")
        EditWorkTime.setWindowModality(QtCore.Qt.ApplicationModal)
        EditWorkTime.resize(300, 400)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        EditWorkTime.setFont(font)
        self.calendar = QtWidgets.QCalendarWidget(EditWorkTime)
        self.calendar.setGeometry(QtCore.QRect(0, 0, 300, 240))
        self.calendar.setSelectedDate(QtCore.QDate(2000, 10, 9))
        self.calendar.setGridVisible(True)
        self.calendar.setSelectionMode(QtWidgets.QCalendarWidget.SingleSelection)
        self.calendar.setNavigationBarVisible(False)
        self.calendar.setDateEditEnabled(True)
        self.calendar.setObjectName("calendar")
        self.label = QtWidgets.QLabel(EditWorkTime)
        self.label.setGeometry(QtCore.QRect(112, 248, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.timeEditIn = QtWidgets.QTimeEdit(EditWorkTime)
        self.timeEditIn.setGeometry(QtCore.QRect(62, 326, 80, 20))
        self.timeEditIn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.timeEditIn.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.timeEditIn.setObjectName("timeEditIn")
        self.label_2 = QtWidgets.QLabel(EditWorkTime)
        self.label_2.setGeometry(QtCore.QRect(111, 302, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.timeEditOut = QtWidgets.QTimeEdit(EditWorkTime)
        self.timeEditOut.setGeometry(QtCore.QRect(160, 326, 80, 20))
        self.timeEditOut.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.timeEditOut.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.timeEditOut.setObjectName("timeEditOut")
        self.saveButton = QtWidgets.QPushButton(EditWorkTime)
        self.saveButton.setGeometry(QtCore.QRect(100, 356, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        self.saveButton.setFont(font)
        self.saveButton.setObjectName("saveButton")
        self.lunchBreakEditIn = QtWidgets.QTimeEdit(EditWorkTime)
        self.lunchBreakEditIn.setGeometry(QtCore.QRect(62, 272, 80, 20))
        self.lunchBreakEditIn.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lunchBreakEditIn.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.lunchBreakEditIn.setObjectName("lunchBreakEditIn")
        self.lunchBreakEditOut = QtWidgets.QTimeEdit(EditWorkTime)
        self.lunchBreakEditOut.setGeometry(QtCore.QRect(159, 272, 80, 20))
        self.lunchBreakEditOut.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lunchBreakEditOut.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.lunchBreakEditOut.setObjectName("lunchBreakEditOut")

        self.retranslateUi(EditWorkTime)
        QtCore.QMetaObject.connectSlotsByName(EditWorkTime)

    def retranslateUi(self, EditWorkTime):
        _translate = QtCore.QCoreApplication.translate
        EditWorkTime.setWindowTitle(_translate("EditWorkTime", "编辑作息时间"))
        self.label.setText(_translate("EditWorkTime", "午休时间"))
        self.label_2.setText(_translate("EditWorkTime", "下班时间"))
        self.saveButton.setText(_translate("EditWorkTime", "保存"))
