import streamlit as st
from PIL import Image
import pytesseract
import PyPDF2

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

def run_invoice_extractor():
    st.title("Invoice Extractor")

    uploaded_file = st.file_uploader("Upload Invoice (Image/PDF)", type=['jpg', 'png', 'pdf'])

    if uploaded_file:
        with st.spinner("Extracting text..."):
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:
                image = Image.open(uploaded_file)
                text = extract_text_from_image(image)
        
        st.subheader("Extracted Invoice Text")
        st.write(text)
