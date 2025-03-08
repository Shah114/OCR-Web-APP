# 📝 OCR Web App with Flask & EasyOCR

This is a **Flask-based OCR web application** that extracts text from images (such as IDs or license plates) using **EasyOCR**. The extracted text is stored in an SQLite database and can be **edited, deleted, and downloaded as CSV or JSON**.

## **🚀 Features**
✅ **Upload images** and extract text  
✅ **Store extracted text** in a database  
✅ **Edit and delete OCR data**  
✅ **Download extracted text as CSV or JSON**  
✅ **Minimalist, warm light UI with animations**  

---

## **📌 Setup & Installation**
Follow these steps to set up the project on your local machine.

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Shah114/ocr-web-app.git
cd ocr-web-app
```
<br/>

### **2️⃣ Set Up a Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate      # On Windows
```
<br/>

### **3️⃣ Install Dependencies**
```
pip install -r requirements.txt
```
<br/>

### **4️⃣ Run the Flask App**
```bash
python app.py
```
✅ Your app is now running! Open http://127.0.0.1:5000/ in your browser.

<br/>

## **📌 Project Structure**
```bash
📂 ProjectOCR
│── 📂 static/uploads/      # Uploaded images
│── 📂 templates/           # HTML files
│   ├── index.html          # Frontend UI
│── 📂 data_storage/        # Database & stored OCR data
│   ├── database.db         # SQLite database
│   ├── ocr_data.csv        # Extracted text in CSV format
│   ├── ocr_data.json       # Extracted text in JSON format
│── app.py                  # Flask backend
│── requirements.txt        # Python dependencies
│── README.md               # Project documentation
```
<br/>

## **📌 Technologies Used**
* Python (Flask) - Web Framework
* EasyOCR - OCR Processing
* SQLite - Database Storage
* HTML + CSS - Frontend UI
* FontAwesome Icons - UI Enhancements

<br/>

## **📌 Future Enhancements**
🚀 Add Drag & Drop File Upload <br/>
🚀 Improve OCR Accuracy with Image Preprocessing <br/>
🚀 Deploy to Heroku or AWS

<br/>

## **📌 License**
This project is open-source and available under the MIT License.
<br/>
