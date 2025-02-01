from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, QSize, Signal, QUrl, QByteArray
from PySide6.QtGui import QMovie, QMouseEvent
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
import tempfile


class FishWidget(QLabel):
    clicked = Signal(object)

    def __init__(self, parent=None, pond=None, fish=None):
        super().__init__(parent)
        self.setFixedSize(QSize(200, 200))
        gif_url = fish.data

        self.network_manager = QNetworkAccessManager(self)
        self.network_manager.finished.connect(self.load_gif)
        self.network_manager.get(QNetworkRequest(QUrl(gif_url)))

        self.lifetime_timer = QTimer(self)
        self.lifetime_timer.timeout.connect(self.check_lifetime)
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_info)

        self.pond = pond
        self.fish = fish

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse click events"""
        self.clicked.emit(self)
        super().mousePressEvent(event)

    def start_lifetime(self, seconds: int):
        """Start the lifetime countdown"""
        self.remaining_lifetime = seconds
        self.lifetime_timer.start(1000)
        self.update_timer.start(1000)

    def check_lifetime(self):
        """Check if fish should still be alive"""
        self.remaining_lifetime -= 1
        if self.remaining_lifetime <= 0:
            self.die()

    def update_info(self):
        """Update fish information"""
        if self.pond and hasattr(self.pond, "update_fish_info"):
            self.pond.update_fish_info()

    def get_info_text(self) -> str:
        """Get formatted fish information"""
        if not self.fish:
            return "No fish information available"

        info = f"Name: {self.fish.name} | "
        info += f"Lifetime: {self.remaining_lifetime}s | "
        if self.fish.group_name != self.pond.pond.name:
            info += f"From: {self.fish.group_name}"
        else:
            info += "Local fish"
        return info

    def die(self):
        """Handle fish death"""
        self.lifetime_timer.stop()
        self.update_timer.stop()
        self.movie.stop()
        self.hide()

        if self.pond:
            self.pond.remove_fish_by_widget(self)
            self.pond.update_fish_info()

        self.deleteLater()

    def load_gif(self, reply):
        """Load GIF from network reply"""
        data = reply.readAll()
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
        temp_file.write(data)
        temp_file.close()

        self.movie = QMovie(temp_file.name)
        self.setMovie(self.movie)
        self.movie.start()
