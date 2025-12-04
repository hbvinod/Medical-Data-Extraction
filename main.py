import pytesseract
import cv2
import fitz  # PyMuPDF
import pandas as pd 
import re
import spacy
import scispacy
from PIL import Image
import io

# Load SciSpaCy model
nlp = spacy.load("en_core_sci_sm")

# Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path, use_ocr=False):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        if use_ocr:
            gray = cv2.cvtColor(cv2.cvtColor(pix.samples, cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray)
        else:
            text = page.get_text()
        
        full_text += text + "\n"
    
    return full_text

def extract_medical_info(text):
    data = {}
    doc = nlp(text)

    data['Entities'] = []
    for ent in doc.ents:
        data['Entities'].append({
            "text": ent.text,
            "label": ent.label_
        })

    # Simple patterns
    name = re.findall(r'Patient Name[:\-]?\s*(.*)', text, re.IGNORECASE)
    age = re.findall(r'Age[:\-]?\s*(\d+)', text, re.IGNORECASE)
    gender = re.findall(r'Gender[:\-]?\s*(Male|Female|Other)', text, re.IGNORECASE)
    diagnosis = re.findall(r'Diagnosis[:\-]?\s*(.*)', text, re.IGNORECASE)
    prescription = re.findall(r'Prescriptions?[:\-]?\s*(.*)', text, re.IGNORECASE)

    if name: data["Patient Name"] = name[0]
    if age: data["Age"] = age[0]
    if gender: data["Gender"] = gender[0]
    if diagnosis: data["Diagnosis"] = diagnosis[0]
    if prescription: data["Prescription"] = prescription[0]

    return data

def save_to_csv(data, filename='output.csv'):
    flat_data = {k: str(v) for k, v in data.items()}
    df = pd.DataFrame([flat_data])
    df.to_csv(filename, index=False)

def save_to_pdf(data, filename="output.pdf"):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for k, v in data.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=1)
    
    pdf.output(filename)
