from datetime import datetime, timedelta

class CommonDatas(object):
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
        self.file_path = None
        self.start_date = None
        self.end_date = None
        self.days_number = 30
        self.member_dict = None

    def reset_data(self, data_dict):
        self.file_path = data_dict["file_path"]
        self.start_date = data_dict["start_date"]
        self.end_date = data_dict["end_date"]
        self.days_number = data_dict["days_number"]
        self.member_dict = {}
        from Scripts.Data.Member import Member
        for name, data in data_dict["member_datas"].items():
            self.member_dict[name] = Member()
            self.member_dict[name].reset_data(data)

    def get_member_by_name(self, name):
        return self.member_dict.get(name)

    def get_all_member_dict(self, contant_out=False):
        if contant_out is True:
            return self.member_dict
        ret_dict = {}
        for key, value in self.member_dict.items():
            if value.ignore is False:
                ret_dict[key] = value
        return ret_dict

    def create_datetime(self, **kwargs):
        if "year" not in kwargs:
            kwargs["year"] = self.start_date.year
        if "month" not in kwargs:
            kwargs["month"] = self.start_date.month
        return datetime(**kwargs)

    def create_work_time(self, day):
        from Scripts.Data.Configs import Configs
        work_time = Configs.get_instance().get_config("work_time")
        start_time = self.create_datetime(day=day, hour=work_time[0][0], minute=work_time[0][1])
        end_time = self.create_datetime(day=day, hour=work_time[1][0], minute=work_time[1][1])
        return start_time, end_time

    def create_lunch_break(self, day):
        from Scripts.Data.Configs import Configs
        lunch_break = Configs.get_instance().get_config("lunch_break")
        start_time = self.create_datetime(day=day, hour=lunch_break[0][0], minute=lunch_break[0][1])
        end_time = self.create_datetime(day=day, hour=lunch_break[1][0], minute=lunch_break[1][1])
        return start_time, end_time

    def get_work_day_duration(self):
        work_time_start, work_time_end = self.create_work_time(1)
        lunch_break_start, lunch_break_end = self.create_lunch_break(1)
        return (lunch_break_start - work_time_start) + (work_time_end - lunch_break_end)