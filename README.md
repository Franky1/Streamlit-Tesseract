# Streamlit Tesseract Test

Streamlit demo project with Tesseract running on Streamlit Cloud.

## App Usage

1. Upload an image with text on it
2. Select the language
3. Select the image preprocessing options (if needed) and check the result in the preview
4. Run the OCR and check the result in the text preview
5. Adjust the settings or image preprocessing and run the OCR again (if needed)
6. Download the result as a text file or copy from the text preview

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

#### Grayscale Conversion

```python
import cv2
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# or
coefficients = [1,0,0] # Gives blue channel all the weight
# for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
m = np.array(coefficients).reshape((1,3))
blue = cv2.transform(im, m)
```

#### Brightness and Contrast

- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- <https://www.tutorialspoint.com/how-to-change-the-contrast-and-brightness-of-an-image-using-opencv-in-python>
- <https://stackoverflow.com/questions/50474302/how-do-i-adjust-brightness-contrast-and-vibrance-with-opencv-python>
- <https://stackoverflow.com/questions/32609098/how-to-fast-change-image-brightness-with-python-opencv>
- <https://github.com/milahu/document-photo-auto-threshold>
- <https://stackoverflow.com/questions/56905592/automatic-contrast-and-brightness-adjustment-of-a-color-photo-of-a-sheet-of-pape>
- <https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv>
- <https://stackoverflow.com/questions/63243202/how-to-auto-adjust-contrast-and-brightness-of-a-scanned-image-with-opencv-python>

#### Image Rotation

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
- [x] Add more OpenCV preprocessing options for rotation
- [ ] Add more OpenCV preprocessing options for cropping
- [ ] Add more OpenCV preprocessing options for brightness and contrast
- [ ] Add non-destructive image rotation
- [ ] Add two column design
- [x] Add import of pdf files with pdf2image
- [x] Add more error handling
- [x] Add caching to speed up the app
- [x] Add a progress bar
- [x] Add more languages
- [ ] Test it on Streamlit Cloud

## Status

> Work in Progress - Not finished yet - 12.02.2023
