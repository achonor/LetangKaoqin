import sys
from PyQt5.QtWidgets import QApplication

from Scripts.UI.UIMain import UIMain

def main():
    app = QApplication(sys.argv)
    uiMain = UIMain()
    uiMain.open()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()