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
            language, language_short, psm, timeout = ts_controls.show_controls()
        elif (ocr_selected_engine == 'EasyOCR'):
            st.write("EasyCOR is Selected but not Implemented Yet!!!")

        st.markdown('---')

    with st.expander("Image Processing Settings"):

        # st.header("Image Preprocessing")
        # st.write("Check the boxes below to apply preprocessing to the image.")
        # cGrayscale = st.checkbox(label="Grayscale", value=True)
        # cDenoising = st.checkbox(label="Denoising", value=False)
        # cDenoisingStrength = st.slider(label="Denoising Strength", min_value=1, max_value=40, value=10, step=1)
        # cThresholding = st.checkbox(label="Thresholding", value=False)
        # cThresholdLevel = st.slider(label="Threshold Level", min_value=0, max_value=255, value=128, step=1)
        # cRotate90 = st.checkbox(label="Rotate in 90° steps", value=False)
        # angle90 = st.slider("Rotate rectangular [Degree]", min_value=0, max_value=270, value=0, step=90)
        # cRotateFree = st.checkbox(label="Rotate in free degrees", value=False)
        # angle = st.slider("Rotate freely [Degree]", min_value=-180, max_value=180, value=0, step=1)
        im_controls.show_image_processing_controls()


# check if installed languages are available
# REGFACTOR! variable installed_languges doesnt used anywhere
installed_languages = tesseract.check_installed_languages(language_short)

# two column layout for image preprocessing options and image preview
col1, col2 = st.columns(spec=[2, 3], gap="large")
image = None

with col1:
    image = up_controls.show_upload_image_controls()

with col2:
    st.subheader("Image Preview")
    if image is not None:
        # preview image
        st.image(image, caption="Uploaded Image Preview", use_column_width=True)

        # add streamlit button
        if st.button("Extract Text"):
            # streamlit spinner
            with st.spinner("Extracting Text..."):
                try:
                 
                    text = tesseract.extract_text_from_image(image, language_short, psm, timeout)
                    print(text)
                    
                    if text:
                        # TODO: move this to the whole page again
                        # TODO: try Ace Editor for text area instead
                        # add streamlit text area
                        st.text_area("Extracted Text", value=text, height=500, key="extracted_text")
                        
                        # add streamlit download button for extracted text
                        st.download_button("Download Extracted Text", data=text.encode("utf-8"), file_name="extract.txt", mime="text/plain", key="download_button")
                    else:
                        st.warning("No text was extracted. Please try again with a different image or settings.")
                        st.stop()
                except Exception as e:
                    st.error("An unexpected error occurred.")
                    st.error(f"Error Message: {str(e)}")
                    st.stop()



