import shutil
import streamlit as st


# search for tesseract binary in path
@st.cache_resource
def find_tesseract_binary() -> str:
    return shutil.which("tesseract")


# create custom oem and psm config string
@st.cache_data
def get_tesseract_config(oem_index: int, psm_index: int) -> str:
    custom_oem_psm_config = f'--oem {oem_index} --psm {psm_index}'
    return custom_oem_psm_config
