# Modules
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import json
import easyocr
import sqlite3
import pandas as pd
from werkzeug.utils import secure_filename

# Making app
app = Flask(__name__)

# Define folder where database and data files should be stored
DATA_FOLDER = "D:/Projects/ProjectOCR/data_storage/"
os.makedirs(DATA_FOLDER, exist_ok=True)  # Ensure directory exists

# Paths for database and data files
DATABASE_PATH = os.path.join(DATA_FOLDER, "database.db")
CSV_PATH = os.path.join(DATA_FOLDER, "ocr_data.csv")
JSON_PATH = os.path.join(DATA_FOLDER, "ocr_data.json")

# Ensure upload folder exists
UPLOAD_FOLDER = "static/uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Database setup
def init_db():
    """Creates the SQLite database inside the specified folder."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ocr_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                extracted_text TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()  # Ensure DB is created

# Function: Save Data to CSV & JSON (Forces File Creation)
def save_data_to_files():
    with sqlite3.connect(DATABASE_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM ocr_data", conn)

        if df.empty:
            print("[INFO] Database is empty. Creating empty CSV and JSON files.")  # Debugging
            df = pd.DataFrame(columns=["id", "image_path", "extracted_text"])  # Ensure column structure
        
        df.to_csv(CSV_PATH, index=False)
        df.to_json(JSON_PATH, orient="records", indent=4)

# Ensure files are created on startup
save_data_to_files()

# Route: Homepage (Display Stored Data)
@app.route('/')
def index():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ocr_data")
        data = cursor.fetchall()
    
    return render_template('index.html', data=data)

# Route: Upload & Process Image
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['image']
    if file.filename == '':
        return redirect(url_for('index'))
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # Process OCR
    results = reader.readtext(file_path, detail=0)
    extracted_text = '\n'.join(results)
    
    # Store in DB
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ocr_data (image_path, extracted_text) VALUES (?, ?)", (file_path, extracted_text))
        conn.commit()
    
    # Update CSV & JSON immediately
    save_data_to_files()
    
    return redirect(url_for('index'))

# Route: Edit OCR Entry
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    new_text = request.form['extracted_text']
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE ocr_data SET extracted_text = ? WHERE id = ?", (new_text, id))
        conn.commit()
    
    # Update CSV & JSON after edit
    save_data_to_files()

    return redirect(url_for('index'))

# Route: Delete OCR Entry
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ocr_data WHERE id = ?", (id,))
        conn.commit()
    
    # Update CSV & JSON after deletion
    save_data_to_files()

    return redirect(url_for('index'))

# Route: Export Data as CSV
@app.route('/download_csv')
def download_csv():
    """Ensure the CSV file is created before download"""
    save_data_to_files()  # Force create/update file
    if not os.path.exists(CSV_PATH):
        return "Error: CSV file could not be found.", 500
    return send_file(CSV_PATH, as_attachment=True)

# Route: Export Data as JSON
@app.route('/download_json')
def download_json():
    """Ensure the JSON file is created before download"""
    save_data_to_files()  # Force create/update file
    if not os.path.exists(JSON_PATH):
        return "Error: JSON file could not be found.", 500
    return send_file(JSON_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)