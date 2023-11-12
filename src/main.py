from typing import Dict, List

from dotenv import load_dotenv
from os import getenv

import tkinter as tk
import supabase

import splash_screen
import player_entry
from networking import Networking
from user import User
from game_logic import GameState

def build_root() -> tk.Tk:
    # Build main window, set title, make fullscreen
    root: tk.Tk = tk.Tk()
    root.title("Photon")
    root.iconbitmap("res/logo.ico")
    root.state("zoomed")
    root.configure(background="white")

    # Force window to fill screen, place at top left
    width: int = root.winfo_screenwidth()
    height: int = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+0+0")

    # Disable resizing
    root.resizable(False, False)

    # Return the root window
    return root

def destroy_root(root: tk.Tk) -> None:
    # Destroy the root window
    root.destroy()

def main() -> None:
    # Create the Supabase client
    load_dotenv()
    supabase_client: supabase.Client = supabase.create_client(
        getenv("SUPABASE_URL"),
        getenv("SUPABASE_KEY")
    )

    # Declare dictionary for storing user information
    # Format: { team: [User, User, ...] }
    users: Dict[str, List[User]] = {
        "green": [],
        "red": []
    }

    # Create networking object
    network: Networking = Networking()
    network.set_sockets()

    # Call build_root function to build the root window
    root: tk.Tk = build_root()

    # Bind escape key and window close button to destroy_root function
    root.bind("<Escape>", lambda event: destroy_root(root))
    root.protocol("WM_DELETE_WINDOW", lambda: destroy_root(root))

    # Build the splash screen
    splash: splash_screen = splash_screen.build(root)

    # After 3 seconds, destroy the splash screen and build the player entry screen
    # Play action screen will be built after F5 is pressed on player entry screen (see on_f5 function in src/player_entry.py)
    root.after(3000, splash.destroy)
    root.after(3000, player_entry.build, root, supabase_client, users, network)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()