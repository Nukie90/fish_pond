import sys
from PySide6.QtWidgets import QApplication
from ui.views.pond_window import PondWindow


def main():
    app = QApplication(sys.argv)
    window = PondWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
