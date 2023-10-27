import streamlit as st

def show_image_processing_controls():
    st.header("Image Preprocessing")
    st.write("Check the boxes below to apply preprocessing to the image.")
    cGrayscale = st.checkbox(label="Grayscale", value=True, key="grayscale_checkbox")
    cDenoising = st.checkbox(label="Denoising", value=False, key="denoising_checkbox")
    cDenoisingStrength = st.slider(label="Denoising Strength", min_value=1, max_value=40, value=10, step=1, key="denoising_strength_slider")
    cThresholding = st.checkbox(label="Thresholding", value=False, key="thresholding_checkbox")
    cThresholdLevel = st.slider(label="Threshold Level", min_value=0, max_value=255, value=128, step=1, key="threshold_level_slider")
    cRotate90 = st.checkbox(label="Rotate in 90° steps", value=False, key="rotate_90_checkbox")
    angle90 = st.slider("Rotate rectangular [Degree]", min_value=0, max_value=270, value=0, step=90, key="rotate_90_slider")
    cRotateFree = st.checkbox(label="Rotate in free degrees", value=False, key="rotate_free_checkbox")
    angle = st.slider("Rotate freely [Degree]", min_value=-180, max_value=180, value=0, step=1, key="rotate_free_slider")

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