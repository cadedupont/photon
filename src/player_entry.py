import tkinter as tk
from tkinter import messagebox
import pygubu
from networking import Networking

# Load the UI file and create the builder
builder: pygubu.Builder = pygubu.Builder()
builder.add_from_file("src/ui/player_entry.ui")

database_response = None
def on_tab(event, root, supabase_client, entry_ids: dict):
    # Make database_response global
    global database_response

    # Get the entry field ID
    # If key doesn't exist, do nothing
    entry_field_id: str = entry_ids[event.widget.winfo_id()]
    if entry_field_id == None:
        return

    # If the entry field ID is an equipment ID field, transmit equipment ID
    if "equipment_id" in entry_field_id:
        # If equipment ID input is not an integer, display error message and refocus entry field to clear input
        if not event.widget.get().isdigit():
            messagebox.showerror("Error", "Equipment ID must be an integer")
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: event.widget.focus_set())
            return

        # Transmit equipment ID
        Networking().transmit_equipment_code(event.widget.get())

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

        # If the user exists, autofill username entry field
        if database_response.data != []:
            builder.get_object(entry_field_id.replace("user_id", "username"), root).insert(0, database_response.data[0]["username"])

            # Jump to next row's equipment ID entry field if not on last row
            row: int = int(entry_field_id.split("_")[-1])
            if row != 15:
                root.after_idle(lambda: builder.get_object(entry_field_id.replace(f"user_id_{row}", f"equipment_id_{row + 1}"), root).focus_set())

    # If the user tabs from the username entry field, insert the user into the database if they don't already exist
    elif "username" in entry_field_id and database_response.data == []:
        # Attempt to insert the user into the database, display error message if POST request fails
        user_id_widget: tk.Entry = builder.get_object(entry_field_id.replace("username", "user_id"), root)
        try:
            supabase_client.table("users").insert({
                "id": user_id_widget.get(),
                "username": event.widget.get()
            }).execute()
        except Exception as e:
            messagebox.showerror("Error", e)
            user_id_widget.delete(0, tk.END)
            event.widget.delete(0, tk.END)
            root.after_idle(lambda: user_id_widget.focus_set())
            return
        
        # If POST request was successful, display success message
        messagebox.showinfo("Success", "User successfully added to database!")

def build(root, supabase_client):
    # Place main frame in center of root window
    main_frame: tk.Frame = builder.get_object("master", root)
    main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Get the team frames
    teams_frame: tk.Frame = builder.get_object("teams", main_frame)
    red_frame: tk.Frame = builder.get_object("red_team", teams_frame)
    green_frame: tk.Frame = builder.get_object("green_team", teams_frame)

    # Create a dictionary of process IDs and their corresponding entry field IDs
    entry_ids: dict = {}
    for i in range(1, 16):
        # Add red team entry field IDs
        entry_ids[builder.get_object(f"red_equipment_id_{i}", red_frame).winfo_id()] = f"red_equipment_id_{i}"
        entry_ids[builder.get_object(f"red_user_id_{i}", red_frame).winfo_id()] = f"red_user_id_{i}"
        entry_ids[builder.get_object(f"red_username_{i}", red_frame).winfo_id()] = f"red_username_{i}"

        # Add green team entry field IDs
        entry_ids[builder.get_object(f"green_equipment_id_{i}", green_frame).winfo_id()] = f"green_equipment_id_{i}"
        entry_ids[builder.get_object(f"green_user_id_{i}", green_frame).winfo_id()] = f"green_user_id_{i}"
        entry_ids[builder.get_object(f"green_username_{i}", green_frame).winfo_id()] = f"green_username_{i}"

    # Place focus on first entry field
    builder.get_object("red_equipment_id_1", red_frame).focus_set()

    # Bind tab key to on_tab function
    root.bind("<Tab>", lambda event: on_tab(event, root, supabase_client, entry_ids))