import pygubu
import tkinter as tk
import os 
import random
import threading
from typing import Dict

import player_entry
from networking import Networking
from game_logic import GameState
from main import build_root, destroy_root

# If on Windows, import winsound, else import playsound for countdown music
if os.name == "nt":
    import winsound
else:
    import playsound

def build_new_game(root: tk.Tk, users: Dict, network: Networking) -> None:
    # Remove buttons from window
    for widget in root.winfo_children():
        widget.destroy()

    # Send back to player entry screen
    player_entry.build(root, users, network)

def destroy_current_game(root: tk.Tk, main_frame: tk.Frame, users: dict, network: Networking, game: GameState) -> None:
    # Destroy the main frame
    main_frame.destroy()

    # TODO: End networking thread

    # Clear the user dictionary
    users["red"].clear()
    users["green"].clear()

    # Destroy game object
    del game

    # Place button in center of root window
    restart_game_button: tk.Button = tk.Button(root, text="Restart Game", font=("Fixedsys", 16), bg="#FFFFFF", command=lambda: build_new_game(root, users, network))
    restart_game_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    end_game_button: tk.Button = tk.Button(root, text="End Game", font=("Fixedsys", 16), bg="#FFFFFF", command=lambda: destroy_root(root, network))
    end_game_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

def update_stream(game: GameState, action_stream: tk.Frame) -> None:
    # Add scroll effect to action stream with game.game_event_list queue
    if len(game.game_event_list) > 0:
        # Get the last event from the queue along with player name
        event: str = game.game_event_list.pop()
        player_name: str = event.split("hit", 1)[0].strip()

        # Create label for event and add to action stream
        event_label: tk.Label = tk.Label(action_stream, text=event, font=("Fixedsys", 16), bg="#FFFFFF")
        event_label.pack(side=tk.TOP, fill=tk.X)

        # Add B to player name if they hit a base
        if "hit green base" in event:
            for user in game.red_users:
                if user.username == player_name:
                    user.username = "B: " + user.username
        elif "hit red base" in event:
            for user in game.green_users:
                if user.username == player_name:
                    user.username = "B: " + user.username
        
        # Remove the last event from the bottom of the action stream
        if len(action_stream.winfo_children()) > 5:
            action_stream.winfo_children()[0].destroy()

    # Recursively call this function after 1 second to incrementally update action stream
    action_stream.after(1000, update_stream, game, action_stream)

def update_score(game: GameState, main_frame: tk.Frame, builder: pygubu.Builder) -> None:
    # Update scores for green team
    for user in game.green_users:
        builder.get_object(f"green_username_{user.row}", main_frame).config(text=user.username)
        builder.get_object(f"green_score_{user.row}", main_frame).config(text=user.game_score)
    builder.get_object("green_total_score", main_frame).config(text=game.green_team_score)

    # Update scores for red team
    for user in game.red_users:
        builder.get_object(f"red_username_{user.row}", main_frame).config(text=user.username)
        builder.get_object(f"red_score_{user.row}", main_frame).config(text=user.game_score)
    builder.get_object("red_total_score", main_frame).config(text=game.red_team_score)

    # Recursively call this function after 1 second to incrementally update scores
    main_frame.after(1000, update_score, game, main_frame, builder)

# Implementing play countdown timer for 6-minutes 
def update_timer(timer_label: tk.Label, seconds: int, root: tk.Tk, main_frame: tk.Frame, users: Dict, network: Networking, game: GameState) -> None:
    # Update text being displayed in timer label
    mins, secs = divmod(seconds, 60)
    timer_label.config(text=f"Time Remaining: {mins:01d}:{secs:02d}")

    # Continue counting down, destroy main frame when timer reaches 0
    if seconds > 0:
        seconds -= 1
        timer_label.after(1000, update_timer, timer_label, seconds, root, main_frame, users, network, game)
    else:
        destroy_current_game(root, main_frame, users, network, game)

def build(network: Networking, users: Dict, root: tk.Tk) -> None:
    # Load the UI file and create the builder
    builder: pygubu.Builder = pygubu.Builder()
    builder.add_from_file("src/ui/play_action.ui")

    # Select random game music file
    file = random.choice(os.listdir("res/moosic"))

    # Based on OS, play the game music
    # Play sound asynchronously to prevent freezing
    if os.name == "nt":
        winsound.PlaySound("res/moosic/" + file, winsound.SND_ASYNC)
    else:
        playsound.playsound("res/moosic/" + file, block=False)

     # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    timer_label: tk.Label = builder.get_object("countdown_label", main_frame)

    # Get action frame and prevent from resizing to fit label contents
    action_stream: tk.Frame = builder.get_object("action_stream_frame", main_frame)
    action_stream.pack_propagate(False)

    # Create game state model
    game: GameState = GameState(users)

    # Update score labels, timer, and action stream
    update_score(game, main_frame, builder)
    update_stream(game, action_stream)
    update_timer(timer_label, 5, root, main_frame, users, network, game)

    # Start thread for UDP listening
    game_thread: threading.Thread = threading.Thread(target=network.run_game, args=(game,), daemon = True)
    game_thread.start()
    # game_thread.join()