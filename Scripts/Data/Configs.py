# -*- coding:utf8 -*-
import json
import os
from datetime import datetime

JSON_PATH = r"configs.json"
TEMP_JSON_PATH = r"temp_configs.json"
DEFAULT_CONFIG = {
    "work_time": [[8, 30], [17, 45]],
    "lunch_break": [[12, 00], [13, 30]],
    "fines": [[5, 2], [8, 5], [15, 7], [1440, 10]],
    "member": {},
    "settings": {
        "detail_table_path": "",
        "summary_table_path": "",
        "out_path": ""
    }
}

MEMBER_CONFIG = {
    "email": "",
    "bank_card": "",
    "profession": "",
    "department_1": "",
    "department_2": "",
    "in_date": "2019-03-18 08:30",
    "out_date": "9999-03-18 08:30"
}

DEFAULT_TEMP_CONFIG = {
    "leaves_times": {},
    "added_checkins": {},
    "work_time_table": []
}

class Configs(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.content = None
        self.temp_content = None
        self.load_json()
        self.load_temp_json()

    def load_json(self):
        if not os.path.exists(JSON_PATH):
            self.content = DEFAULT_CONFIG
            self.save_json()
        file = open(JSON_PATH, "r", encoding="utf-8")
        content = file.read()
        self.content = json.loads(content)
        print(self.content)

    def load_temp_json(self):
        if not os.path.exists(TEMP_JSON_PATH):
            self.temp_content = {}
            self.save_temp_json()
        file = open(TEMP_JSON_PATH, "r", encoding="utf-8")
        content = file.read()
        self.temp_content = json.loads(content)
        print(self.temp_content)

    def save_json(self):
        new_content = None
        if os.path.exists(JSON_PATH):
            with open(JSON_PATH, "r", encoding="utf-8") as file:
                new_content = file.read()
        try:
            new_content = json.dumps(self.content, ensure_ascii=False, indent=4)
        except Exception as exc:
            print("内容无法转换成json")
        else:
            with open(JSON_PATH, "w", encoding="utf-8") as file:
                file.write(new_content)

    def save_temp_json(self):
        with open(TEMP_JSON_PATH, "w", encoding="utf-8") as file:
            file_content = json.dumps(self.temp_content, ensure_ascii=False, indent=4)
            file.write(file_content)

    def get_config(self, config_name):
        return self.content.get(config_name)

    def set_config(self, config_name, value):
        self.content[config_name] = value

    def get_year_month_config(self):
        cur_temp_config = None
        from Scripts.Data.CommonDatas import CommonDatas
        start_date = CommonDatas.get_instance().start_date
        year_str = str(start_date.year)
        month_str = str(start_date.month)
        if year_str not in self.temp_content:
            self.temp_content[year_str] = {}
        year_config = self.temp_content[year_str]
        if month_str not in year_config:
            year_config[month_str] = DEFAULT_TEMP_CONFIG
            for day in range(1, CommonDatas.get_instance().days_number + 1):
                cur_date = CommonDatas.get_instance().create_datetime(day=day)
                year_config[month_str]["work_time_table"].append(cur_date.weekday() <= 4)
            self.save_temp_json()
        cur_temp_config = year_config[month_str]
        return cur_temp_config

    def get_temp_config(self, config_name):
        cur_temp_config = self.get_year_month_config()
        return cur_temp_config.get(config_name)

    def set_temp_config(self, config_name, value):
        cur_temp_config = self.get_year_month_config()
        cur_temp_config[config_name] = value

    def get_member_config(self, member_name):
        member_dict = self.get_config("member")
        if not member_name in member_dict:
            member = MEMBER_CONFIG
            member_dict[member_name] = member
            self.save_json()
        return member_dict[member_name]

    def set_member_config(self, member_name, value):
        member_dict = self.get_config("member")
        member_dict[member_name] = value
        self.save_json()

    def get_member_leave_temp_config(self, member_name):
        leaves_temp_config = self.get_temp_config("leaves_times")
        if member_name not in leaves_temp_config:
            leaves_temp_config[member_name] = []
            self.save_temp_json()
        return leaves_temp_config[member_name]

    def set_member_leave_temp_config(self, member_name, value):
        leaves_temp_config = self.get_temp_config("leaves_times")
        leaves_temp_config[member_name] = value
        self.save_temp_json()

    def get_member_checkin_temp_config(self, member_name):
        checkin_temp_config = self.get_temp_config("added_checkins")
        if member_name not in checkin_temp_config:
            checkin_temp_config[member_name] = {}
            self.save_temp_json()
        return checkin_temp_config[member_name]

    def set_member_checkin_temp_config(self, member_name, value):
        checkin_temp_config = self.get_temp_config("added_checkins")
        checkin_temp_config[member_name] = value
        self.save_temp_json()

    def get_fine_number(self, duration):
        if 0 == duration:
            return 0
        fines = self.get_config("fines")
        for fine in fines:
            if duration <= fine[0]:
                return fine[1]
        return 99999

    def get_is_work_time(self, day):
        work_time_table = self.get_temp_config("work_time_table")
        return work_time_table[day - 1]

    def set_is_work_time(self, day, value):
        work_time_table = self.get_temp_config("work_time_table")
        work_time_table[day - 1] = value