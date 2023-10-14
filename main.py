import time

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from flask import send_file
import io
from config import DATABASE_URI, BASE62, ALLOWED_EXTENSIONS  # Import variables from config.py


#BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"



#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# SQLite database configuration
#DATABASE_URI = 'sqlite:///file_storage.db'  # Change this to your desired database URI
engine = create_engine(DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define the SQLAlchemy model for the file table
class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    data = Column(LargeBinary, nullable=False)
    base62_result = Column(String(255), nullable=True)  # New column for Base62 result


# Create the table in the database (Run this once to initialize the database)
Base.metadata.create_all(engine)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            file_data = uploaded_file.read()

            # Calculate the Base62 result
            unique_number = generate_unique_number()
            base62_result = encode(unique_number, BASE62)

            # Store the file and Base62 result in the database
            session = Session()
            new_file = File(filename=filename, data=file_data, base62_result=base62_result)
            session.add(new_file)
            session.commit()
            session.close()

            return 'File uploaded successfully.'

    return render_template('upload.html')


@app.route('/download', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        file_id = request.form['file_id']
        session = Session()
        file_record = session.query(File).filter_by(id=file_id).first()

        if file_record:
            # Send the file data as a response with a custom filename
            return send_file(
                io.BytesIO(file_record.data),
                as_attachment=True,  # Treat as an attachment
                download_name=file_record.filename  # Custom filename
            )
        else:
            return 'File not found', 404

    # Query the database to fetch a list of available files
    session = Session()
    files = session.query(File).all()

    return render_template('download.html', files=files)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_number():
    # Get the IP address and port from the Flask request object
    host, port = request.host.split(':')

    # Remove dots from the IP address
    ip_address = host.replace('.', '')

    # Concatenate the IP address, port, and current Unix timestamp
    unique_number = ip_address + port + str(int(time.time() * 1000))

    # Check if the string is empty after removing '0'
    if not unique_number:
        unique_number = '0'  # If the string is empty, set it to '0'

    return unique_number


@app.route('/downloadbykeyword', methods=['GET'])
def download_by_keyword_form():
    return render_template('downloadbykeyword.html')


@app.route('/downloadbykeyword', methods=['POST'])
def download_file_by_keyword():
    if request.method == 'POST':
        keyword = request.form['keyword']
        session = Session()
        file_record = session.query(File).filter_by(base62_result=keyword).first()

        if file_record:
            # Send the file data as a response with a custom filename
            return send_file(
                io.BytesIO(file_record.data),
                as_attachment=True,  # Treat as an attachment
                download_name=file_record.filename  # Custom filename
            )
        else:
            return 'File not found for the specified keyword.', 404

@app.route('/serverinfo')
def print_server_info():
    # Call the generate_unique_number function
    unique_number = generate_unique_number()

    # Print the generated unique number to the console
    print(f"Unique Number: {unique_number}")

    # Convert the unique identifier to base 62
    base62_result = encode(unique_number, BASE62)

    # Print the base 62 representation
    print("Base 62 Representation:", base62_result)

    return "Unique Number printed to console."

def encode(unique_identifier, alphabet):

    unique_number = int(unique_identifier)

    if unique_number == 0:
        return alphabet[0]

    arr = []
    arr_append = arr.append
    _divmod = divmod
    base = len(alphabet)

    while unique_number:
        unique_number, rem = _divmod(unique_number, base)
        arr_append(alphabet[rem])

    arr.reverse()
    return ''.join(arr)




if __name__ == '__main__':
    app.run(debug=True)
