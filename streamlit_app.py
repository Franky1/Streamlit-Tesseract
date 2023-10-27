import streamlit as st
# streamlit config
st.set_page_config(page_title="Local OCR", page_icon="📝", layout="wide", initial_sidebar_state="expanded")

import numpy as np
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                PDFPopplerTimeoutError, PDFSyntaxError)
import helpers.constants as constants
import helpers.opencv as opencv
import helpers.pdfimage as pdfimage
import helpers.tesseract as tesseract
import helpers.easy_ocr as easy_ocr
import controls.tesseract_controls as ts_controls
import controls.image_processing_controls as im_controls
import controls.upload_image_controls as up_controls
import controls.image_preview_controls as preview_controls
import controls.text_extraction_controls as txt_controls




# Initialize st.session_state
if 'image_processing_config' not in st.session_state:
    st.session_state.image_processing_config = {
        'Grayscale': True,
        'Denoising': False,
        'DenoisingStrength': 10,
        'Thresholding': False,
        'ThresholdLevel': 128,
        'Rotate90': False,
        'Angle90': 0,
        'RotateFree': False,
        'Angle': 0
    }

if 'tesseract_config' not in st.session_state:
    st.session_state['tesseract_config'] = tesseract.load_config()['tesseract']

# apply custom css
with open('helpers/style.css') as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# add streamlit title
st.title("Local OCR - Optical Character Recognition 📝")

# add streamlit markdown text
# st.markdown('''**Local OCR** - Optical Character Recognition using Tesseract, OpenCV and Streamlit.<br>
# This is a simple OCR demo app that can be used to extract text from images. Supported languages see below.
# ''', unsafe_allow_html=True)
st.markdown(f'''# {constants.flag_string}''')


with st.sidebar:
    with st.expander("OCR Engine Settings"):

        st.header("OCR Engine Selector")

        ocr_selected_engine = st.selectbox(label="Select OCR Engine", options = list(['TesseractOCR', 'EasyOCR']), index=0)

        st.write(ocr_selected_engine)

        st.markdown('---')

        if (ocr_selected_engine == 'TesseractOCR'):
            ts_controls.show_controls()
        elif (ocr_selected_engine == 'EasyOCR'):
            st.write("EasyCOR is Selected but not Implemented Yet!!!")

        st.markdown('---')

    with st.expander("Image Processing Settings"):
        im_controls.show_image_processing_controls()


# two column layout for image preprocessing options and image preview
col1, col2 = st.columns(spec=[2, 3], gap="large")
image = None

with col1:
    image = up_controls.show_upload_image_controls()

with col2:
    if image is not None:
        preview_controls.show_image_preview_controls(image)    
        txt_controls.show_text_extraction_contol(image)



