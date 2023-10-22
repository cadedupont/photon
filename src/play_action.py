from typing import Dict
from PIL import Image, ImageTk

import tkinter as tk
import pygubu
import cv2
import playsound
import os

from networking import Networking

# Import winsound if on Windows
if os.name == "nt":
    import winsound

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/play_action.ui")

def update_timer(timer_label: tk.Label, seconds: int, main_frame: tk.Frame, network: Networking) -> None:
    # Change contents of timer label
    timer_label.config(text=f"Game Starts In: {seconds} Seconds")

    # If seconds is greater than 0, decrement seconds and call this function again after 1 second
    if seconds > 0:
        seconds -= 1
        timer_label.after(1000, update_timer, timer_label, seconds, main_frame, network)
    else:
        # Destroy main frame and start game, transmitting start game code
        main_frame.destroy()
        network.transmit_start_game_code()

def update_video(video_label: tk.Label, cap: cv2.VideoCapture, frame_rate: int, video_width: int, video_height: int) -> None:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (video_width, video_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.config(image=photo)
        video_label.photo = photo
        video_label.after(1000 // frame_rate, update_video, video_label, cap, frame_rate, video_width, video_height)
    else:
        # Rewind the video to the beginning when it ends
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        update_video(video_label, cap, frame_rate, video_width, video_height)

def build(root: tk.Tk, users: Dict, network: Networking) -> None:
    # Based on OS, play the countdown sound
    if os.name == "nt":
        winsound.PlaySound("res/countdown.wav", winsound.SND_ASYNC)
    else:
        playsound.playsound("res/countdown.wav", False)

    # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Get the time frame and label
    countdown_frame: tk.Frame = builder.get_object("countdown_frame", main_frame)
    video_frame: tk.Frame = builder.get_object("video_frame", countdown_frame)
    timer_label: tk.Label = builder.get_object("countdown_label", main_frame)

    # For each user entry, fill in username for each team
    for team in users:
        count: int = 1
        for equipment_id in users[team]:
            builder.get_object(f"{team}_username_{count}", main_frame).configure(text=users[team][equipment_id][1])
            count += 1

    # Load the video
    cap: cv2.VideoCapture = cv2.VideoCapture("res/countdown.mp4")
    
    # Get the video's frame rate
    frame_rate: int = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the desired video size
    video_width: int = 500
    video_height: int = 500

    # Make the video label
    video_label: tk.Label = tk.Label(video_frame)
    video_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Initialize the countdown time
    seconds: int = 30

    # Start the countdown
    update_timer(timer_label, seconds, main_frame, network)

    # Start displaying the video
    update_video(video_label, cap, frame_rate, video_width, video_height)