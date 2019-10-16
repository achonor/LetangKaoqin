from datetime import datetime, timedelta
from Scripts.Data.Configs import Configs
from Scripts.Logic import Functions
from Scripts.Data.CommonDatas import CommonDatas
import re

class Member(object):
    def __init__(self):
        self.ID = None
        self.name = None
        self.department = None
        self.checkin_list = None
        self.leave_dict = None
        self.added_checkin_list = None
        self.profession = None
        self.department_1 = None
        self.department_2 = None
        self.email = None
        self.bank_card = None
        self.in_date = None
        self.out_date = None
        self.ignore = False
        self.lack_checkin_count = 0
        self.late_or_early_count = 0
        self.late_or_early_duration = 0
        self.late_early_time_dict = None
        self.late_or_early_fine_number = 0
        self.work_days = 0
        self.holidays = 0
        self.day_leave_durations = None
        self.leave_durations = 0

    def __str__(self):
        return "ID: %s name: %s department: %s checkin_list: %s" % (self.ID, self.name, self.department, self.checkin_list)

    def reset_data(self, member_data):
        self.ID = member_data["ID"]
        self.name = member_data["name"]
        self.department = member_data["department"]
        self.checkin_list = member_data["checkin_list"]
        self.ignore = False
        self.load_config_data()

    def load_leaves_data(self):
        leave_text_list = Configs.get_instance().get_member_leave_temp_config(self.name)
        self.set_leaves(leave_text_list, False)

    def load_added_checkins(self):
        start_date = CommonDatas.get_instance().start_date
        self.added_checkin_list = []
        added_checkins_config = Configs.get_instance().get_member_checkin_temp_config(self.name)
        for day in range(1, CommonDatas.get_instance().days_number + 1):
            checkins = []
            day_checkins = []
            if str(day) in added_checkins_config:
                checkins = added_checkins_config[str(day)]
            for checkin in checkins:
                day_checkins.append(CommonDatas.get_instance().create_datetime(day=day, hour=checkin[0], minute=checkin[1]))
            self.added_checkin_list.append(day_checkins)

    def load_config_data(self):
        start_date = CommonDatas.get_instance().start_date
        member_config = Configs.get_instance().get_member_config(self.name)
        self.email = member_config["email"]
        self.bank_card = member_config["bank_card"]
        self.profession = member_config["profession"]
        self.department_1 = member_config["department_1"]
        self.department_2 = member_config["department_2"]
        self.in_date = Functions.string2datetime(member_config["in_date"])
        self.out_date = Functions.string2datetime(member_config["out_date"])

        self.ignore = (self.out_date.year == start_date.year and self.out_date.month < start_date.month)
        if self.in_date.year == start_date.year and start_date.month < self.in_date.month:
            #还没入职
            self.ignore = True
        if self.in_date.year == start_date.year and self.in_date.month == start_date.month and 15 < self.in_date.day:
            #上个月15号以后入职不统计
            self.ignore = True

    def calc_all_data(self):
        #缺卡
        self.lack_checkin_count = 0
        #迟到早退
        self.late_or_early_count = 0
        self.late_or_early_duration = 0
        self.late_or_early_fine_number = 0
        self.late_early_time_dict = {}
        #工作天数
        self.work_days = 0
        #放假天数
        self.holidays = 0
        #请假时长
        self.day_leave_durations = []
        self.leave_durations = timedelta()
        #重新加载配置
        self.load_leaves_data()
        self.load_added_checkins()
        self.load_config_data()
        for index in range(1, CommonDatas.get_instance().days_number + 1):
            if not self.in_company(index):
                #没入职
                pass
            elif not Configs.get_instance().get_is_work_time(index):
                #休息日
                self.holidays += 1
            else:
                self.work_days += 1
                duration, late, early = self.calc_late_and_early_time(index)
                self.late_early_time_dict[index] = [duration, late, early]
                if 0 < duration:
                    self.late_or_early_count += 1
                    self.late_or_early_duration += duration
                    self.late_or_early_fine_number += Configs.get_instance().get_fine_number(duration)
                if 30 <= duration:
                    self.lack_checkin_count += 1
            #请假时长
            leave_duration_am = timedelta()
            leave_duration_pm = timedelta()
            leave_times = self.get_leave_time_range(index)
            lunch_break_start, lunch_break_end = CommonDatas.get_instance().create_lunch_break(index)
            for leave_time in leave_times:
                if leave_time[0] < lunch_break_start:
                    leave_duration_am += leave_time[1] - leave_time[0]
                else:
                    leave_duration_pm += leave_time[1] - leave_time[0]
            self.day_leave_durations.append((leave_duration_am, leave_duration_pm))
            self.leave_durations += (leave_duration_am + leave_duration_pm)
        if 5 < self.late_or_early_count:
            self.late_or_early_fine_number *= 2

    def calc_late_and_early_time(self, day):
        checkins = self.get_checkin_time_range(day)
        start, end = self.get_day_work_time(day)
        if end <= start:
            return 0, 0, 0
        if len(checkins) <= 0:
            return 1440, 720, 720
        if len(checkins) <= 1:
            return 480, 240, 240
        late_time = 0
        early_time = 0
        if start < checkins[0]:
            late_time = int((checkins[0] - start).total_seconds() / 60)
        if checkins[-1] < end:
            early_time = int((end - checkins[-1]).total_seconds() / 60)
        return late_time + early_time, late_time, early_time

    def get_day_work_time(self, day):
        start, end = CommonDatas.get_instance().create_work_time(day)
        if Functions.is_same_day(start, self.in_date):
            start = self.in_date
        if Functions.is_same_day(end, self.out_date):
            end = self.out_date
        #午休
        lunch_break_start, lunch_break_end = CommonDatas.get_instance().create_lunch_break(day)
        #获取请假时间
        leave_times = self.get_leave_time_range(day)
        for leave_time in leave_times:
            if leave_time[0]  <= start and start < leave_time[1]:
                start = leave_time[1]
            if lunch_break_start <= start and start <= lunch_break_end:
                start = lunch_break_end
            if end <= leave_time[1] and leave_time[0] < end:
                end = leave_time[0]
            if lunch_break_start <= end and end <= lunch_break_end:
                end = lunch_break_start
        return start, end

    def add_leave(self, start, end):
        try:
            work_time = Configs.get_instance().get_config("work_time")
            start_date = Functions.string2datetime(start)
            end_date = Functions.string2datetime(end)
            while start_date < end_date:
                lunch_break_start, lunch_break_end = CommonDatas.get_instance().create_lunch_break(start_date.day)
                tempend_date = CommonDatas.get_instance().create_work_time(start_date.day)[1]
                if end_date < tempend_date:
                    tempend_date = end_date
                if start_date < lunch_break_start and lunch_break_end < tempend_date:
                    #午休的时间拆开
                    self._add_leave(start_date, lunch_break_start)
                    self._add_leave(lunch_break_end, tempend_date)
                else:
                    self._add_leave(start_date, tempend_date)
                if start_date.day == CommonDatas.get_instance().days_number:
                    break
                else:
                    start_date = CommonDatas.get_instance().create_work_time(start_date.day + 1)[0]
        except Exception as e:
            print(e)
            return False
        return True

    def _add_leave(self, start_date, end_date):

        if start_date.day not in self.leave_dict:
            self.leave_dict[start_date.day] = []
        self.leave_dict[start_date.day].append([start_date, end_date])

    def set_leaves(self, time_text_list, need_save=True):
        if 1 == len(time_text_list) % 2:
            return False
        self.leave_dict = {}
        for idx in range(0, len(time_text_list), 2):
            if not self.add_leave(time_text_list[idx], time_text_list[idx + 1]):
                return False
        if need_save:
            Configs.get_instance().set_member_leave_temp_config(self.name, time_text_list)
        return True

    def set_config(self, **kwargs):
        member_config = Configs.get_instance().get_member_config(self.name)
        if "email" in kwargs:
            member_config["email"] = kwargs["email"]
        if "bank_card" in kwargs:
            member_config["bank_card"] = kwargs["bank_card"]
        if "profession" in kwargs:
            member_config["profession"] = kwargs["profession"]
        if "department_1" in kwargs:
            member_config["department_1"] = kwargs["department_1"]
        if "department_2" in kwargs:
            member_config["department_2"] = kwargs["department_2"]
        if "in_date" in kwargs:
            member_config["in_date"] = Functions.QDateTime2string(kwargs["in_date"])
        if "out_date" in kwargs:
            member_config["out_date"] = Functions.QDateTime2string(kwargs["out_date"])
        Configs.get_instance().save_json()
        self.load_config_data()

    def add_checkin(self, day, time):
        added_checkins_config = Configs.get_instance().get_member_checkin_temp_config(self.name)
        day_str = str(day)
        if day_str not in added_checkins_config:
            added_checkins_config[day_str] = []
        day_checkins = added_checkins_config[day_str]
        day_checkins.append(time)
        day_checkins.sort(key=lambda key: (key[0], key[1]))
        Configs.get_instance().save_temp_json()
        self.load_added_checkins()

    def remove_all_checkins(self, day):
        day_str = str(day)
        added_checkins_config = Configs.get_instance().get_member_checkin_temp_config(self.name)
        if day_str not in added_checkins_config:
            return
        added_checkins_config.pop(day_str)
        Configs.get_instance().save_temp_json()
        self.load_added_checkins()

    def get_checkin_time_range(self, day):
        if self.added_checkin_list is None:
            self.load_added_checkins()
        ret_checkin_list = self.checkin_list[day - 1] + self.added_checkin_list[day - 1]
        ret_checkin_list.sort()
        return ret_checkin_list

    def get_late_and_early_time(self, day):
        if day in self.late_early_time_dict:
            return self.late_early_time_dict[day]
        return [0, 0, 0]

    def get_leave_time_range(self, day):
        if self.leave_dict is None:
            self.load_leaves_data()
        if day not in self.leave_dict:
            self.leave_dict[day] = []
        return self.leave_dict[day]

    def get_leave_text_list(self):
        return Configs.get_instance().get_member_leave_temp_config(self.name)

    def get_leave_count(self):
        return int(len(self.get_leave_text_list()) / 2)

    def get_leave_duration(self, day=None):
        if day is not None:
            am_duration, pm_duration = self.day_leave_durations[day - 1]
            return am_duration + pm_duration, am_duration, pm_duration
        else:
            return self.leave_durations

    def get_attendance(self):
        ret_attendance = -round(self.leave_durations.total_seconds() / 3600, 1)
        for day in range(1, CommonDatas.get_instance().days_number + 1):
            if not self.in_company(day):
                ret_attendance -= round(CommonDatas.get_instance().get_work_day_duration().total_seconds() / 3600, 1)
        return ret_attendance

    def in_company(self, day):
        today = CommonDatas.get_instance().create_datetime(day=day)
        if self.in_date <= today or Functions.is_same_day(today, self.in_date):
            if today <= self.out_date or Functions.is_same_day(today, self.out_date):
                return True
        return False
    def is_late_or_early(self, day):
        return self.is_late(day) or self.is_early(day)

    def is_late(self, day):
        return 0 < self.late_early_time_dict[day][1]

    def is_early(self, day):
        return 0 < self.late_early_time_dict[day][2]