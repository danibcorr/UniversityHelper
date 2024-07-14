# %% Libraries

import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import cv2 
import numpy as np
from markdownify import markdownify as md
import PyPDF2

# %% Parameters for Streamlit

# Set the page configuration for Streamlit
st.set_page_config(page_title = "PDF2MD", page_icon = "📄", layout = "wide")
st.title("📄 PDF to Markdown")
st.sidebar.image("./images/logo.png")

# %% Functions

def preprocess_image(img: Image) -> Image:

    """
    Apply basic image preprocessing techniques to improve OCR accuracy.

    Args:
        img (Image): The input image.

    Returns:
        Image: The preprocessed image.
    """
    
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    return Image.fromarray(cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB))

def extract_text_from_pdf_ocr(pdf_file, ln: str) -> str or None:

    """
    Extract text from a PDF file using OCR.
    
    Args:
        pdf_file (BytesIO): The PDF file object.
    
    Returns:
        str: The extracted text from the PDF, or None if there was an error.
    """

    try:

        # Open the PDF file
        pdf_document = fitz.open(stream = pdf_file.read(), filetype = "pdf")
        text = ""

        for page_num in range(len(pdf_document)):

            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()

            # Save the page image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Apply image preprocessing
            img = preprocess_image(img)

            # Apply OCR to the image
            page_text = pytesseract.image_to_string(img, lang = ln)
            text += page_text + "\n"

        return text

    except Exception as e:

        st.error(f"Error extracting text from PDF using OCR: {e}")

        return None

def extract_text_from_pdf_pypdf2(pdf_file) -> str or None:

    """
    Extract text from a PDF file using PyPDF2.
    
    Args:
        pdf_file (BytesIO): The PDF file object.
    
    Returns:
        str: The extracted text from the PDF, or None if there was an error.
    """

    try:

        # Open the PDF file
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        text = ""

        for page in pdf_reader.pages:

            text += page.extractText() + "\n"

        return text

    except Exception as e:

        st.error(f"Error extracting text from PDF using PyPDF2: {e}")

        return None

def extract_text_from_pdf_ctrl_a(pdf_file) -> str or None:

    """
    Extract text from a PDF file by emulating Ctrl+A.
    
    Args:
        pdf_file (BytesIO): The PDF file object.
    
    Returns:
        str: The extracted text from the PDF, or None if there was an error.
    """

    try:

        # Open the PDF file
        pdf_document = fitz.open(stream = pdf_file.read(), filetype = "pdf")
        text = ""

        for page in pdf_document:

            text += page.getText() + "\n"

        return text

    except Exception as e:

        st.error(f"Error extracting text from PDF using Ctrl+A: {e}")

        return None

def convert_text_to_markdown(text: str) -> str:

    """
    Convert plain text to Markdown format.
    
    Args:
        text (str): The plain text to convert.
    
    Returns:
        str: The converted Markdown text.
    """

    markdown_text = md(text)

    return markdown_text

def main() -> None:

    """
    Run the Streamlit app to convert a PDF file to Markdown.
    """

    col1, col2 = st.columns(2)

    with col1:
            
        st.subheader("File Configuration")

        uploaded_file = st.file_uploader("Choose a PDF file", type = "pdf")

        output_path = st.text_input('Enter the output directory', '.')
        output_file = st.text_input('Enter the output file name', 'output') 
        output_file = f"{output_path}/{output_file}.md"

        ln = st.multiselect("List of available languages",
            pytesseract.get_languages(), ["eng"])
        ln = "+".join(ln)

    with col2:
        
        st.subheader("Method Configuration")

        extraction_method = st.selectbox("Select the extraction method", ["OCR", "PyPDF2", "Ctrl+A"])
        
        st.markdown(
            '''
            + PyPDF2 method may not work well with scanned PDFs or PDFs with complex layouts.
            + Ctrl+A method may not work well with PDFs that contain a lot of graphics or tables. 
            + The OCR method is generally the most accurate, but it can be slow and may not work well with PDFs that contain a lot of noise or distortion.'''
        )

    if uploaded_file is not None:

        if extraction_method == "OCR":

            text = extract_text_from_pdf_ocr(uploaded_file, ln)

        elif extraction_method == "PyPDF2":

            text = extract_text_from_pdf_pypdf2(uploaded_file)

        elif extraction_method == "Ctrl+A":

            text = extract_text_from_pdf_ctrl_a(uploaded_file)

        if text:

            markdown_text = convert_text_to_markdown(text)
            
            st.subheader("Extracted Text")
            st.text_area("Extracted Text", text, height = 300)
            
            save_button = st.button('Save as.md')
            
            if save_button:

                with open(output_file, 'w', encoding = 'utf-8') as f:

                    f.write(markdown_text)

                st.success(f"File saved as {output_file}")

# %% Main

if __name__ == '__main__':

    main()