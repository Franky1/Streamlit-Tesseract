import cv2
import numpy as np
import streamlit as st
from io import BytesIO
from scipy.ndimage import rotate as rotate_image


# make numpy array from image
@st.cache_data
def load_image(image_file: BytesIO) -> np.ndarray:
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    return cv2.imdecode(file_bytes, 1)


# opencv preprocessing grayscale
@st.cache_data
def grayscale(img: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# opencv preprocessing noise removal
@st.cache_data
def remove_noise(img: np.ndarray) -> np.ndarray:
    return cv2.medianBlur(img, 5)


# opencv preprocessing denoising
@st.cache_data
def denoising(img: np.ndarray, strength: int=10) -> np.ndarray:
    if len(img.shape) == 3:
        return cv2.fastNlMeansDenoisingColored(img, None, strength, strength, 7, 21)
    else:
        return cv2.fastNlMeansDenoising(img, None, strength, 7, 21)


# opencv preprocessing thresholding
@st.cache_data
def thresholding(img: np.ndarray, threshold: int=128) -> np.ndarray:
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
def dilate(img: np.ndarray) -> np.ndarray:
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(img, kernel, iterations=1)


# opencv preprocessing erosion
@st.cache_data
def erode(img: np.ndarray) -> np.ndarray:
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(img, kernel, iterations=1)


# opencv preprocessing opening
@st.cache_data
def opening(img: np.ndarray) -> np.ndarray:
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


# opencv convert BGR to RGB
@st.cache_data
def convert_to_rgb(img: np.ndarray) -> np.ndarray:
    # check if image is color
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        return img

@st.cache_data
def rotate90(img, rotate: bool=None) -> np.ndarray:
    '''Rotate the image by 90 degree steps.
    Uses the OpenCV rotate function.'''
    if rotate is not None:
        img = cv2.rotate(img, rotate)
    return img


@st.cache_data
def rotate(img: np.ndarray, angle: int=None) -> np.ndarray:
    '''Rotate the image by free angle degrees.
    Uses the OpenCV warpAffine function. Rotation losses the image corners.
    param angle: angle in degrees
    '''
    if angle is not None:
        height, width = img.shape[:2]
        center = (width/2, height/2)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)
        img = cv2.warpAffine(src=img, M=rotate_matrix, dsize=(width, height), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
    return img


@st.cache_data
def rotate_scipy(img: np.ndarray, angle: int=None, reshape: bool=True) -> np.ndarray:
    '''Rotate the image by free angle degrees.
    param angle: angle in degrees
    param reshape: if True, the image is reshaped to fit the rotated image
    '''
    if angle is not None:
        img = rotate_image(input=img, angle=angle, reshape=reshape, mode='constant', cval=255)
    return img
