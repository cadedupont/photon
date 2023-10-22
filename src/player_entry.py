from typing import Dict

from tkinter import messagebox
import tkinter as tk
import pygubu

from networking import Networking

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/player_entry.ui")

database_response = None
def on_tab(event: tk.Event, root: tk.Tk, supabase_client, entry_ids: Dict, users: Dict) -> None:
    # Make database response and users dictionary global
    global database_response

    # Get the entry field ID
    # If key doesn't exist, do nothing
    entry_field_id: str = entry_ids.get(event.widget.winfo_id())
    if entry_field_id is None:
        return
    
    # If the entry field ID is an equipment ID field, transmit equipment ID
    if "equipment_id" in entry_field_id:
        # If equipment ID input is not an integer, display error message and refocus entry field to clear input
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "Equipment ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return
        
        # Get the equipment ID
        equipment_id: int = int(event.widget.get())

        # Check if equipment ID is between 0 and 100
        if equipment_id < 0 or equipment_id > 100:
            messagebox.showerror("Error", "Equipment ID must be between 0 and 100")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        # Check if equipment ID is already in use
        if equipment_id in users["green"] or equipment_id in users["red"]:
            messagebox.showerror("Error", "Equipment ID is already in use")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

    # If the entry field ID is a user ID field, query database for user with matching ID
    elif "user_id" in entry_field_id:
        # If entry field is empty or not an integer, display error message and refocus entry field to clear input
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "User ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        # Query the database for the user with the matching ID
        database_response = supabase_client.table("users").select("*").eq("id", event.widget.get()).execute()

        # If user already exists in the database, autofill username entry field
        if database_response.data:
            equipment_id: int = int(builder.get_object(entry_field_id.replace("user_id", "equipment_id"), root).get())
            user_id: int = int(database_response.data[0]["id"])
            username: str = database_response.data[0]["username"]
            
            # If user already exists in the users dictionary, display an error message and refocus entry field to clear input
            if user_id in users["green"] or user_id in users["red"]:
                messagebox.showerror("Error", "User has already signed up for this match")
                event.widget.delete(0, tk.END)
                root.after_idle(lambda: event.widget.focus_set())
                return

            # Add user information to the users dictionary, specifying the team
            users["green" if "green" in entry_field_id else "red"][equipment_id] = (user_id, username)

            # Autofill the username entry field
            builder.get_object(entry_field_id.replace("user_id", "username"), root).insert(0, username)

            # Jump to the next row's equipment ID entry field if not on the last row
            row: int = int(entry_field_id.split("_")[-1])
            if row != 15:
                next_entry_field = builder.get_object(entry_field_id.replace(f"user_id_{row}", f"equipment_id_{row + 1}"), root)
                root.after_idle(lambda: next_entry_field.focus_set())

    # If the user tabs from the username entry field, insert the user into the database if they don't already exist
    elif "username" in entry_field_id and database_response.data == []:

        # TODO: If the user goes back and deletes the username or user ID, remove the user from the users dictionary

        # Get the equipment ID entry contents
        equipment_id: int = int(builder.get_object(entry_field_id.replace("username", "equipment_id"), root).get())

        # Get the user ID entry field box (need contents along with box for refocusing)
        user_id_widget: tk.Entry = builder.get_object(entry_field_id.replace("username", "user_id"), root)

        # Get contents of the user ID entry field and username entry field
        user_id: int = int(user_id_widget.get())
        username = event.widget.get()

        # Place user information in the users dictionary, specifying the team
        users["green" if "green" in entry_field_id else "red"][equipment_id] = (user_id, username)

        # Attempt to insert the user into the database, display an error message if the POST request fails
        try:
            supabase_client.table("users").insert({
                "id": user_id,
                "username": username
            }).execute()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            user_id_widget.delete(0, tk.END)
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: user_id_widget.focus_set())
            return

        # If the POST request was successful, display a success message
        messagebox.showinfo("Success", "User successfully added to the database!")

def on_f12(event: tk.Event, root: tk.Tk, entry_ids: Dict, users: Dict) -> None:
    # Clear all entry fields
    for entry_id in entry_ids: 
        builder.get_object(entry_ids[entry_id], root).delete(0, tk.END)

        # Clear users dictionary 
        users.clear()

        # Refocus the first entry field 
        builder.get_object("green_equipment_id_1", root).focus_set()

# f5 key to open play action screen and have 30 second timer before game starts and 6 minute game timer
def on_f5(main_frame: tk.Tk, root: tk.Tk, users: Dict, event: tk.Event = None) -> None:
    root.unbind("<F12>")
    
    # Destroy main_frame
    main_frame.destroy()

    # Build the player action screen
    import play_action
    play_action.build(root, users)

def build(root: tk.Tk, supabase_client, users: Dict) -> None:
    # Place the main frame in the center of the root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Get the team frames
    teams_frame: tk.Frame = builder.get_object("teams", main_frame)
    red_frame: tk.Frame = builder.get_object("red_team", teams_frame)
    green_frame: tk.Frame = builder.get_object("green_team", teams_frame)

    # Create a dictionary of process IDs and their corresponding entry field IDs
    entry_ids: Dict = {}
    for i in range(1, 16):
        # Add red team entry field IDs
        entry_ids[builder.get_object(f"red_equipment_id_{i}", red_frame).winfo_id()] = f"red_equipment_id_{i}"
        entry_ids[builder.get_object(f"red_user_id_{i}", red_frame).winfo_id()] = f"red_user_id_{i}"
        entry_ids[builder.get_object(f"red_username_{i}", red_frame).winfo_id()] = f"red_username_{i}"

        # Add green team entry field IDs
        entry_ids[builder.get_object(f"green_equipment_id_{i}", green_frame).winfo_id()] = f"green_equipment_id_{i}"
        entry_ids[builder.get_object(f"green_user_id_{i}", green_frame).winfo_id()] = f"green_user_id_{i}"
        entry_ids[builder.get_object(f"green_username_{i}", green_frame).winfo_id()] = f"green_username_{i}"

    # Place focus on the first entry field
    builder.get_object("green_equipment_id_1", red_frame).focus_set()

    # Bind keys to lambda functions
    root.bind("<Tab>", lambda event: on_tab(event, root, supabase_client, entry_ids, users))
    root.bind("<KeyPress-F12>", lambda event: on_f12(event, root, entry_ids, users))
    root.bind("<KeyPress-F5>", lambda event: on_f5(main_frame, root, users, event))

    # Bind continue button to F5 function for moving on to play action screen
    cont_button: tk.Button = builder.get_object("submit", main_frame)
    cont_button.configure(command=lambda: on_f5(main_frame, root, users))