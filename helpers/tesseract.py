import shutil
import streamlit as st
import pytesseract


pytesseract.pytesseract.tesseract_cmd = None

# set tesseract path
@st.cache_resource
def set_tesseract_path(tesseract_path: str):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Search for Tesseract binary in path
@st.cache_resource
def find_tesseract_binary() -> str:
    return shutil.which("tesseract")

# Get Tesseract version
@st.cache_resource
def get_tesseract_version():
    # check if tesseract is installed
    try:
        tesseract_version = pytesseract.get_tesseract_version()
        return tesseract_version
    except pytesseract.TesseractNotFoundError:
        st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
        st.stop()
    except Exception as e:
        st.error("Unexpected Exception")
        st.error(f"Error Message: {e}")
        st.stop()
    else:
        if not tesseract_version:
            st.error("Tesseract is not installed. Please install Tesseract.")
            st.stop()




# Create custom OEM and PSM config string
@st.cache_data
def get_tesseract_config(oem_index: int, psm_index: int) -> str:
    custom_oem_psm_config = f'--oem {oem_index} --psm {psm_index}'
    return custom_oem_psm_config


# Set Tesseract binary path and check installation
@st.cache_data
def set_tesseract_cmd_and_check_installation() -> str:
    tesseract_cmd = find_tesseract_binary()
    if not tesseract_cmd:
        st.error("Tesseract binary not found in PATH. Please install Tesseract.")
        return None
    try:
        tesseract_version = pytesseract.get_tesseract_version()
        if not tesseract_version:
            st.error("Tesseract is not installed. Please install Tesseract.")
            return None
    except pytesseract.TesseractNotFoundError:
        st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
        return None
    except Exception as e:
        st.error("Unexpected Exception")
        st.error(f"Error Message: {e}")
        return None
    return tesseract_cmd

@st.cache_data
def check_installed_languages(language_short, language):
    try:
        installed_languages = pytesseract.get_languages(config='')
    except pytesseract.TesseractError:
        st.error("TesseractError: Tesseract reported an error during language data extraction.")
        st.stop()
    except pytesseract.TesseractNotFoundError:
        st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
        st.stop()
    except Exception as e:
        st.error("Unexpected Exception")
        st.error(f"Error Message: {e}")
        st.stop()
    else:
        if language_short not in installed_languages:
            st.error(f'Selected language "{language}" is not installed. Please install language data.')
            st.stop()
        return installed_languages


def extract_text_from_image(image, language_short, custom_oem_psm_config, timeout):
    """
    This function attempts to extract text from an image using Tesseract OCR.
    It takes an image, a language code, a custom OEM and PSM config string, and a timeout value as input.
    If any error occurs during the text extraction, an appropriate error message is displayed and the Streamlit app is stopped.

    :param image: Image to extract text from
    :param language_short: Short code for the language used in the image
    :param custom_oem_psm_config: Custom configuration string for OEM and PSM
    :param timeout: Timeout value for Tesseract OCR
    :return: Extracted text if successful, None otherwise
    """
    try:
        text = pytesseract.image_to_string(image=image,
                                           lang=language_short,
                                           output_type=pytesseract.Output.STRING,
                                           config=custom_oem_psm_config,
                                           timeout=timeout)
        return text
    except pytesseract.TesseractError as e:
        st.error("TesseractError: Tesseract reported an error during text extraction.")
        st.error(f"Error Message: {e}")
        st.stop()
    except pytesseract.TesseractNotFoundError:
        st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
        st.stop()
    except RuntimeError:
        st.error("RuntimeError: Tesseract timed out during text extraction.")
        st.stop()
    except Exception as e:
        st.error("Unexpected Exception")
        st.error(f"Error Message: {e}")
        st.stop()
    return None

