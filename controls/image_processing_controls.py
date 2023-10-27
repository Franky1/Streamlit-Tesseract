
import streamlit as st

def show_image_processing_controls():
    st.header("Image Preprocessing")
    st.write("Check the boxes below to apply preprocessing to the image.")
    cGrayscale = st.checkbox(label="Grayscale", value=True)
    cDenoising = st.checkbox(label="Denoising", value=False)
    cDenoisingStrength = st.slider(label="Denoising Strength", min_value=1, max_value=40, value=10, step=1)
    cThresholding = st.checkbox(label="Thresholding", value=False)
    cThresholdLevel = st.slider(label="Threshold Level", min_value=0, max_value=255, value=128, step=1)
    cRotate90 = st.checkbox(label="Rotate in 90° steps", value=False)
    angle90 = st.slider("Rotate rectangular [Degree]", min_value=0, max_value=270, value=0, step=90)
    cRotateFree = st.checkbox(label="Rotate in free degrees", value=False)
    angle = st.slider("Rotate freely [Degree]", min_value=-180, max_value=180, value=0, step=1)

    # update image_processing_config
    
    st.session_state.image_processing_config = {
        'Grayscale': cGrayscale,
        'Denoising': cDenoising,
        'DenoisingStrength': cDenoisingStrength,
        'Thresholding': cThresholding,
        'ThresholdLevel': cThresholdLevel,
        'Rotate90': cRotate90,
        'Angle90': angle90,
        'RotateFree': cRotateFree,
        'Angle': angle
    }

    return "OK"