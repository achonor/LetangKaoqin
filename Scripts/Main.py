import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication

from Scripts.UI.UIMain import UIMain
#pyinstaller --hidden-import pandas -F -w Scripts/Main.py
def main():
    app = QApplication(sys.argv)
    uiMain = UIMain()
    uiMain.open()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()