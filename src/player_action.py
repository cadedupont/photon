import tkinter as tk
import pygubu

import player_entry

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/player_action.ui")

def build(root: tk.Tk) -> None:
    
    # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Get the time frame
    time_frame: tk.Frame = builder.get_object("time_remaining", main_frame)

    for team in users:
        count : int = 1
        for equipment_id in users[team]:
            count += 1
            builder.get_object(f"{team}_username_{count}", main_frame).insert(0, users[equipment_id][1])

    root.bind("<F5>", lambda event: on_f12(event, root, entry_ids))

