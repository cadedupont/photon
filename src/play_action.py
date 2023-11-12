import pygubu
import tkinter as tk
from networking import Networking
from typing import Dict

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/play_action.ui")

def update_score(users: Dict, main_frame: tk.Frame) -> None:
        for team in users:
            for user in users[team]:
                builder.get_object(f"{team}_username_{user.user_row}", main_frame).config(text=user.username)
                builder.get_object(f"{team}_score_{user.user_row}", main_frame).config(text=user.game_score)
            total_score = sum([user.game_score for user in users[team]])
            builder.get_object(f"{team}_total_score", main_frame).config(text=total_score)
        main_frame.after(1000, update_score, users, main_frame)

def build(network: Networking, users: Dict, root: tk.Tk) -> None:
     # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    update_score(users, main_frame)