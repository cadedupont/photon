from dotenv import load_dotenv
from importlib import reload
from supabase import create_client, Client
from tkinter import messagebox
import os

# Run splash screen and player registration GUI
import splash
import register

# Load environment variables
load_dotenv()

# Create a new Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Get user input from GUI
info: dict = register.info

# Check whether user already exists in user table
user: dict = supabase.table("players").select("*").eq("username", info["username"]).execute()

# While user already exists, re-run registration GUI
while (user.data != []):
    # Display error message
    messagebox.showerror("Error", "Username already exists")

    # Re-run registration GUI
    reload(register)
    info: dict = register.info
    
    # Re-run query to check whether user already exists
    user: dict = supabase.table("players").select("*").eq("username", info["username"]).execute()

# Insert player into table and display success message
supabase.table("players").insert([info]).execute()
messagebox.showinfo("Success", "User successfully registered!")