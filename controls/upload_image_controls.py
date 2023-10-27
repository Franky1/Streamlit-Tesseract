import streamlit as st
from pdf2image.exceptions import (PDFInfoNotInstalledError, PDFPageCountError,
                                PDFPopplerTimeoutError, PDFSyntaxError)
import helpers.pdfimage as pdfimage
import numpy as np
import helpers.opencv as opencv
import helpers.constants as constants

def show_upload_image_controls():
    # Load the image processing configuration from session state
    config = st.session_state.image_processing_config
    
    # Extract data from the configuration dictionary into separate variables
    cGrayscale = config['Grayscale']
    cDenoising = config['Denoising']
    cDenoisingStrength = config['DenoisingStrength']
    cThresholding = config['Thresholding']
    cThresholdLevel = config['ThresholdLevel']
    cRotate90 = config['Rotate90']
    angle90 = config['Angle90']
    cRotateFree = config['RotateFree']
    angle = config['Angle']

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
                    image = opencv.rotate_scipy(image, angle=angle, reshape=True)
                # TODO: add crop functions here
                # if cCrop:
                #     pass
                image = opencv.convert_to_rgb(image)
                return image
            except Exception as e:
                st.error(f"Exception during Image Preprocessing (Probably you selected Threshold on a color image?): {e}")
                st.stop()

    
