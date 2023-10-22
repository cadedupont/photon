from dotenv import load_dotenv
from os import getenv

import tkinter as tk
import supabase

import splash_screen
import player_entry

# Create the Supabase client
load_dotenv()
supabase_client: supabase.Client = supabase.create_client(
    getenv("SUPABASE_URL"),
    getenv("SUPABASE_KEY")
)

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

# Bind escape key to exit
root.bind("<Escape>", lambda event: root.destroy())

def main() -> None:
    # Build the splash screen
    splash: splash_screen = splash_screen.build(root)

    # After 3 seconds, destroy the splash screen and build the player entry screen
    root.after(3000, splash.destroy)
    root.after(3000, player_entry.build, root, supabase_client)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()