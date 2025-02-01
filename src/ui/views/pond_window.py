from tkinter import *
import random
from datetime import datetime
import json
from core.mqtt_client import MqttClient
from core.pond import Pond, Fish
from ui.widgets.fish_widget import FishWidget
from PIL import Image, ImageTk
import os


class PondWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("Fish Pond")
        self.root.geometry("1080x720")
        self.root.configure(bg="#FAFAFA")

        # Initialize core components
        self.mqtt_client = MqttClient()
        self.mqtt_client.pond_window = self
        self.pond = Pond(name="DC Universe")
        self.fish_widgets = {}

        # Load pond background image
        self.pond_bg_image = None  # Initialize as None
        self.load_pond_background()

        self.setup_ui()
        self.setup_connections()

    def load_pond_background(self):
        """Load the pond background image"""
        try:
            # Get the path relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "pond.png")

            # Load and resize image to fit the main frame
            image = Image.open(image_path)
            image = image.resize((771, 341))
            self.pond_bg_image = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Failed to load pond background: {e}")

    def setup_ui(self):
        """Setup the UI components"""
        # Pond name label
        self.pond_name_label = Label(
            self.root,
            text="Pond DC Universe",
            font=("Times New Roman", 36, "bold"),
            bg="#FAFAFA",
            fg="black",
        )
        self.pond_name_label.place(x=300, y=30, width=480, height=41)

        # Main pond frame
        self.main_frame = Frame(
            self.root, bg="#F5F5F5", highlightbackground="black", highlightthickness=1
        )
        self.main_frame.place(x=159, y=110, width=771, height=341)

        # Add pond background image
        if self.pond_bg_image:
            self.pond_bg_label = Label(
                self.main_frame, image=self.pond_bg_image, bg="#F5F5F5"
            )
            self.pond_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Buttons frame
        self.buttons_frame = Frame(
            self.root, bg="#FAFAFA", highlightbackground="black", highlightthickness=1
        )
        self.buttons_frame.place(x=100, y=480, width=880, height=61)

        # Add Fish button
        self.add_fish_button = Button(
            self.buttons_frame,
            text="Add Fish",
            font=("Times New Roman", 18, "bold"),
            bg="#66CC99",
            fg="black",
            bd=0,
            command=self.handle_add_fish,
        )
        self.add_fish_button.place(x=60, y=10, width=230, height=41)

        # Send Fish button
        self.send_fish_button = Button(
            self.buttons_frame,
            text="Send Fish",
            font=("Times New Roman", 18, "bold"),
            bg="#FE9F06",
            fg="black",
            bd=0,
            command=self.handle_send_fish,
            state="disabled",
        )
        self.send_fish_button.place(x=330, y=10, width=230, height=41)

        # Connect button
        self.connect_button = Button(
            self.buttons_frame,
            text="Connect to MQTT",
            font=("Times New Roman", 18, "bold"),
            bg="#B0AFE6",
            fg="black",
            bd=0,
            command=self.handle_mqtt_connection,
        )
        self.connect_button.place(x=600, y=10, width=230, height=41)

        # Fish count frame
        self.count_frame = Frame(
            self.root, bg="#FAFAFA", highlightbackground="black", highlightthickness=1
        )
        self.count_frame.place(x=50, y=639, width=161, height=51)

        # Fish count label
        self.fish_count_label = Label(
            self.count_frame,
            text="Fish Count: 0",
            font=("Times New Roman", 18),
            bg="#FAFAFA",
            fg="black",
        )
        self.fish_count_label.place(x=20, y=10)

    def setup_connections(self):
        """Setup event handlers"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def handle_mqtt_connection(self):
        """Handle MQTT connection"""
        try:
            self.mqtt_client.connect()
            self.connect_button.configure(state="disabled", text="Connected")
            self.send_fish_button.configure(state="normal")
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.connect_button.configure(text="Failed")
            self.root.after(3000, self.reset_connect_button)

    def reset_connect_button(self):
        """Reset connect button text after failed connection"""
        self.connect_button.configure(text="Connect to MQTT")

    def handle_add_fish(self):
        """Handle adding a new fish to the pond"""
        fish = self.pond.add_fish()
        self.create_fish_widget(fish)
        print(f"Added fish with name: {fish.name}, lifetime: {fish.lifetime} seconds")

    def handle_received_fish(self, message):
        """Handle receiving a fish from another pond"""
        try:
            data = json.loads(message.payload)
            print(data)

            fish = Fish(
                name=data["name"],
                group_name=data["group_name"],
                lifetime=data["lifetime"],
                data=data["data"],
            )

            self.pond.fishes[fish.name] = fish
            self.create_fish_widget(fish)
            fish_info = f"Received fish from {data['group_name']}, name: {data['name']}, lifetime: {data['lifetime']} seconds"
            print(fish_info)

        except Exception as e:
            print(f"Error handling received fish: {e}")

    def handle_send_fish(self):
        """Handle sending a fish to another pond"""
        if not self.mqtt_client.is_connected():
            print("Cannot send fish: Not connected to MQTT broker")
            return

        try:
            send_to = "DC_Universe2"

            if not self.pond.fishes:
                print("No fish available to send!")
                return

            name, fish = random.choice(list(self.pond.fishes.items()))

            self.mqtt_client.send_fish(
                name=name,
                group_name=self.pond.name,
                lifetime=fish.lifetime,
                send_to=send_to,
                data=fish.data,
            )

            self.fish_widgets[name].die()
            print(f"Sent fish with name: {name} to {send_to}")
        except Exception as e:
            print(f"Failed to send fish: {e}")

    def create_fish_widget(self, fish: Fish):
        """Create and setup a fish widget"""
        # If we have a background image, make fish widget parent the main_frame
        parent = self.main_frame
        fish_widget = FishWidget(parent, self, fish)

        # Random position within the pond frame
        x = random.randint(0, self.main_frame.winfo_width() - 200)
        y = random.randint(0, self.main_frame.winfo_height() - 200)
        fish_widget.place(x=x, y=y)
        fish_widget.lift()

        # Start lifetime countdown
        remaining_lifetime = fish.remaining_lifetime
        if remaining_lifetime > 0:
            fish_widget.start_lifetime(int(remaining_lifetime))

            # Store reference to widget
            self.fish_widgets[fish.name] = fish_widget
            self.update_fish_label()
        else:
            fish_widget.destroy()

    def update_fish_label(self):
        """Update the fish count label in the UI"""
        self.fish_count_label.configure(text=f"Fish Count: {len(self.fish_widgets)}")

    def remove_fish_by_widget(self, fish_widget):
        """Remove fish from pond and UI when its lifetime ends"""
        fish_id_to_remove = None

        for fish_id, widget in self.fish_widgets.items():
            if widget == fish_widget:
                fish_id_to_remove = fish_id
                break

        if fish_id_to_remove:
            self.fish_widgets.pop(fish_id_to_remove, None)
            self.pond.fishes.pop(fish_id_to_remove, None)
            self.update_fish_label()

    def on_closing(self):
        """Handle window closing"""
        self.mqtt_client.disconnect()
        self.root.destroy()

    def run(self):
        """Start the application"""
        self.root.mainloop()
