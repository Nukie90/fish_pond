import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from Front.View.PondUI import *

class PondUI(QMainWindow):
    def __init__(self):
        super(PondUI,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PondUI()
    window.show()
    sys.exit(app.exec())