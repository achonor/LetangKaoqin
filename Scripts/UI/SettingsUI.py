# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingsUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.setWindowModality(QtCore.Qt.ApplicationModal)
        Settings.resize(300, 194)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        Settings.setFont(font)
        self.label = QtWidgets.QLabel(Settings)
        self.label.setEnabled(False)
        self.label.setGeometry(QtCore.QRect(20, 20, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.detailPathEdit = QtWidgets.QLineEdit(Settings)
        self.detailPathEdit.setEnabled(False)
        self.detailPathEdit.setGeometry(QtCore.QRect(20, 40, 220, 20))
        self.detailPathEdit.setDragEnabled(False)
        self.detailPathEdit.setReadOnly(False)
        self.detailPathEdit.setClearButtonEnabled(False)
        self.detailPathEdit.setObjectName("detailPathEdit")
        self.summaryPathEdit = QtWidgets.QLineEdit(Settings)
        self.summaryPathEdit.setEnabled(False)
        self.summaryPathEdit.setGeometry(QtCore.QRect(20, 90, 220, 20))
        self.summaryPathEdit.setReadOnly(False)
        self.summaryPathEdit.setObjectName("summaryPathEdit")
        self.label_2 = QtWidgets.QLabel(Settings)
        self.label_2.setEnabled(False)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.summaryPathButton = QtWidgets.QPushButton(Settings)
        self.summaryPathButton.setEnabled(False)
        self.summaryPathButton.setGeometry(QtCore.QRect(250, 90, 40, 20))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.summaryPathButton.setFont(font)
        self.summaryPathButton.setObjectName("summaryPathButton")
        self.label_3 = QtWidgets.QLabel(Settings)
        self.label_3.setGeometry(QtCore.QRect(20, 120, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.outPathEdit = QtWidgets.QLineEdit(Settings)
        self.outPathEdit.setGeometry(QtCore.QRect(20, 140, 220, 20))
        self.outPathEdit.setReadOnly(False)
        self.outPathEdit.setObjectName("outPathEdit")
        self.outPathButton = QtWidgets.QPushButton(Settings)
        self.outPathButton.setGeometry(QtCore.QRect(250, 140, 40, 20))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.outPathButton.setFont(font)
        self.outPathButton.setObjectName("outPathButton")
        self.detailPathButton = QtWidgets.QPushButton(Settings)
        self.detailPathButton.setEnabled(False)
        self.detailPathButton.setGeometry(QtCore.QRect(250, 40, 40, 20))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        self.detailPathButton.setFont(font)
        self.detailPathButton.setObjectName("detailPathButton")

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "设置"))
        self.label.setText(_translate("Settings", "明细表模板路径"))
        self.label_2.setText(_translate("Settings", "汇总表模板路径"))
        self.summaryPathButton.setText(_translate("Settings", "选择"))
        self.label_3.setText(_translate("Settings", "导出文件路径"))
        self.outPathButton.setText(_translate("Settings", "选择"))
        self.detailPathButton.setText(_translate("Settings", "选择"))
