
from PyQt5.QtWidgets import QDialog
from Scripts.UI.UIBase import UIBase
from Scripts.UI import MemberDataUI


class UIMemberData(MemberDataUI.Ui_MemberData, UIBase):
    def __init__(self):
        super().__init__()
        self.widget = QDialog()
        self.setupUi(self.widget)
        self.member = None
        #注册回调
        self.saveInOutButton.clicked.connect(self.save_config)


    def open(self, member):
        super().open()
        self.member = member
        if self.member is None:
            return
        self.widget.show()
        self.refresh_UI()

    def refresh_UI(self):
        self.nameLabel.setText(self.member.name)
        self.emailEdit.setText(self.member.email)
        self.bankCardEdit.setText(self.member.bank_card)
        self.professionEdit.setText(self.member.profession)
        self.department_1_Edit.setText(self.member.department_1)
        self.department_2_Edit.setText(self.member.department_2)
        self.inDateEdit.setDateTime(self.member.in_date)
        self.outDateEdit.setDateTime(self.member.out_date)

    def save_config(self):
        self.member.set_config(email=self.emailEdit.text(),
                               bank_card=self.bankCardEdit.text(),
                               profession=self.professionEdit.text(),
                               department_1=self.department_1_Edit.text(),
                               department_2=self.department_2_Edit.text(),
                               in_date=self.inDateEdit.dateTime(),
                               out_date=self.outDateEdit.dateTime())
        from Scripts.UI.UIMain import UIMain
        UIMain.get_instance().refresh_UI()
        self.refresh_UI()
