from pymongo import MongoClient
import urllib.parse

# MongoDB connection setup
username = urllib.parse.quote_plus("kjxsofttechpvtltd")
password = urllib.parse.quote_plus("KJXSOFTTECH123")
connection_string = f"mongodb+srv://{username}:{password}@kjxwebsite.3mup0.mongodb.net/?retryWrites=true&w=majority&appName=kjxwebsite"

try:
    # Establish a connection to the MongoDB cluster
    client = MongoClient(connection_string)
    
    # Access the database
    db = client['KJXWebsite']  # Your database name is KJXWebsite
    
    # Access the collection
    collection = db['Users data']  # Your collection name is Users data
    
    # Sample document to insert
    sample_document = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "+1234567890",
        "problem_statement": "Sample problem statement for testing."
    }
    
    # Insert the sample document into the collection
    result = collection.insert_one(sample_document)
    
    # Print success message
    print(f"Document inserted with _id: {result.inserted_id}")
    
except Exception as e:
    print(f"An error occurred: {e}")
