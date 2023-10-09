import tkinter as tk
import supabase
import pygubu

def build(root, supabase_client):
    # Load the UI file and create the builder
    builder: pygubu.Builder = pygubu.Builder()

    # Load the UI file
    builder.add_from_file("src/ui/player_entry.ui")

    # Place main frame in center of root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)