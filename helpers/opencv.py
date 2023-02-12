import cv2
import numpy as np
import streamlit as st


# make numpy array from image
@st.cache_data
def load_image(image_file):
    # img = cv2.imread(image_file)
    # return np.array(img)
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, 1)

# opencv preprocessing grayscale
@st.cache_data
def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# opencv preprocessing noise removal
@st.cache_data
def remove_noise(img):
    return cv2.medianBlur(img, 5)

# opencv preprocessing denoising
@st.cache_data
def denoising(img, strength=10):
    if len(img.shape) == 3:
        return cv2.fastNlMeansDenoisingColored(img, None, strength, strength, 7, 21)
    else:
        return cv2.fastNlMeansDenoising(img, None, strength, 7, 21)

# opencv preprocessing thresholding
@st.cache_data
def thresholding(img, threshold=128):
    # FIXME: add handling for color images
    # Convert the image to grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply the threshold
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    return img

    # # check if image is grayscale
    # if len(img.shape) == 2:
    #     return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # # else:
    # # Convert the image to HSV
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # # Define a range of colors to threshold
    # lower_color = np.array([0, 50, 50])
    # upper_color = np.array([10, 255, 255])

    # # Threshold the image to get only the desired colors
    # mask = cv2.inRange(hsv, lower_color, upper_color)
    # thresholded_img = cv2.bitwise_and(img, img, mask=mask)
    # return thresholded_img

# opencv preprocessing dilation
@st.cache_data
def dilate(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)

# opencv preprocessing erosion
@st.cache_data
def erode(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(img, kernel, iterations=1)

# opencv preprocessing opening
@st.cache_data
def opening(img):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# opencv convert BGR to RGB
@st.cache_data
def convert_to_rgb(img):
    # check if image is color
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        return img
