from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QMovie
import requests
from io import BytesIO
import tempfile
import os


class FishWidget(QLabel):
    def __init__(self, parent, pond_window, fish):
        super().__init__(parent)
        self.pond_window = pond_window
        self.fish = fish

        self.setFixedSize(200, 200)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Initialize movie as None
        self.movie = None
        self.gif_path = None

        # Load the GIF
        self.load_gif(fish.data)

        self.remaining_lifetime = None
        self.lifetime_timer = None

        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

    def load_gif(self, url):
        """Load GIF from URL"""
        try:
            # Download GIF
            response = requests.get(url)
            if response.status_code == 200:
                # Save to temporary file
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".gif"
                ) as tmp_file:
                    tmp_file.write(response.content)
                    tmp_file.flush()  # Ensure all data is written
                    self.gif_path = tmp_file.name

                # Create and set up QMovie
                if os.path.exists(self.gif_path):
                    self.movie = QMovie(self.gif_path)
                    if self.movie.isValid():
                        self.setMovie(self.movie)
                        self.movie.start()
                    else:
                        print("Invalid GIF file")
                        self.cleanup_gif()
                else:
                    print("GIF file not found")

        except Exception as e:
            print(f"Error loading GIF: {e}")
            self.cleanup_gif()

    def cleanup_gif(self):
        """Clean up GIF resources"""
        if self.movie:
            self.movie.stop()
            self.movie = None

        if self.gif_path and os.path.exists(self.gif_path):
            try:
                os.unlink(self.gif_path)
                self.gif_path = None
            except Exception as e:
                print(f"Error cleaning up GIF file: {e}")

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
