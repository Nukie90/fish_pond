from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tempfile
import os


class FishWidget(Label):
    def __init__(self, parent, pond_window, fish):
        super().__init__(parent)
        self.pond_window = pond_window
        self.fish = fish

        self.configure(
            width=200,
            height=200,
        )

        self.load_gif(fish.data)

        self.remaining_lifetime = None
        self.after_id = None

        self.bind("<Button-1>", self.on_click)

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
                    self.gif_path = tmp_file.name

                # Load the GIF
                self.frames = []
                self.current_frame = 0

                gif = Image.open(self.gif_path)
                try:
                    while True:
                        photoframe = ImageTk.PhotoImage(gif.copy())
                        self.frames.append(photoframe)
                        gif.seek(len(self.frames))
                except EOFError:
                    pass

                if self.frames:
                    self.configure(image=self.frames[0])
                    self.after(100, self.update_frame)

        except Exception as e:
            print(f"Error loading GIF: {e}")

    def update_frame(self):
        """Update to next frame of GIF"""
        if hasattr(self, "frames") and self.frames:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.configure(image=self.frames[self.current_frame])
            self.after(100, self.update_frame)

    def start_lifetime(self, seconds: int):
        """Start the lifetime countdown"""
        self.remaining_lifetime = seconds
        self.check_lifetime()

    def check_lifetime(self):
        """Check if fish should still be alive"""
        if self.remaining_lifetime is not None:
            if self.remaining_lifetime <= 0:
                self.die()
            else:
                self.remaining_lifetime -= 1
                self.after_id = self.after(1000, self.check_lifetime)

    def die(self):
        """Handle fish death"""
        if self.after_id:
            self.after_cancel(self.after_id)

        # Clean up temporary file
        if hasattr(self, "gif_path") and os.path.exists(self.gif_path):
            try:
                os.unlink(self.gif_path)
            except:
                pass

        self.pond_window.remove_fish_by_widget(self)
        self.destroy()

    def on_click(self, event):
        """Handle click events"""
        if hasattr(self, "fish"):
            print(self.pond_window.get_info_text())
