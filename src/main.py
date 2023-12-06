from typing import Dict, List
from dotenv import load_dotenv
from platform import system
import os
import tkinter as tk
import supabase

from networking import Networking
from user import User
from game_logic import GameState
import splash_screen
import player_entry

if os.name == "nt":
    import winsound

# Create the Supabase client
load_dotenv()
supabase_client: supabase.Client = supabase.create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def build_root() -> tk.Tk:
    # Build main window, set title, make fullscreen
    root: tk.Tk = tk.Tk()
    root.title("Photon")
    root.configure(background="white")

    # If platform is not Linux, set state to zoomed and include icon
    if system() != "Linux":
        root.state("zoomed")
        root.iconbitmap("res/photon.ico")

    # Force window to fill screen, place at top left
    width: int = root.winfo_screenwidth()
    height: int = root.winfo_screenheight()
    root.geometry(f"{width}x{height}+0+0")

    # Disable resizing
    root.resizable(False, False)

    # Return the root window
    return root

def destroy_root(root: tk.Tk, network: Networking) -> None:
    # Stop sounds from playing if on Windows
    if os.name == "nt":
        winsound.PlaySound(None, winsound.SND_ASYNC)

    # Close network sockets
    network.close_sockets()

    # Destroy the root window
    root.destroy()

def main() -> None:
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
    root.bind("<Escape>", lambda event: destroy_root(root, network))
    root.protocol("WM_DELETE_WINDOW", lambda: destroy_root(root, network))

    # Build the splash screen
    splash: splash_screen = splash_screen.build(root)

    # After 3 seconds, destroy the splash screen and build the player entry screen
    # Play action screen will be built after F5 is pressed on player entry screen (see on_f5 function in src/player_entry.py)
    root.after(3000, splash.destroy)
    root.after(3000, player_entry.build, root, users, network)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
