import numpy as np
import pytesseract
import streamlit as st
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                PDFPopplerTimeoutError, PDFSyntaxError)

import helpers.constants as constants
import helpers.opencv as opencv
import helpers.pdfimage as pdfimage
import helpers.tesseract as tesseract

pytesseract.pytesseract.tesseract_cmd = None

# set tesseract path
@st.cache_resource
def set_tesseract_path(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

# streamlit config
st.set_page_config(page_title="Tesseract OCR", page_icon="📝", layout="wide", initial_sidebar_state="expanded")

# apply custom css
with open('helpers/style.css') as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# add streamlit title
st.title("Tesseract OCR - Optical Character Recognition 📝")

# add streamlit markdown text
# st.markdown('''**Tesseract OCR** - Optical Character Recognition using Tesseract, OpenCV and Streamlit.<br>
# This is a simple OCR demo app that can be used to extract text from images. Supported languages see below.
# ''', unsafe_allow_html=True)
st.markdown(f'''# {constants.flag_string}''')

# set tesseract binary path
pytesseract.pytesseract.tesseract_cmd = tesseract.find_tesseract_binary()
if not pytesseract.pytesseract.tesseract_cmd:
    st.error("Tesseract binary not found in PATH. Please install Tesseract.")
    st.stop()

# check if tesseract is installed
try:
    tesseract_version = pytesseract.get_tesseract_version()
except pytesseract.TesseractNotFoundError:
    st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
    st.stop()
except Exception as e:
    st.error(f"Unexpected Exception: {e}")
    st.stop()
else:
    if not tesseract_version:
        st.error("Tesseract is not installed. Please install Tesseract.")
        st.stop()

with st.sidebar:
    st.success(f"Tesseract Version **{tesseract_version}** is installed.")
    st.header("Tesseract OCR Settings")
    language = st.selectbox(label="Select Language", options=list(constants.languages_sorted.values()), index=constants.default_language_index)
    language_short = list(constants.languages_sorted.keys())[list(constants.languages_sorted.values()).index(language)]
    # FIXME: OEM option does not work in tesseract 4.1.1
    # oem = st.selectbox(label="OCR Engine mode (not working)", options=constants.oem, index=3, disabled=True)
    psm = st.selectbox(label="Page segmentation mode", options=constants.psm, index=3)
    timeout = st.slider(label="Tesseract OCR timeout [sec]", min_value=1, max_value=60, value=20, step=1)
    st.markdown('---')
    st.header("Image Preprocessing")
    st.write("Check the boxes below to apply preprocessing to the image.")
    cGrayscale = st.checkbox(label="Grayscale", value=True)
    cDenoising = st.checkbox(label="Denoising", value=False)
    cDenoisingStrength = st.slider(label="Denoising Strength", min_value=1, max_value=40, value=10, step=1)
    cThresholding = st.checkbox(label="Thresholding", value=False)
    cThresholdLevel = st.slider(label="Threshold Level", min_value=0, max_value=255, value=128, step=1)
    cRotate90 = st.checkbox(label="Rotate in 90° steps", value=False)
    angle90 = st.slider("Rotate rectangular [Degree]", min_value=0, max_value=270, value=0, step=90)
    cRotateFree = st.checkbox(label="Rotate in free degrees", value=False)
    angle = st.slider("Rotate freely [Degree]", min_value=-180, max_value=180, value=0, step=1)
    st.markdown('''---
# About
## GitHub
<https://github.com/Franky1/Streamlit-Tesseract>
''', unsafe_allow_html=True)

# get index of selected oem parameter
# FIXME: OEM option does not work in tesseract 4.1.1
# oem_index = constants.oem.index(oem)
oem_index = 3
# get index of selected psm parameter
psm_index = constants.psm.index(psm)
# create custom oem and psm config string
custom_oem_psm_config = tesseract.get_tesseract_config(oem_index=oem_index, psm_index=psm_index)

# check if installed languages are available
installed_languages = list()
try:
    installed_languages = pytesseract.get_languages(config='')
except pytesseract.TesseractError:
    st.error("TesseractError: Tesseract reported an error during language data extraction.")
    st.stop()
except pytesseract.TesseractNotFoundError:
    st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract..")
    st.stop()
except Exception as e:
    st.error(f"Unexpected Exception: {e}")
    st.stop()
else:
    if language_short not in installed_languages:
        st.error(f'Selected language "{language}" is not installed. Please install language data.')
        st.stop()

# two column layout for image preprocessing options and image preview
col1, col2 = st.columns(spec=[2, 3], gap="large")
image = None

with col1:
    # upload image
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "bmp", "tif", "tiff", "pdf"])

    if uploaded_file is not None:
        # check if uploaded file is pdf
        if uploaded_file.name.lower().endswith(".pdf"):
            try:
                page = st.number_input("Select Page of PDF", min_value=1, max_value=100, value=1, step=1)
                image = pdfimage.pdftoimage(uploaded_file, page=page)
                if image is not None:
                    image = np.array(image) # convert pillow image to numpy array
                    image = pdfimage.img2opencv2(image)
                else:
                    st.error("Invalid PDF page selected.")
                    st.stop()
            except PDFInfoNotInstalledError as e:
                st.error("PDFInfoNotInstalledError: PDFInfo is not installed?")
                st.stop()
            except PDFPageCountError as e:
                st.error("PDFPageCountError: Could not determine number of pages in PDF.")
                st.stop()
            except PDFSyntaxError as e:
                st.error("PDFSyntaxError: PDF is damaged/corrupted?")
                st.stop()
            except PDFPopplerTimeoutError as e:
                st.error("PDFPopplerTimeoutError: PDF conversion timed out.")
                st.stop()
            except Exception as e:
                st.error("Unknwon Exception during PDF conversion")
                st.error(f"Error Message: {e}")
                st.stop()
        # else uploaded file is image file
        else:
            try:
                # convert uploaded file to numpy array
                image = opencv.load_image(uploaded_file)
            except Exception as e:
                st.error("Exception during Image Conversion")
                st.error(f"Error Message: {e}")
                st.stop()
        try:
            if cGrayscale:
                image = opencv.grayscale(image)
            if cDenoising:
                image = opencv.denoising(image, strength=cDenoisingStrength)
            if cThresholding:
                image = opencv.thresholding(image, threshold=cThresholdLevel)
            if cRotate90:
                # convert angle to opencv2 enum
                angle90 = constants.angles.get(angle90, None)
                image = opencv.rotate90(image, rotate=angle90)
            if cRotateFree:
                image = opencv.rotate(image, angle=angle)
            # TODO: add crop functions here
            # if cCrop:
            #     pass
            image = opencv.convert_to_rgb(image)
        except Exception as e:
            st.error(f"Exception during Image Preprocessing (Probably you selected Threshold on a color image?): {e}")
            st.stop()

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
                    # st.info(f"Tesseract configuration: {custom_oem_psm_config}")
                    text = pytesseract.image_to_string(image=image,
                                                lang=language_short,
                                                output_type=pytesseract.Output.STRING,
                                                config=custom_oem_psm_config,
                                                timeout=timeout)
                except pytesseract.TesseractError as e:
                    st.error("TesseractError: Tesseract reported an error during text extraction.")
                    st.error(f"Error Message: {e}")
                    st.stop()
                except pytesseract.TesseractNotFoundError:
                    st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract..")
                    st.stop()
                except RuntimeError:
                    st.error("RuntimeError: Tesseract timed out during text extraction.")
                    st.stop()
                except Exception as e:
                    st.error("Unexpected Exception")
                    st.error(f"Error Message: {e}")
                    st.stop()
                else:
                    # add streamlit subheader
                    # st.subheader("Extracted Text")
                    if text:
                        # add streamlit text area
                        st.text_area(label="Extracted Text", value=text, height=500)
                        # add streamlit download button for extracted text
                        st.download_button(label="Download Extracted Text", data=text.encode("utf-8"), file_name="extract.txt", mime="text/plain")
                    else:
                        st.warning("No text was extracted.")
