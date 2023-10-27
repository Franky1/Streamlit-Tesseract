import streamlit as st
import helpers.constants as constants
import helpers.tesseract as tesseract

def show_controls():
    st.success(f"Tesseract Version **{tesseract.get_tesseract_version()}** is installed.")
    st.header("Tesseract OCR Settings")
    language = st.selectbox(label="Select Language", options=list(constants.languages_sorted.values()), index=constants.default_language_index)
    language_short = list(constants.languages_sorted.keys())[list(constants.languages_sorted.values()).index(language)]
    # FIXME: OEM option does not work in tesseract 4.1.1
    # oem = st.selectbox(label="OCR Engine mode (not working)", options=constants.oem, index=3, disabled=True)
    psm = st.selectbox(label="Page segmentation mode", options=constants.psm, index=3)
    timeout = st.slider(label="Tesseract OCR timeout [sec]", min_value=1, max_value=60, value=20, step=1)
    st.write("Tesseract Configuration:")
    st.write(st.session_state['tesseract_config'])
    return language, language_short, psm, timeout
