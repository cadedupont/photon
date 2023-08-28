from tkinter import messagebox
import pygubu

# Create builder
builder = pygubu.Builder()
builder.add_from_file("res/register.ui")

# Create root window
root = builder.get_object("root")
root.iconbitmap("res/logo.ico")
root.focus_force()

# Place window in center of screen
width = 300
height = 210
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# Get widgets
first_name = builder.get_object("first_name_entry")
last_name = builder.get_object("last_name_entry")
username = builder.get_object("username_entry")
submit_button = builder.get_object("submit_button")

# Make first_name entry widget focused by default
first_name.focus_force()

# Define tab order
widgets = [first_name, last_name, username, submit_button]
for widget in widgets:
    widget.lift()

# Bind enter and escape keys to submit and destroy functions
root.bind("<Return>", lambda event: submit_button.invoke())
root.bind("<Escape>", lambda event: exit(1))

# If user clicks submit button, get user information and destroy root window
def submit():
    # Get user information
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

    # Destroy root window
    root.destroy()

# Bind submit function to submit button
submit_button.configure(command=submit)

# Run root window main loop
root.mainloop()