from typing import Dict
from PIL import Image, ImageTk

import tkinter as tk
import pygubu
import cv2

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/play_action.ui")

def update_timer(timer_label: tk.Label, seconds: int, time_frame: tk.Frame) -> None:
    timer_label.config(text=f"Time left: {seconds} seconds")
    if seconds > 0:
        seconds -= 1
        timer_label.after(1000, update_timer)
    else:
        time_frame.destroy()

def update_video(video_label: tk.Label, cap: cv2.VideoCapture, frame_rate: int, video_width: int, video_height: int) -> None:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (video_width, video_height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            video_label.config(image=photo)
            video_label.photo = photo
            video_label.after(1000 // frame_rate, update_video)  # Adjust for video frame rate
        else:
            # Rewind the video to the beginning when it ends
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            update_video()

def build(root: tk.Tk, users: Dict) -> None:
    # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Get the time frame
    time_frame: tk.Frame = builder.get_object("time_remaining", main_frame)

    # For each user entry, fill in username for each team
    for team in users:
        count: int = 1
        for equipment_id in users[team]:
            builder.get_object(f"{team}_username_{count}", main_frame).configure(text=users[team][equipment_id][1])
            count += 1

    cap = cv2.VideoCapture("res/NineLives2.mp4")
    
    # Get the video's frame rate and total frame count
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Define the desired video size
    video_width, video_height = 800, 700

    # Create a label for the video
    video_label = tk.Label(root)
    video_label.pack()

    # Initialize the countdown time
    seconds = 60

    # Create a label to display the countdown
    timer_label = tk.Label(root, text=f"Time left: {seconds} seconds", font=("Helvetica", 20))
    timer_label.pack(pady=20)

    # Start the countdown
    update_timer(timer_label, seconds, time_frame)

    # Start displaying the video
    update_video(video_label, cap, frame_rate, video_width, video_height)