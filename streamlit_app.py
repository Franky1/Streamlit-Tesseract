import streamlit as st

import helpers.constants as constants
import helpers.opencv as opencv
import helpers.pdfimage as pdfimage
import helpers.tesseract as tesseract
# import helpers.easy_ocr as easy_ocr

language_options_list = list(constants.languages_sorted.values())


def init_tesseract():
    tess_version = None
    # set tesseract binary path
    tesseract.set_tesseract_binary()
    if not tesseract.find_tesseract_binary():
        st.error("Tesseract binary not found in PATH. Please install Tesseract.")
        st.stop()
    # check if tesseract is installed
    tess_version, error = tesseract.get_tesseract_version()
    if error:
        st.error(error)
        st.stop()
    elif not tess_version:
        st.error("Tesseract is not installed. Please install Tesseract.")
        st.stop()
    return tess_version


def reset_sidebar_values():
    '''Reset all sidebar values of buttons/sliders to default values.
    '''
    st.session_state.psm = tesseract.psm[3]
    st.session_state.timeout = 20
    st.session_state.cGrayscale = True
    st.session_state.cDenoising = False
    st.session_state.cDenoisingStrength = 10
    st.session_state.cThresholding = False
    st.session_state.cThresholdLevel = 128
    st.session_state.cRotate90 = False
    st.session_state.angle90 = 0
    st.session_state.cRotateFree = False
    st.session_state.angle = 0


# init tesseract
tesseract_version = init_tesseract()

# streamlit config
st.set_page_config(
    page_title="Tesseract OCR",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# apply custom css
with open(file="helpers/style.css", mode='r', encoding='utf-8') as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

col_title_1, col_title_2 = st.columns(spec=2, gap="large")

# title and flag columns
with col_title_1:
    # add streamlit title
    st.title("Tesseract OCR :mag:")
with col_title_2:
    # add streamlit markdown
    pass
st.markdown("---")

with st.sidebar:
    st.success(f"Tesseract Version **{tesseract_version}** is installed.")
    st.header("Tesseract OCR Settings")
    st.button('Reset OCR parameters below to default values', on_click=reset_sidebar_values)
    # st.markdown("---")
    # FIXME: OEM option does not work in tesseract 4.1.1
    # oem = st.selectbox(label="OCR Engine mode (not working)", options=constants.oem, index=3, disabled=True)
    psm = st.selectbox(label="Page segmentation mode", options=tesseract.psm, index=3, key="psm")
    timeout = st.slider(label="Tesseract OCR timeout [sec]", min_value=1, max_value=60, value=20, step=1, key="timeout")
    st.markdown("---")
    st.header("Image Preprocessing")
    st.write("Check the boxes below to apply preprocessing to the image.")
    cGrayscale = st.checkbox(label="Grayscale", value=True, key="cGrayscale")
    cDenoising = st.checkbox(label="Denoising", value=False, key="cDenoising")
    cDenoisingStrength = st.slider(label="Denoising Strength", min_value=1, max_value=40, value=10, step=1, key="cDenoisingStrength")
    cThresholding = st.checkbox(label="Thresholding", value=False, key="cThresholding")
    cThresholdLevel = st.slider(label="Threshold Level", min_value=0, max_value=255, value=128, step=1, key="cThresholdLevel")
    cRotate90 = st.checkbox(label="Rotate in 90° steps", value=False, key="cRotate90")
    angle90 = st.slider("Rotate rectangular [Degree]", min_value=0, max_value=270, value=0, step=90, key="angle90")
    cRotateFree = st.checkbox(label="Rotate in free degrees", value=False, key="cRotateFree")
    angle = st.slider("Rotate freely [Degree]", min_value=-180, max_value=180, value=0, step=1, key="angle")
    st.markdown(
        """---
# About
## GitHub
<https://github.com/Franky1/Streamlit-Tesseract>
""",
        unsafe_allow_html=True,
    )

# get index of selected oem parameter
# FIXME: OEM option does not work in tesseract 4.1.1
# oem_index = tesseract.oem.index(oem)
oem_index = 3
# get index of selected psm parameter
psm_index = tesseract.psm.index(psm)
# create custom oem and psm config string
custom_oem_psm_config = tesseract.get_tesseract_config(oem_index=oem_index, psm_index=psm_index)

# check if installed languages are available
installed_languages, error = tesseract.get_tesseract_languages()
if error:
    st.error(error)
    st.stop()

raw_image, image = None, None

col_upload_1, col_upload_2 = st.columns(spec=2, gap="large")
with col_upload_2:
    st.subheader("Select Language :globe_with_meridians:")
    language = st.selectbox(
        label="Select Language",
        options=language_options_list,
        index=constants.default_language_index,
    )
    language_short = list(constants.languages_sorted.keys())[list(constants.languages_sorted.values()).index(language)]
    if language_short not in installed_languages:
        st.error(f'Selected language "{language}" is not installed. Please install language data.')
        st.stop()
    # add 4 columns with a slider each for cropping the image from the top, bottom, left, and right
    st.subheader("Image Cropping :scissors:")
    cCrop = st.checkbox("Crop Image", value=False)
    with st.expander("Cropping by 0-40 percent from each side", expanded=cCrop):
        col_left, col_top, col_right, col_bottom = st.columns(spec=4, gap="small")
        with col_left:
            crop_left = st.slider("Left %", min_value=0, max_value=40, step=1, key="crop_left")
        with col_top:
            crop_top = st.slider("Top %", min_value=0, max_value=40, step=1, key="crop_top")
        with col_right:
            crop_right = st.slider("Right %", min_value=0, max_value=40, step=1, key="crop_right")
        with col_bottom:
            crop_bottom = st.slider("Bottom %", min_value=0, max_value=40, step=1, key="crop_bottom")

with col_upload_1:
    st.markdown(f"""# {constants.flag_string}""")
    # upload image
    st.subheader("Upload Image :arrow_up:")
    uploaded_file = st.file_uploader(
        "Upload Image or PDF", type=["png", "jpg", "jpeg", "bmp", "tif", "tiff", "pdf"]
    )

    if uploaded_file is not None:
        # check if uploaded file is pdf
        if uploaded_file.name.lower().endswith(".pdf"):
            page = st.number_input("Select Page of PDF", min_value=1, max_value=100, value=1, step=1)
            raw_image, error = pdfimage.pdftoimage(pdf_file=uploaded_file, page=page)
            if error:
                st.error(error)
                st.stop()
            elif raw_image is None:
                st.error("No image was extracted from PDF.")
                st.stop()
        # else uploaded file is image file
        else:
            try:
                # convert uploaded file to numpy array
                raw_image = opencv.load_image(uploaded_file)
            except Exception as e:
                st.error("Exception during Image Conversion")
                st.error(f"Error Message: {e}")
                st.stop()
        try:
            with st.spinner("Preprocessing Image..."):
                image = raw_image.copy()
                # apply image preprocessing
                if cGrayscale:
                    image = opencv.grayscale(img=image)
                if cDenoising:
                    image = opencv.denoising(img=image, strength=cDenoisingStrength)
                if cThresholding:
                    image = opencv.thresholding(img=image, threshold=cThresholdLevel)
                if cRotate90:
                    angle90 = opencv.angles.get(angle90, None)  # convert angle to opencv2 enum
                    image = opencv.rotate90(img=image, rotate=angle90)
                if cRotateFree:
                    image = opencv.rotate_scipy(img=image, angle=angle, reshape=True)
                if cCrop:
                    image = opencv.crop(img=image, left=crop_left, right=crop_right, top=crop_top, bottom=crop_bottom)
                image = opencv.convert_to_rgb(image)
        except Exception as e:
            st.error(str(e))
            st.stop()

st.markdown("---")

# two column layout for image preprocessing options and image preview
col1, col2 = st.columns(spec=2, gap="large")

with col1:
    st.subheader("Image Preview after Upload :eye:")
    if image is not None:
        st.image(raw_image, caption="Uploaded Image Preview after Upload", use_column_width=True)

with col2:
    st.subheader("Image Preview after Preprocessing :eye:")
    if image is not None:
        # preview image
        st.image(image, caption="Uploaded Image Preview after Preprocessing", use_column_width=True)

        # add streamlit button
        if st.button("Extract Text"):
            # streamlit spinner
            with st.spinner("Extracting Text..."):
                text, error = tesseract.image_to_string(
                    image=image,
                    language_short=language_short,
                    config=custom_oem_psm_config,
                    timeout=timeout,
                )
                if error:
                    st.error(error)
                    st.stop()
                elif text:
                    # add streamlit text area
                    st.text_area(label="Extracted Text", value=text, height=500)
                    # add streamlit download button for extracted text
                    st.download_button(
                        label="Download Extracted Text",
                        data=text.encode("utf-8"),
                        file_name="extract.txt",
                        mime="text/plain",
                    )
                else:
                    st.warning("No text was extracted.")
                    st.stop()
