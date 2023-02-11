import streamlit as st
import pytesseract

import constants

# change path if required / for mac os just comment this line
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# streamlit config
st.set_page_config(page_title="OCR - Optical Character Recognition", page_icon="📝", layout="centered", initial_sidebar_state="expanded")

# add streamlit title
st.title("OCR - Optical Character Recognition")

# add streamlit subheader
st.subheader("Optical Character Recognition using Tesseract")
# show all supported languages
st.write(f"Supported Languages: {constants.flag_string}")

# add streamlit selectbox
language = st.selectbox(label="Select Language", options=list(constants.languages.values()), index=0)
language_short = list(constants.languages.keys())[list(constants.languages.values()).index(language)]
