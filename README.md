# Streamlit Tesseract Test

Streamlit demo project with Tesseract running on Streamlit Cloud.

## App Usage

1. Upload an image with text on it
2. Select the language
3. Set the Page segmentation mode (if needed)
4. Select the image preprocessing (if needed) and check the result in the preview
5. Run the OCR and check the result in the text preview
6. Adjust the settings or image preprocessing and run the OCR again (if needed)
7. Download the result as a text file

## Developer Usage

> tbd.

## Resources

### Tesseract

- Tesseract Documentation
  - <https://tesseract-ocr.github.io/>
- pytesseract Documentation
  - <https://github.com/madmaze/pytesseract>
- OCR with Tesseract
  - <https://nanonets.com/blog/ocr-with-tesseract/>

### pdf2image

<https://github.com/Belval/pdf2image>

### OpenCV

OpenCV is used for image preprocessing before running OCR with Tesseract because image preprocessing is a crucial step in achieving accurate OCR results. The following are some of the reasons why image preprocessing is important and why OpenCV is a commonly used library for this purpose:

- Image enhancement: Image preprocessing can improve the visual quality of an image and make it easier for OCR software to identify and extract text. OpenCV provides a wide range of image enhancement techniques such as thresholding, contrast stretching, and histogram equalization that can be used to improve the quality of an image before running OCR.
- Noise reduction: Digital images often contain noise which can negatively impact the accuracy of OCR results. OpenCV provides filters such as Gaussian and median filters that can be used to reduce noise in an image.
- Binarization: OCR software works best with black and white images rather than color images. OpenCV provides functions to convert an image into a binary format, which makes it easier for OCR software to identify and extract text.

In summary, OpenCV is used for image preprocessing before running OCR with Tesseract because it provides a wide range of tools and techniques for improving the quality of an image, making it easier for OCR software to produce accurate results.

The following resources are helpful to understand the image preprocessing options.

- OpenCV Image Processing Documentation
  - <https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html>
- OpenCV Python Tutorial
  - <https://www.geeksforgeeks.org/opencv-python-tutorial/>
- OCR in Python Tutorials
  - <https://www.youtube.com/watch?v=tQGgGY8mTP0&list=PL2VXyKi-KpYuTAZz__9KVl1jQz74bDG7i>

### Image Rotation

#### opencv

```python
import cv2
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1)
rotated = cv2.warpAffine(image, M, (w, h))
```

#### imutils

```python
import imutils
rotate = imutils.rotate_bound(image, angle)
```

#### scipy

```python
from scipy.ndimage import rotate as rotate_image
rotated_img1 = rotate_image(img,90)
```

---

## ToDo

- [x] Test it locally with Docker
- [x] Add OpenCV preprocessing of the image
- [ ] Add more OpenCV preprocessing options for cropping, rotation, etc.
- [ ] Add two column design
- [ ] Add import of pdf files with pdf2image
- [x] Add more error handling
- [x] Add caching to speed up the app
- [x] Add a progress bar
- [x] Add more languages
- [ ] Test it on Streamlit Cloud

## Status

> Work in Progress - Not finished yet - 12.02.2023
