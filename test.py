# Test use of Supabase client in Python
from supabase import create_client, Client
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Create a new Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Print first 20 users in user table
for row in supabase.table("users").select("*").lte('id', 20).execute().data:
    print(row['username'])