# test_db.py
import pymongo

# --- PASTE YOUR FULL MONGO_URI CONNECTION STRING HERE ---
# --- Make sure the password is correct and there are no < > brackets ---
MONGO_URI = "mongodb+srv://CAREERPATHUSER:BH67OER45POBDJHKINAS9@cluster0.5zthmvl.mongodb.net/careerpathuser?retryWrites=true&w=majority&appName=Cluster0 "

print("Attempting to connect to MongoDB...")

try:
    # 1. Attempt to connect to the server
    client = pymongo.MongoClient(MONGO_URI)
    
    # 2. The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("✅ MongoDB server is reachable.")
    
    # 3. Try to access a specific database and list collections to test auth
    db = client.get_default_database() # This gets the DB name from your URI
    print(f"✅ Successfully connected to database: '{db.name}'")
    
    print("✅✅✅ CONNECTION SUCCESSFUL! ✅✅✅")
    
except pymongo.errors.ConfigurationError as e:
    print("❌ CONFIGURATION ERROR: The connection string is likely malformed.")
    print(f"   Details: {e}")

except pymongo.errors.OperationFailure as e:
    print("❌ AUTHENTICATION FAILED: Check your username and password.")
    print(f"   Details: {e}")

except pymongo.errors.ConnectionFailure as e:
    print("❌ CONNECTION FAILED: The server could not be reached. Check your firewall/network settings in Atlas.")
    print(f"   Details: {e}")

except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")