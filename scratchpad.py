import streamlit as st

with st.sidebar:
    st.markdown('''---
# About
#### Binary libraries used
- `tesseract-ocr`
    - The Tesseract OCR Engine
- `tesseract-ocr-<language>`
    - Language data for each language
#### Python libraries used
- `pytesseract`
## GitHub
<https://github.com/Franky1/Streamlit-Tesseract>
''', unsafe_allow_html=True)
