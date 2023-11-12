import pygubu
import tkinter as tk
import os 
import random
from networking import Networking
from typing import Dict

# If on Windows, import winsound, else import playsound for countdown music
if os.name == "nt":
    import winsound
else:
    import playsound

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

#Implementing play countdown timer for 6-minutes 
def update_timer(main_frame: tk.Frame, timer_label: tk.Label, seconds: int) -> None:
    # Update text being displayed in timer label
    mins, secs = divmod(seconds, 60)
    timer_label.config(text=f"Time Remaining: {mins:01d}:{secs:02d}")

    # If there is still time left, recursively call this function after 1 second
    # Otherwise, destroy countdown frame and start game
    if seconds > 0:
        seconds -= 1
        timer_label.after(1000, update_timer, main_frame, timer_label, seconds)
    else:
        main_frame.destroy()

def build(network: Networking, users: Dict, root: tk.Tk) -> None:
    filenames = os.listdir("res/moosic")
    file = random.choice(filenames)
    # Based on OS, play the countdown sound
    # Play sound asynchronously to prevent freezing
    if os.name == "nt":
        winsound.PlaySound("res/moosic/" + file, winsound.SND_ASYNC)
    else:
        playsound.playsound("res/moosic/" + file, block=False)

     # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    timer_label: tk.Label = builder.get_object("countdown_label", main_frame)
    seconds: int = 360

    update_score(users, main_frame)
    update_timer(main_frame, timer_label, seconds)

