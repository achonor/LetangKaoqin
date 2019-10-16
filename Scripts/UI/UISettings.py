import os
from Scripts.UI import SettingsUI
from PyQt5.QtWidgets import QWidget, QDialog
from Scripts.UI.UIBase import UIBase
from Scripts.Data.Configs import Configs
from Scripts.Logic import Functions

class UISettings(SettingsUI.Ui_Settings, UIBase):
    def __init__(self):
        super().__init__()
        self.widget = QDialog()
        self.setupUi(self.widget)
        self.settings_configs = None

        self.detailPathButton.clicked.connect(self.select_detail_table_path)
        self.summaryPathButton.clicked.connect(self.select_summary_table_path)
        self.outPathButton.clicked.connect(self.select_out_path)
        self.detailPathEdit.returnPressed.connect(self.save_config)
        self.summaryPathEdit.returnPressed.connect(self.save_config)
        self.outPathEdit.returnPressed.connect(self.save_config)

    def open(self):
        super().open()
        self.widget.show()
        self.refresh_UI()

    def refresh_UI(self):
        self.settings_configs = Configs.get_instance().get_config("settings")
        detail_table_path = self.settings_configs["detail_table_path"]
        summary_table_path = self.settings_configs["summary_table_path"]
        out_path = self.settings_configs["out_path"]
        if os.path.isfile(detail_table_path):
            self.detailPathEdit.setText(detail_table_path)
        if os.path.isfile(summary_table_path):
            self.summaryPathEdit.setText(summary_table_path)
        if os.path.isdir(out_path):
            self.outPathEdit.setText(out_path)

    def select_detail_table_path(self):
        self.select_table_path("detail_table_path")

    def select_summary_table_path(self):
        self.select_table_path("summary_table_path")

    def select_table_path(self, table_key):
        default_path = os.path.dirname(self.settings_configs[table_key])
        select_path = self.open_file_dialog( default_path=default_path, extension=["*.xlsx", "*.xls"])
        if select_path is None:
            return
        self.settings_configs[table_key] = select_path
        Configs.get_instance().save_json()
        self.refresh_UI()

    def select_out_path(self):
        default_path = self.settings_configs["out_path"]
        select_path = self.open_dir_dialog(default_path=default_path)
        if select_path is None:
            return
        self.settings_configs["out_path"] = select_path
        Configs.get_instance().save_json()
        self.refresh_UI()

    def save_config(self):
        if os.path.isdir(self.outPathEdit.text()):
            self.settings_configs["out_path"] = self.outPathEdit.text()
        if os.path.isfile(self.detailPathEdit.text()):
            self.settings_configs["detail_table_path"] = self.detailPathEdit.text()
        if os.path.isfile(self.summaryPathEdit.text()):
            self.settings_configs["summary_table_path"] = self.summaryPathEdit.text()
