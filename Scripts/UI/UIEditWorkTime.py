from PyQt5 import QtGui
from PyQt5.QtCore import QStringListModel, QDate, Qt, QTime
from PyQt5.QtWidgets import QWidget, QDialog
from Scripts.UI.UIBase import UIBase
from Scripts.UI import EditWorkTimeUI
from Scripts.Data.CommonDatas import CommonDatas
from Scripts.Data.Configs import Configs
from datetime import datetime

class UIEditWorkTime(EditWorkTimeUI.Ui_EditWorkTime, UIBase):
    def __init__(self):
        super().__init__()
        self.widget = QDialog()
        self.setupUi(self.widget)
        self.work_time_table = None
        #注册回调
        self.saveButton.clicked.connect(self.save_config)
        self.timeEditIn.timeChanged.connect(self.on_time_change)
        self.timeEditOut.timeChanged.connect(self.on_time_change)
        self.lunchBreakEditIn.timeChanged.connect(self.on_time_change)
        self.lunchBreakEditOut.timeChanged.connect(self.on_time_change)
        self.calendar.activated.connect(self.double_click)


    def open(self):
        super().open()
        self.widget.show()
        self.calendar.setMinimumDate(CommonDatas.get_instance().start_date)
        self.calendar.setMaximumDate(CommonDatas.get_instance().end_date)
        work_time = Configs.get_instance().get_config("work_time")
        self.timeEditOut.setTime(QTime(work_time[1][0], work_time[1][1]))
        self.timeEditIn.setTime(QTime(work_time[0][0], work_time[0][1]))
        lunch_break = Configs.get_instance().get_config("lunch_break")
        self.lunchBreakEditOut.setTime(QTime(lunch_break[1][0], lunch_break[1][1]))
        self.lunchBreakEditIn.setTime(QTime(lunch_break[0][0], lunch_break[0][1]))
        self.work_time_table = Configs.get_instance().get_temp_config("work_time_table").copy()
        self.on_time_change()
        self.refresh_UI()

    def refresh_UI(self):
        cur_date = CommonDatas.get_instance().start_date
        for index, value in enumerate(self.work_time_table):
            brush = QtGui.QBrush()
            if value is True:
                brush.setColor(QtGui.QColor("Black"))
            else:
                brush.setColor(QtGui.QColor("Red"))
            cmd_fmt = QtGui.QTextCharFormat()
            cmd_fmt.setForeground(brush)
            self.calendar.setDateTextFormat(QDate(cur_date.year, cur_date.month, index + 1), cmd_fmt)

    def save_config(self):
        in_time = self.timeEditIn.time()
        out_time = self.timeEditOut.time()
        work_time = []
        work_time.append([in_time.hour(), in_time.minute()])
        work_time.append([out_time.hour(), out_time.minute()])
        Configs.get_instance().set_config("work_time", work_time)
        lunch_break_in_time = self.lunchBreakEditIn.time()
        lunch_break_out_time = self.lunchBreakEditOut.time()
        lunch_break = []
        lunch_break.append([lunch_break_in_time.hour(), lunch_break_in_time.minute()])
        lunch_break.append([lunch_break_out_time.hour(), lunch_break_out_time.minute()])
        Configs.get_instance().set_config("lunch_break", lunch_break)
        Configs.get_instance().save_json()

        Configs.get_instance().set_temp_config("work_time_table", self.work_time_table)
        Configs.get_instance().save_temp_json()
        from Scripts.UI.UIMain import UIMain
        UIMain.get_instance().refresh_UI()

    def on_time_change(self):
        self.timeEditOut.setMinimumTime(self.timeEditIn.time())
        self.timeEditIn.setMaximumTime(self.timeEditOut.time())
        self.lunchBreakEditOut.setMinimumTime(self.lunchBreakEditIn.time())
        self.lunchBreakEditIn.setMaximumTime(self.lunchBreakEditOut.time())

    def double_click(self):
        #双击取反
        index = self.calendar.selectedDate().day() - 1
        self.work_time_table[index] = not self.work_time_table[index]
        self.refresh_UI()
