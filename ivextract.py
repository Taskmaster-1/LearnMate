import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google AI
genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

def get_gemini_response(input_prompt, image_data, user_input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image_data[0], user_input])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def run_invoice_extractor():
    st.header("Invoice Extractor")

    uploaded_file = st.file_uploader("Upload Invoice (Image)", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice.", use_column_width=True)

        user_input = st.text_input("Ask a question about the invoice:", key="input")

        input_prompt = """
        You are an expert in understanding invoices.
        You will receive input images as invoices &
        you will have to answer questions based on the input image
        """

        if st.button("Analyze Invoice"):
            with st.spinner("Analyzing invoice..."):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data, user_input)
            
            st.subheader("Analysis Result")
            st.write(response)

#if __name__ == "__main__":
#    run_invoice_extractor()