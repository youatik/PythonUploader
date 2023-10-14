from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from flask import send_file
import io


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

# SQLite database configuration
DATABASE_URI = 'sqlite:///file_storage.db'  # Change this to your desired database URI
engine = create_engine(DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define the SQLAlchemy model for the file table
class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    data = Column(LargeBinary, nullable=False)

# Create the table in the database (Run this once to initialize the database)
Base.metadata.create_all(engine)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            file_data = uploaded_file.read()

            # Store the file in the database
            session = Session()
            new_file = File(filename=filename, data=file_data)
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
'''

@app.route('/download/<int:file_id>')
def download_file(file_id):
    session = Session()
    file_record = session.query(File).filter_by(id=file_id).first()

    if file_record:
        # Send the file data as a response
        return send_file(
            io.BytesIO(file_record.data),
            as_attachment=True,  # Treat as an attachment
            download_name=file_record.filename  # Custom filename
        )
    else:
        return 'File not found', 404
'''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
