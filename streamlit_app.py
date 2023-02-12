import shutil

import cv2
import numpy as np
import pytesseract
import streamlit as st

import constants

# change path if required / for mac os just comment this line
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# search for tesseract binary in path
@st.cache_resource
def find_tesseract_binary():
    return shutil.which("tesseract")

# set tesseract path
@st.cache_resource
def set_tesseract_path(path):
    pytesseract.pytesseract.tesseract_cmd = path

# make numpy array from image
@st.cache_data
def load_image(image_file):
    # img = cv2.imread(image_file)
    # return np.array(img)
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, 1)

# opencv preprocessing grayscale
@st.cache_data
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# opencv preprocessing noise removal
@st.cache_data
def remove_noise(img):
    return cv2.medianBlur(img, 5)

# opencv preprocessing denoising
@st.cache_data
def denoising(img, strength=10):
    if len(img.shape) == 3:
        noiseless_image = cv2.fastNlMeansDenoisingColored(img, None, strength, strength, 7, 21)
    else:
        noiseless_image = cv2.fastNlMeansDenoising(img, None, strength, 7, 21)
    return noiseless_image

# opencv preprocessing thresholding
@st.cache_data
def thresholding(img, threshold=128):
    # FIXME: add handling for color images
    # Convert the image to grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply the threshold
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return img

    # # check if image is grayscale
    # if len(img.shape) == 2:
    #     return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # # else:
    # # Convert the image to HSV
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # # Define a range of colors to threshold
    # lower_color = np.array([0, 50, 50])
    # upper_color = np.array([10, 255, 255])

    # # Threshold the image to get only the desired colors
    # mask = cv2.inRange(hsv, lower_color, upper_color)
    # thresholded_img = cv2.bitwise_and(img, img, mask=mask)
    # return thresholded_img

# opencv preprocessing dilation
@st.cache_data
def dilate(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)

# opencv preprocessing erosion
@st.cache_data
def erode(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(img, kernel, iterations=1)

# opencv preprocessing opening
@st.cache_data
def opening(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# opencv convert BGR to RGB
@st.cache_data
def convert_to_rgb(img):
    # check if image is color
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        return img

# streamlit config
st.set_page_config(page_title="Tesseract OCR - Optical Character Recognition", page_icon="📝", layout="wide", initial_sidebar_state="expanded")

# add streamlit title
st.title("Tesseract OCR - Optical Character Recognition 📝")

# add streamlit subheader
st.markdown(f'''**Tesseract OCR** - Optical Character Recognition using Tesseract, OpenCV and Streamlit.<br>
This is a simple OCR demo app that can be used to extract text from images. Supported languages see below.
# {constants.flag_string}
''', unsafe_allow_html=True)

with st.sidebar:
    st.header("Tesseract OCR Settings")
    language = st.selectbox(label="Select Language", options=list(constants.languages.values()), index=0)
    language_short = list(constants.languages.keys())[list(constants.languages.values()).index(language)]
    oem = st.selectbox(label="OCR Engine mode", options=constants.oem, index=3)
    psm = st.selectbox(label="Page segmentation mode", options=constants.psm, index=3)
    timeout = st.slider(label="Tesseract OCR timeout [sec]", min_value=1, max_value=60, value=10, step=1)
    st.markdown('---')
    st.header("Image Preprocessing")
    st.write("Check the boxes below to apply preprocessing to the image before extracting text with Tesseract OCR. Preview the image after each preprocessing step.")
    cGrayscale = st.checkbox(label="Grayscale", value=True)
    cNoise = st.checkbox(label="Noise Removal", value=False)
    cDenoising = st.checkbox(label="Denoising", value=False)
    cDenoisingStrength = st.slider(label="Denoising Strength", min_value=1, max_value=40, value=10, step=1)
    cThresholding = st.checkbox(label="Thresholding", value=False)
    cThresholdLevel = st.slider(label="Threshold", min_value=0, max_value=255, value=128, step=1)
    cDilation = st.checkbox(label="Dilation", value=False)
    cErosion = st.checkbox(label="Erosion", value=False)
    cOpening = st.checkbox(label="Opening", value=False)
    st.markdown('''---
# About
## GitHub
<https://github.com/Franky1/Streamlit-Tesseract>
''', unsafe_allow_html=True)

custom_oem_psm_config = rf'--oem {oem} --psm {psm}'

st.write(f'Tesseract path: {find_tesseract_binary()}')

# check if tesseract is installed
try:
    version = pytesseract.get_tesseract_version()
except pytesseract.TesseractNotFoundError:
    st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
    st.stop()
except Exception as e:
    st.error(f"Unexpected Exception: {e}")
    st.stop()
else:
    if version:
        st.success(f"Tesseract Version {version} is installed.")
    else:
        st.error("Tesseract is not installed. Please install Tesseract.")
        st.stop()

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
    st.write(f"Installed Languages: {installed_languages}")
    if language_short not in installed_languages:
        st.error(f'Selected language "{language}" is not installed. Please install language data.')
        st.stop()

# upload image
st.subheader("Upload Image")
uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg", "bmp", "tif", "tiff"])

if uploaded_file is not None:
    try:
        # TODO: add more fine tuning options for image preprocessing
        # convert uploaded file to numpy array
        image = load_image(uploaded_file)
        if cGrayscale:
            image = grayscale(image)
        if cNoise:
            image = remove_noise(image)
        if cDenoising:
            image = denoising(image, strength=cDenoisingStrength)
        if cThresholding:
            image = thresholding(image, threshold=cThresholdLevel)
        if cDilation:
            image = dilate(image)
        if cErosion:
            image = erode(image)
        if cOpening:
            image = opening(image)
        # always convert to RGB
        image = convert_to_rgb(image)
    except Exception as e:
        st.error(f"Exception during Image Preprocessing (Probably you selected Threshold on a color image?): {e}")
        st.stop()

    # preview image
    st.image(image, caption="Uploaded Image", width=500)

    # add streamlit button
    if st.button("Extract Text"):
        # streamlit spinner
        with st.spinner("Extracting Text..."):
            try:
                text = pytesseract.image_to_string(image=image,
                                            lang=language_short,
                                            output_type=pytesseract.Output.STRING,
                                            config=custom_oem_psm_config,
                                            timeout=timeout)
            except pytesseract.TesseractError:
                st.error("TesseractError: Tesseract reported an error during text extraction.")
                st.stop()
            except pytesseract.TesseractNotFoundError:
                st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract..")
                st.stop()
            except RuntimeError:
                st.error("RuntimeError: Tesseract timed out during text extraction.")
                st.stop()
            except Exception as e:
                st.error(f"Unexpected Exception: {e}")
                st.stop()
            else:
                # add streamlit subheader
                st.subheader("Extracted Text")
                if text:
                    # add streamlit text area
                    st.text_area(label="Extracted Text", value=text, height=500)
                    # add streamlit download button for extracted text
                    st.download_button(label="Download Extracted Text", data=text.encode("utf-8"), file_name="extract.txt", mime="text/plain")
                else:
                    st.warning("No text was extracted.")
