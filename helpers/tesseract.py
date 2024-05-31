import shutil

import pytesseract
import streamlit as st


pytesseract.pytesseract.tesseract_cmd = None

oem = [
    "Original Tesseract only",
    "Neural nets LSTM only  ",
    "Tesseract + LSTM       ",
    "Default                ",
]

psm = [
    "Orientation and script detection (OSD) only.                      ",
    "Automatic page segmentation with OSD.                             ",
    "Automatic page segmentation, but no OSD, or OCR. (not implemented)",
    "Fully automatic page segmentation, but no OSD. (Default)          ",
    "Assume a single column of text of variable sizes.                 ",
    "Assume a single uniform block of vertically aligned text.         ",
    "Assume a single uniform block of text.                            ",
    "Treat the image as a single text line.                            ",
    "Treat the image as a single word.                                 ",
    "Treat the image as a single word in a circle.                     ",
    "Treat the image as a single character.                            ",
    "Sparse text. Find as much text as possible in no particular order.",
    "Sparse text with OSD.                                             ",
    "Raw line. Treat the image as a single text line.                  ",
]


# search for tesseract binary in path
@st.cache_resource(show_spinner=False)
def find_tesseract_binary() -> str:
    return shutil.which("tesseract")


# set tesseract path
@st.cache_resource(show_spinner=False)
def set_tesseract_path(tesseract_path: str):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


@st.cache_resource(show_spinner=False)
def set_tesseract_binary():
    set_tesseract_path(find_tesseract_binary())


@st.cache_resource(show_spinner=False)
def get_tesseract_version() -> tuple[str, str]:
    tesseract_version, error = None, None
    try:
        tesseract_version = pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        error = "TesseractNotFoundError: Tesseract is not installed. Please install Tesseract."
    except Exception as e:
        error = str(e)
    return (tesseract_version, error)


@st.cache_resource(show_spinner=False)
def get_tesseract_languages() -> tuple[list[str], str]:
    installed_languages, error = list(), None
    try:
        installed_languages = pytesseract.get_languages(config="")
    except pytesseract.TesseractError:
        error = "TesseractError: Tesseract reported an error during language data extraction."
    except pytesseract.TesseractNotFoundError:
        error = "TesseractNotFoundError: Tesseract is not installed. Please install Tesseract."
    except Exception as e:
        error = str(e)
    return (installed_languages, error)


# create custom oem and psm config string
@st.cache_resource(show_spinner=False)
def get_tesseract_config(oem_index: int, psm_index: int) -> str:
    custom_oem_psm_config = f"--oem {oem_index} --psm {psm_index}"
    return custom_oem_psm_config


@st.cache_data(show_spinner=False)
def image_to_string(image: bytes,
                    language_short : str,
                    config : str,
                    timeout : int
                    ) -> tuple[str, str]:
    text, error = None, None
    try:
        text = pytesseract.image_to_string(
                        image=image,
                        lang=language_short,
                        output_type=pytesseract.Output.STRING,
                        config=config,
                        timeout=timeout
                    )
    except pytesseract.TesseractError:
        error = "TesseractError: Tesseract reported an error during text extraction."
    except pytesseract.TesseractNotFoundError:
        error = "TesseractNotFoundError: Tesseract is not installed. Please install Tesseract."
    except RuntimeError:
        error = "RuntimeError: Tesseract timed out during text extraction."
    except Exception as e:
        error = str(e)

    return (text, error)
