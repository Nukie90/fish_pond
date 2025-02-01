from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QMovie
from pathlib import Path


class FishWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(200, 200))

        gif_path = str(Path(__file__).parent.parent / "resources/images/fish.gif")
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)

        self.movie.start()

        self.lifetime_timer = QTimer(self)
        self.lifetime_timer.timeout.connect(self.check_lifetime)

    def start_lifetime(self, seconds: int):
        """Start the lifetime countdown"""
        self.remaining_lifetime = seconds
        self.lifetime_timer.start(1000)

    def check_lifetime(self):
        """Check if fish should still be alive"""
        self.remaining_lifetime -= 1
        if self.remaining_lifetime <= 0:
            self.die()

    def die(self):
        """Handle fish death"""
        self.lifetime_timer.stop()
        self.movie.stop()
        self.hide()
        self.deleteLater()
