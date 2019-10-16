import os
from PyQt5 import QtGui
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QStringListModel, QDate, Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QMenu

from Scripts.UI.UIBase import UIBase
from Scripts.UI import MainUI
from Scripts.Data.CommonDatas import CommonDatas
from Scripts.Data.Member import Member
from Scripts.UI.UIEditWorkTime import UIEditWorkTime
from Scripts.UI.UIMemberData import UIMemberData
from Scripts.UI.UISettings import UISettings
from Scripts.Data.Configs import Configs
from Scripts.Logic import Functions, ExportXLSX
import chardet

class UIMain(MainUI.Ui_MainWindow, UIBase):
    def __init__(self):
        super().__init__()
        self.widget = QMainWindow()
        self.setupUi(self.widget)
        
        self.file_path = None
        self.select_member = None
        self.edit_leave_member = None
        self.edit_worktime_UI = UIEditWorkTime()
        self.member_data_UI = UIMemberData()
        self.settings_UI = UISettings()
        #列表右键菜单
        self.memberList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.memberList.customContextMenuRequested.connect(self.show_member_list_menu)
        self.member_list_contextMenu = QMenu(self.calendar)
        eidt_member_data = self.member_list_contextMenu.addAction("编辑成员信息")
        eidt_member_data.triggered.connect(self.open_edit_member_data)
        #日历右键菜单
        self.calendar.setContextMenuPolicy(Qt.CustomContextMenu)
        self.calendar.customContextMenuRequested.connect(self.show_calendar_menu)
        self.calendar_contextMenu = QMenu(self.calendar)
        menu_add_in_checkin = self.calendar_contextMenu.addAction('添加上班打卡')
        menu_add_out_checkin = self.calendar_contextMenu.addAction('添加下班打卡')
        menu_remove_added_checkins = self.calendar_contextMenu.addAction('删除添加的打卡')
        menu_add_in_checkin.triggered.connect(self.add_in_checkin)
        menu_add_out_checkin.triggered.connect(self.add_out_checkin)
        menu_remove_added_checkins.triggered.connect(self.remove_added_checkins)
        #注册回调
        self.actionImport_File.triggered.connect(self.import_file)
        self.actionExport_File.triggered.connect(self.export_file)
        self.actionEdit_WorkTime.triggered.connect(self.edit_worktime)
        self.actionSettings.triggered.connect(self.open_settings)
        self.memberList.clicked.connect(self.click_member)
        self.calendar.clicked.connect(self.click_date)
        self.leaveMember.currentIndexChanged.connect(self.click_leave)
        self.saveLeaveButton.clicked.connect(self.save_leave)
        self.saveInOutButton.clicked.connect(self.save_in_out)
        self.showOutMember.stateChanged.connect(self.refresh_UI)

    def open(self):
        super().open()
        self.widget.show()
        self.saveResultLabel.setText("")
        self.actionExport_File.setEnabled(False)
        self.actionEdit_WorkTime.setEnabled(False)
        #self.import_file(r"C:\Users\achonor\Desktop\KaoqinXML\08月考勤报表汇总.xml")

    def refresh_UI(self):
        #成员列表
        list_model = QStringListModel()
        listString = []
        show_out_member = self.showOutMember.isChecked()
        for key in CommonDatas.get_instance().get_all_member_dict(show_out_member):
            listString.append(key)
        list_model.setStringList(listString)
        self.memberList.setModel(list_model)
        self.calendar.setMinimumDate(CommonDatas.get_instance().start_date)
        self.calendar.setMaximumDate(CommonDatas.get_instance().end_date)
        self.leaveMember.addItems(listString)
        self.saveResultLabel.setText("")
        self.refresh_select_member()

    def show_calendar_menu(self):
        self.calendar_contextMenu.exec_(QCursor.pos())

    def show_member_list_menu(self):
        if self.select_member is None:
            return
        self.member_list_contextMenu.exec_(QCursor.pos())

    def add_in_checkin(self):
        date = self.calendar.selectedDate()
        work_time = Configs.get_instance().get_config("work_time")
        self.select_member.add_checkin(int(date.day()), [work_time[0][0], work_time[0][1]])
        self.refresh_select_member()

    def add_out_checkin(self):
        date = self.calendar.selectedDate()
        work_time = Configs.get_instance().get_config("work_time")
        self.select_member.add_checkin(int(date.day()), [work_time[1][0], work_time[1][1]])
        self.refresh_select_member()

    def remove_added_checkins(self):
        date = self.calendar.selectedDate()
        self.select_member.remove_all_checkins(int(date.day()))
        self.refresh_select_member()

    def import_file(self, default_path= None):
        if type(default_path) is str:
            self.file_path = default_path
        else:
            self.file_path = self.open_file_dialog(default_path=r"C:\Users\achonor\Desktop\KaoqinXML")
        if self.file_path is None:
            return
        print(self.file_path)
        #修改编码
        self.convert(self.file_path)
        #删除回车
        self.delete_nr(self.file_path)
        xml_data = Functions.load_XML(self.file_path)
        CommonDatas.get_instance().reset_data(xml_data)

        #数据加载完成
        self.actionExport_File.setEnabled(True)
        self.actionEdit_WorkTime.setEnabled(True)
        self.refresh_UI()

    def export_file(self):
        error_tips = None
        miss_member = False
        settings_configs = Configs.get_instance().get_config("settings")
        if False and not os.path.isfile(settings_configs["detail_table_path"]):
            error_tips = "请选择明细表模板"
        elif False and not os.path.isfile(settings_configs["summary_table_path"]):
            error_tips = "请选择汇总表模板"
        elif not os.path.isdir(settings_configs["out_path"]):
            error_tips = "请选择输出文件路径"
        else:
            show_out_member = self.showOutMember.isChecked()
            for name, member in CommonDatas.get_instance().get_all_member_dict(show_out_member).items():
                if len(member.email) <= 0:
                    error_tips = name + "的邮箱没填写"
                elif len(member.bank_card) <= 0:
                    error_tips = name + "的银行卡号没填写"
                if error_tips is not None:
                    miss_member = member
                    break
        if error_tips is not None:
            reply = QMessageBox.warning(self.widget, 'Message', error_tips, QMessageBox.Yes, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                if miss_member is not False:
                    self.open_edit_member_data(member=miss_member)
                else:
                    self.open_settings()
            return
        try:
            #导出明细表
            ExportXLSX.export_detail_table(settings_configs["detail_table_path"], settings_configs["out_path"])
            #导出汇总表
            ExportXLSX.export_summary_table(settings_configs["summary_table_path"], settings_configs["out_path"])
        except PermissionError as exc:
            QMessageBox.warning(self.widget, "Error", "文件导出错误" + str(exc), QMessageBox.Yes)
        else:
            os.system("start explorer " + settings_configs["out_path"].replace("/", "\\"))

    def edit_worktime(self):
        self.edit_worktime_UI.open()

    def open_settings(self):
        print("open_settings")
        self.settings_UI.open()

    def open_edit_member_data(self, **kwargs):
        member = self.select_member
        if "member" in kwargs:
            member = kwargs["member"]
        if member is None:
            return
        self.member_data_UI.open(member)

    def refresh_select_member(self, new_member=None):
        if new_member is not None:
            self.select_member = new_member
        if self.select_member is None:
            return
        self.select_member.calc_all_data()
        cur_year = CommonDatas.get_instance().start_date.year
        cur_month = CommonDatas.get_instance().start_date.month
        for index in range(1, CommonDatas.get_instance().days_number + 1):
            brush = QtGui.QBrush()
            if not self.select_member.in_company(index):
                #没入职或者离职了
                brush.setColor(QtGui.QColor('Black'))
            elif not Configs.get_instance().get_is_work_time(index):
                #休息日
                brush.setColor(QtGui.QColor('Black'))
            elif 0 < self.select_member.is_late_or_early(index):
                #迟到
                brush.setColor(QtGui.QColor('Red'))
            else:
                brush.setColor(QtGui.QColor('Green'))
            cmd_fmt = QtGui.QTextCharFormat()
            cmd_fmt.setForeground(brush)
            self.calendar.setDateTextFormat(QDate(cur_year, cur_month, index), cmd_fmt)
        self.leaveMember.setCurrentText(self.select_member.name)
        self.inDateEdit.setDateTime(self.select_member.in_date)
        self.outDateEdit.setDateTime(self.select_member.out_date)
        #显示
        member = self.select_member
        self.detailedInfo.setText(member.name)
        self.detailedInfo.append("缺卡次数：{0}".format(member.lack_checkin_count))
        self.detailedInfo.append("迟到早退天数：{0} 罚款总数：{1}".format(member.late_or_early_count, member.late_or_early_fine_number))
        self.detailedInfo.append("工作天数：{0} 休息天数：{1}".format(member.work_days, member.holidays))
        self.detailedInfo.append("请假次数：{0} 请假时长：{1}".format(member.get_leave_count(), Functions.timedelta2string(member.get_leave_duration())))

    def click_member(self):
        member_name = self.memberList.currentIndex().data()
        if member_name is None:
            return
        member = CommonDatas.get_instance().get_member_by_name(member_name)
        self.refresh_select_member(member)

    def click_date(self):
        date = self.calendar.selectedDate()
        if self.select_member is None:
            return
        day = int(date.day())
        self.detailedInfo.setText(self.select_member.name)
        self.detailedInfo.append(date.toString(Qt.ISODate))
        #打卡时间
        checkins_text = ""
        today_checkins = self.select_member.get_checkin_time_range(day)
        for checkin in today_checkins:
            checkins_text += "<{0:02d}:{1:02d}>".format(checkin.hour, checkin.minute)
        self.detailedInfo.append("打卡时间：" + checkins_text)
        self.detailedInfo.append("迟早早退时长：{0}".format(self.select_member.get_late_and_early_time(day)[0]))
        #请假时间
        leaves_text = ""
        today_leaves = self.select_member.get_leave_time_range(day)
        if (len(today_leaves) <= 0):
            leaves_text = "无"
        else:
            for leave in today_leaves:
                leaves_text +="<{0:02d}:{1:02d}>-><{2:02d}:{3:02d}>".format(leave[0].hour, leave[0].minute, leave[1].hour, leave[1].minute)
        self.detailedInfo.append("请假时间：" + leaves_text)

    def click_leave(self):
        member_name = self.leaveMember.currentText()
        self.edit_leave_member = CommonDatas.get_instance().get_member_by_name(member_name)
        self.leaveEdit.setText("")
        for leaveText in self.edit_leave_member.get_leave_text_list():
            self.leaveEdit.append(leaveText)

    def save_leave(self):
        leaveText = self.leaveEdit.toPlainText()
        member_name = self.leaveMember.currentText()
        self.edit_leave_member = CommonDatas.get_instance().get_member_by_name(member_name)
        leaveTextList = leaveText.splitlines()
        if self.edit_leave_member.set_leaves(leaveTextList):
            self.saveResultLabel.setText("成功")
            self.saveResultLabel.setStyleSheet("color:green")
        else:
            self.saveResultLabel.setText("失败")
            self.saveResultLabel.setStyleSheet("color:red")
        self.click_member()

    def save_in_out(self):
        if self.select_member is None:
            return
        self.select_member.set_config(in_date=self.inDateEdit.dateTime(), out_date=self.outDateEdit.dateTime())
        self.refresh_UI()

    def convert(self, filename, out_encoding="UTF-8"):
        #try:
        content = open(filename, 'rb').read()
        source_encoding = chardet.detect(content).get('encoding')
        if source_encoding.lower() == out_encoding.lower():
            return
        content = open(filename, 'r', encoding=source_encoding).read()
        content = content.replace("encoding=\"{0}\"".format(source_encoding), "encoding=\"{0}\"".format(out_encoding))
        with open(filename, 'w', encoding=out_encoding) as file:
            file.write(content)

        #except IOError as err:
            #print("I/O error:{0}".format(err))

    def delete_nr(self, filename):
        file = open(filename, 'r', encoding="UTF-8")
        content = file.read()
        content = content.replace("\r", r"").replace("\n", r"")
        with open(filename, 'w', encoding="UTF-8") as file:
            file.write(content)