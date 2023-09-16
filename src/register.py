from tkinter import Tk, messagebox, Entry, Button
from pygubu import Builder

# Create builder
builder: Builder = Builder()
builder.add_from_file("../res/register.ui")

# Create root window
root: Tk = builder.get_object("root")
root.iconbitmap("../res/logo.ico")
root.focus_force()

# Place window in center of screen
width: int = 300
height: int = 210
x: int = (root.winfo_screenwidth() // 2) - (width // 2)
y: int = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Get widgets
first_name: Entry = builder.get_object("first_name_entry")
last_name: Entry = builder.get_object("last_name_entry")
username: Entry = builder.get_object("username_entry")
submit_button: Button = builder.get_object("submit_button")

# Make cursor focus on first name entry field by default
first_name.focus_force()

# Define tab order of widgets
widgets = [first_name, last_name, username, submit_button]
for widget in widgets:
    widget.lift()

# If user clicks submit button, get user information and destroy root window
def submit():
    # Get user information, declare as global to access in main.py
    global info
    info = {
        "first_name": first_name.get(),
        "last_name": last_name.get(),
        "username": username.get()
    }

    # If any fields are empty, display error message
    for key, value in info.items():
        if value == "":
            messagebox.showerror("Error", "Please fill out all fields")
            return
        else:
            # Strip leading and trailing whitespace from user input
            info[key] = value.strip()

    # Check if first and last name contain only letters and spaces
    if not all(char.isalpha() or char.isspace() for char in info["first_name"] + info["last_name"]):
        messagebox.showerror("Error", "Please enter only letters for first and last name")
        return

    # Destroy root window
    root.destroy()

# Bind submit function to submit button
submit_button.configure(command=submit)

# If user presses enter key, call submit function
root.bind("<Return>", lambda event: submit_button.invoke())

# If user presses escape key, exit program
root.bind("<Escape>", lambda event: exit(0))

# Run root window main loop
root.mainloop()