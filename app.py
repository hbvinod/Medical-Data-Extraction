
#app.py

import streamlit as st
from medical_extractor import extract_text_from_pdf, extract_medical_info, save_to_csv, save_to_pdf

st.title("🩺 Medical Data Extraction Report")
uploaded_file = st.file_uploader("Upload PDF Medical Report", type="pdf")
use_ocr = st.checkbox("Use OCR (for scanned reports)", value=False)

if uploaded_file:
    st.success("PDF uploaded successfully.")
    text = extract_text_from_pdf(uploaded_file, use_ocr=use_ocr)
    st.subheader("Extracted Text")
    st.text_area("Text", text, height=300)

    if st.button("Extract Medical Info"):
        extracted = extract_medical_info(text)
        st.subheader("Extracted Medical Information")
        for k, v in extracted.items():
            st.write(f"**{k}**: {v}")

        if st.button("Download CSV"):
            save_to_csv(extracted)
            st.success("Saved as output.csv")

        if st.button("Download PDF"):
            save_to_pdf(extracted)
            st.success("Saved as output.pdf")



