from typing import Dict

import tkinter as tk
import pygubu

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/play_action.ui")

def build(root: tk.Tk, users: Dict) -> None:
    # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Get the time frame
    time_frame: tk.Frame = builder.get_object("time_remaining", main_frame)

    # For each user entry, fill in username for each team
    for team in users:
        count : int = 1
        for equipment_id in users[team]:
            builder.get_object(f"{team}_username_{count}", main_frame).configure(text=users[team][equipment_id][1])
            count += 1