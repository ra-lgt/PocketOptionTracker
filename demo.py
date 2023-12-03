import tkinter as tk
from customtkinter import CTkLabel

class YourClass:
    def __init__(self):
        self.miss_rate = 0  # Initial value, replace with your actual initial value

        # Create the CTkLabel
        self.miss_rate_count = CTkLabel(
            master=tracker_frame,
            text=str(self.miss_rate),
            text_color="#E0E0E0",
            font=("Arial", 15)
        )
        self.miss_rate_count.grid(row=1, column=2, sticky=tk.E)

        # Set up a trace on self.miss_rate to automatically update the CTkLabel
        self.trace_id = None
        self.setup_trace()

    def setup_trace(self):
        # Set up a trace on self.miss_rate to automatically update the CTkLabel
        self.trace_id = self.miss_rate_count.register(self.update_miss_rate_label, '%P')
        self.miss_rate_count.configure(textvariable=self.trace_id)

    def update_miss_rate_label(self, *args):
        # Callback function to update the CTkLabel when self.miss_rate changes
        new_value = self.miss_rate_count.get()
        try:
            self.miss_rate = int(new_value)
        except ValueError:
            # Handle the case where the value is not a valid integer
            pass

    # Other methods and code for your class...

# Create an instance of YourClass
your_instance = YourClass()

# Example of changing self.miss_rate
your_instance.miss_rate = 42  # The CTkLabel should update automatically
