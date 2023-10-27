import shutil
import streamlit as st
import pytesseract
import yaml
import helpers.constants as constants

@st.cache_data
def load_config():
    with open('configs/tesseract_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config


# Search for Tesseract binary in path
@st.cache_resource
def find_tesseract_binary() -> str:
    return shutil.which("tesseract")

tesseract_cmd = find_tesseract_binary()
if not tesseract_cmd:
    st.error("Tesseract binary not found in PATH. Please install Tesseract.")
    st.stop()
else:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

# Get Tesseract version
@st.cache_resource
def get_tesseract_version():
    try:
        version = pytesseract.get_tesseract_version()
        if not version:
            st.error("Tesseract is not installed or version could not be determined. Please install Tesseract.")
            st.stop()
        return version
    except pytesseract.TesseractNotFoundError:
        st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
        st.stop()
    except Exception as e:
        st.error("Unexpected Exception")
        st.error(f"Error Message: {e}")
        st.stop()

# Create custom OEM and PSM config string
@st.cache_data
def get_tesseract_config(oem_index: int, psm_index: int) -> str:
    return f'--oem {oem_index} --psm {psm_index}'


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


def check_installed_languages(language_short):
    try:
        installed_languages = pytesseract.get_languages(config='')
        if language_short not in installed_languages:
            st.error(f'Selected language "{language_short}" is not installed. Please install language data.')
            st.stop()
        return installed_languages
    except pytesseract.TesseractError as e:
        st.error("TesseractError: Tesseract reported an error during language data extraction.")
        st.exception(e)
        st.stop()
    except pytesseract.TesseractNotFoundError:
        st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
        st.stop()
    except Exception as e:
        st.error("Unexpected Exception")
        st.exception(e)
        st.stop()


def extract_text_from_image(image, language_short, psm, timeout):
    # get index of selected oem parameter
    # FIXME: OEM option does not work in tesseract 4.1.1
    # oem_index = constants.oem.index(oem)
    oem_index = 3
    # get index of selected psm parameter
    psm_index = constants.psm.index(psm)

    custom_oem_psm_config = get_tesseract_config(oem_index=oem_index, psm_index=psm_index)

    try:
        text = pytesseract.image_to_string(image=image, lang=language_short, config=custom_oem_psm_config, timeout=timeout)
        return text
    except pytesseract.TesseractError as e:
        st.error("TesseractError: Tesseract reported an error during text extraction.")
        st.exception(e)
        st.stop()
    except pytesseract.TesseractNotFoundError:
        st.error("TesseractNotFoundError: Tesseract is not installed. Please install Tesseract.")
        st.stop()
    except RuntimeError as e:
        st.error("RuntimeError: Tesseract timed out during text extraction.")
        st.exception(e)
        st.stop()
    except Exception as e:
        st.error("Unexpected Exception")
        st.exception(e)
        st.stop()
