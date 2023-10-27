import streamlit as st
import helpers.tesseract as tesseract

def show_image_preview_controls(image):

    config = st.session_state.tesseract_config

    language_short = config['language']
    psm = config['psm']
    timeout = config['timeout']

    st.subheader("Image Preview")
    if image is not None:
        # preview image
        st.image(image, caption="Uploaded Image Preview", use_column_width=True)

        # add streamlit button
        if st.button("Extract Text"):
            # streamlit spinner
            with st.spinner("Extracting Text..."):
                try:
                 
                    text = tesseract.extract_text_from_image(image, language_short, psm, timeout)
                    print(text)
                    
                    if text:
                        # TODO: move this to the whole page again
                        # TODO: try Ace Editor for text area instead
                        # add streamlit text area
                        st.text_area("Extracted Text", value=text, height=500, key="extracted_text")
                        
                        # add streamlit download button for extracted text
                        st.download_button("Download Extracted Text", data=text.encode("utf-8"), file_name="extract.txt", mime="text/plain", key="download_button")
                    else:
                        st.warning("No text was extracted. Please try again with a different image or settings.")
                        st.stop()
                except Exception as e:
                    st.error("An unexpected error occurred.")
                    st.error(f"Error Message: {str(e)}")
                    st.stop()




    return "OK"