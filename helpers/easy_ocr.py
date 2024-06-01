'''
This module is curently NOT used in the main app.
It is a helper module to test the easyocr library with streamlit in the future.
'''
import cv2
import easyocr
import numpy as np
import pandas as pd
import requests
import streamlit as st
import torch

# st.set_page_config(page_title="EasyOCR", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")


@st.cache_resource
def download_sample_image(url: str) -> np.ndarray:
    """Download sample image from url with requests
    params: url: url to download
    """
    response = requests.get(url)
    content = response.content
    array = np.frombuffer(content, dtype=np.uint8)
    cv2_bgr = cv2.imdecode(buf=array, flags=cv2.COLOR_RGB2BGR)
    cv2_rgb = cv2.cvtColor(cv2_bgr, cv2.COLOR_BGR2RGB)
    return cv2_rgb


@st.cache_resource
def easyocr_reader(lang: str) -> easyocr.easyocr.Reader:
    """Create an easyocr reader object
    params: lang: language to use
    """
    if torch.cuda.is_available():
        return easyocr.Reader([lang], gpu=True)
    else:
        return easyocr.Reader([lang], gpu=False)


@st.cache_data
def easyocr_read(img: np.ndarray, _reader: easyocr.easyocr.Reader, detail: int = 0):
    """Read text from image using easyocr
    params: img: image to read
            reader: easyocr reader object
            detail: 0 for text only, 1 for verbose
    """
    return _reader.readtext(img, detail=detail)


@st.cache_data
def easyocr_get_dataframe_from_result(result: list) -> pd.DataFrame:
    """Get dataframe from easyocr verbose result
    params: result: easyocr verbose result with detail=1
    """
    return pd.DataFrame(result, columns=["box", "text", "confidence"])


@st.cache_data
def easyocr_get_text_list_from_result(result: list) -> list:
    """Get list of text from easyocr verbose result
    params: result: easyocr verbose result with detail=1
    """
    return [text for box, text, conf in result]


@st.cache_data
def easyocr_get_text_from_result(result: list) -> str:
    """Get text from easyocr verbose result
    params: result: easyocr verbose result with detail=1
    """
    return "\r".join([text for box, text, conf in result])


# Test the functions above with streamlit and easyocr
if __name__ == "__main__":
    st.title("EasyOCR")
    reader = easyocr_reader(lang="en")
    sample_image_url = (
        "https://raw.githubusercontent.com/JaidedAI/EasyOCR/master/examples/english.png"
    )
    # load sample image from url to numpy array with cv2
    sample_image = download_sample_image(sample_image_url)
    st.image(sample_image, width=800)
    # read text from image with easyocr
    result = easyocr_read(sample_image, reader, detail=1)
    # get dataframe from result
    df = easyocr_get_dataframe_from_result(result)
    with st.expander("Details of detected text"):
        # show dataframe
        st.dataframe(df, width=1600)
    # get list of text from result
    text = easyocr_get_text_from_result(result)
    # show text list in editor
    st.text_area(label="Extracted Text", value=text, height=600)
