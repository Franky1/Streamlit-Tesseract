import streamlit as st


def show_image_preview_controls(image):
    st.subheader("Image Preview")
    if image is not None:
        # preview image
        st.image(image, caption="Uploaded Image Preview", use_column_width=True)   

    return "OK"