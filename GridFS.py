from pymongo import MongoClient
from gridfs import GridFS

# MongoDB connection settings
MONGO_URI = 'mongodb://localhost:27017/'  # Update with your MongoDB URI
client = MongoClient(MONGO_URI)
db = client['hackathon']  # Use the "hackathon" database
fs = GridFS(db, collection='uploads')  # Use the "uploads" collection in GridFS

# Function to upload content to GridFS
def upload_content_to_gridfs():
    content = b"This is a test file content."
    filename = "test.txt"

    with fs.new_file(filename=filename, content_type="text/plain") as grid_file:
        grid_file.write(content)

if __name__ == "__main__":
    upload_content_to_gridfs()
