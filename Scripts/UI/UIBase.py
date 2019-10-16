import os
from PyQt5.QtWidgets import QFileDialog

class UIBase(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.widget = None

    def open(self):
        pass

    def close(self):
        pass

    def open_file_dialog(self, **kwargs):
        title = "选取文件"
        default_path = "./"
        filename_filter = ""
        if "title" in kwargs:
            title = kwargs["title"]
        if "default_path" in kwargs:
            default_path = kwargs["default_path"]
        if "extension" in kwargs:
            for name in kwargs["extension"]:
                filename_filter += "文件类型 ({0})".format(name)
                filename_filter += ";;"
            filename_filter = filename_filter[0:-2]
        file_path, file_type = QFileDialog.getOpenFileName(self.widget, title, default_path, filename_filter)
        if not os.path.isfile(file_path):
            return None
        return file_path

    def open_dir_dialog(self, **kwargs):
        title = "选取文件"
        default_path = "./"
        if "title" in kwargs:
            title = kwargs["title"]
        if "default_path" in kwargs:
            default_path = kwargs["default_path"]
        dir = QFileDialog.getExistingDirectory(self.widget, title, default_path)
        if not os.path.isdir(dir):
            return None
        return dir