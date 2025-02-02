from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QMovie
import os


class FishWidget(QLabel):
    def __init__(self, parent, pond_window, fish):
        super().__init__(parent)
        self.pond_window = pond_window
        self.fish = fish

        self.setFixedSize(200, 200)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Initialize movie
        self.movie = None

        # Load the GIF
        self.load_gif(fish.group_name)

        self.remaining_lifetime = None
        self.lifetime_timer = None

        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

    def load_gif(self, group_name):
        """Load GIF"""
        try:
            gif_path = os.path.join(
                "src", "ui", "resources", "images", f"{group_name}.gif"
            )

            if os.path.exists(gif_path):
                self.movie = QMovie(gif_path)
                if self.movie.isValid():
                    self.setMovie(self.movie)
                    self.movie.start()
                else:
                    print(f"Invalid GIF file for group: {group_name}")
                    self.cleanup_gif()
            else:
                print(f"GIF file not found for group: {group_name}")

        except Exception as e:
            print(f"Error loading GIF: {e}")
            self.cleanup_gif()

    def cleanup_gif(self):
        """Clean up GIF resources"""
        if self.movie:
            self.movie.stop()
            self.movie = None

    def start_lifetime(self, seconds: int):
        """Start the lifetime countdown"""
        self.remaining_lifetime = seconds
        self.lifetime_timer = QTimer(self)
        self.lifetime_timer.timeout.connect(self.check_lifetime)
        self.lifetime_timer.start(1000)  # 1 second interval

    def check_lifetime(self):
        """Check if fish should still be alive"""
        if self.remaining_lifetime is not None:
            if self.remaining_lifetime <= 0:
                self.die()
            else:
                self.remaining_lifetime -= 1

    def die(self):
        """Handle fish death"""
        if self.lifetime_timer:
            self.lifetime_timer.stop()

        self.cleanup_gif()
        self.pond_window.remove_fish_by_widget(self)
        self.deleteLater()

    def mousePressEvent(self, event):
        """Handle click events"""
        if hasattr(self, "fish"):
            print(f"Clicked fish: {self.fish.name}")
        super().mousePressEvent(event)
