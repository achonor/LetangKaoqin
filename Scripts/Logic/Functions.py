import re
import xml.dom.minidom
from datetime import datetime, timedelta
from PyQt5.QtCore import QDateTime
from openpyxl import load_workbook

WEEK_STR = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

def three_param_operator(flag_value, param1, param2):
    if flag_value:
        return param1
    return param2

def datetime2string(date_time):
    return date_time.strftime("%Y-%m-%d %H:%M")

def string2datetime(date_time_str):
    return datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

def QDateTime2string(q_date_time):
    return q_date_time.toString("yyyy-MM-dd hh:mm")

def string2QDateTime(date_time_str):
    return QDateTime.fromString(date_time_str, "yyyy-MM-dd hh:mm")

def timedelta2string(time_delta):
    ret_str = ""
    seconds = time_delta.total_seconds()
    if 86400 < seconds:
        ret_str += "{0}天".format(int(seconds / 86400))
    seconds = seconds % 86400
    ret_str += "{0}时".format(round(seconds / 3600, 1))
    return ret_str

def leave_string2ecxel_text(date_time_str_list):
    from Scripts.Data.CommonDatas import CommonDatas
    ret_str = ""
    for idx in range(0, len(date_time_str_list), 2):
        start_date = datetime.strptime(date_time_str_list[idx], "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(date_time_str_list[idx + 1], "%Y-%m-%d %H:%M")
        while start_date < end_date:
            day_end_date = CommonDatas.get_instance().create_work_time(start_date.day)[1]
            if end_date < day_end_date:
                day_end_date = end_date
            ret_str += "{0}月{1}日（{2}：{3:02d}-{4}：{5:02d}） ".format(start_date.month, start_date.day, start_date.hour,
                                                                  start_date.minute, day_end_date.hour, day_end_date.minute)
            if start_date.day == CommonDatas.get_instance().days_number:
                break
            else:
                start_date = CommonDatas.get_instance().create_work_time(start_date.day + 1)[0]
    return ret_str

def QDateTime2datetime(q_date_time):
    return string2datetime(QDateTime2string(q_date_time))

def datetime2QDateTime(date_time):
    return string2QDateTime(datetime2string(date_time))

def is_same_day(date1, date2):
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day

def get_node_value(node, *args):
    root = node
    for index in args:
        if root is None or root.childNodes.length <= index:
            return None
        root = root.childNodes[index]
    return root.nodeValue

def load_XML(file_path):
    dom_tree = xml.dom.minidom.parse(file_path)
    contents = dom_tree.getElementsByTagName("Worksheet")
    for content in contents:
        ss_dame = content.getAttribute("ss:Name")
        print(ss_dame)
        if "刷卡记录" == ss_dame:
            content_node = content.getElementsByTagName("Table")[0]
    if content_node is None:
        print("Error")
        return
    member_datas = {}
    rowList = content_node.getElementsByTagName("Row")
    for index, row in enumerate(rowList):
        cells = row.getElementsByTagName("Cell")
        if cells.length <= 0:
            continue
        firstValue = get_node_value(cells[0], 0, 0)
        # 检测是否是dateInterval
        if "考勤日期 : " == firstValue:
            dateStr = get_node_value(cells[1], 0, 0)
            tempList = re.findall(r"\d+", dateStr)
            for idx, temp in enumerate(tempList):
                tempList[idx] = int(temp)
            start_date = datetime(tempList[0], tempList[1], tempList[2])
            end_date = datetime(tempList[0], tempList[3], tempList[4])
            days_number = (end_date - start_date).days + 1
            print(start_date, end_date, days_number)
        # 获取员工信息
        if "工号 : " == firstValue:
            member = load_member_from_XML(start_date.year, start_date.month, rowList[index], rowList[index + 1])
            if member["name"] is not None:
                if member["name"] in member_datas:
                    #特殊情况，合并打卡记录就行
                    old_member = member_datas[member["name"]]
                    member["checkin_list"] = merge_checkins(member["checkin_list"], old_member["checkin_list"])
                member_datas[member["name"]] = member
    ret_dict = {}
    ret_dict["file_path"] = file_path
    ret_dict["start_date"] = start_date
    ret_dict["end_date"] =end_date
    ret_dict["days_number"] = days_number
    ret_dict["member_datas"] = member_datas
    return ret_dict

def load_member_from_XML(year, month, infoNode, checkInNode):
    ID = get_node_value(infoNode, 2, 0, 0)
    name = get_node_value(infoNode, 10, 0, 0)
    department = get_node_value(infoNode, 20, 0, 0)
    checkin_list = []
    checkins = checkInNode.getElementsByTagName("Cell")
    for index, checkIn in enumerate(checkins):
        checkinstr = get_node_value(checkIn, 0, 0)
        checkin_list.append(timetexts2time(checkinstr, year, month, index + 1))
    ret_dict = {}
    ret_dict["ID"] = ID
    ret_dict["name"] = name
    ret_dict["department"] = department
    ret_dict["checkin_list"] = checkin_list
    return ret_dict

def timetexts2time(timetexts, year, month, day):
    time_list = []
    if timetexts is None:
        return time_list
    temp_list = re.findall(r"\d{2}", timetexts)
    for index in range(0, len(temp_list), 2):
        time_list.append(datetime(year, month, day, int(temp_list[index]), int(temp_list[index + 1])))
    return time_list

def merge_checkins(checkins1, checkins2):
    if len(checkins1) <= 0:
        return checkins2
    if len(checkins2) <= 0:
        return checkins1
    ret_checins = []
    for index, value in enumerate(checkins1):
        checkin1 = checkins1[index]
        checkin2 = checkins2[index]
        checkin = []
        for idx in range(0, len(checkin1) + len(checkin2)):
            if len(checkin1) <= 0 or (0 < len(checkin2) and checkin2[0] < checkin1[0]):
                checkin.append(checkin2[0])
                checkin2 = checkin2[1:]
            elif len(checkin2) <= 0 or (0 < len(checkin1) and checkin1[0] < checkin2[0]):
                checkin.append(checkin1[0])
                checkin1 = checkin1[1:]
        ret_checins.append(checkin)
    return ret_checins

def weekday2string(weekday):
    return WEEK_STR[weekday]