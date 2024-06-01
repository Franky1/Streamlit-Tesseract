<!-- markdownlint-disable MD026 -->
# Streamlit Tesseract OCR :mag_right: :page_facing_up:

Streamlit project with Tesseract OCR running on Streamlit Cloud.

[![Streamlit](https://img.shields.io/badge/Go%20To-Streamlit%20Cloud%20Application-red?logo=streamlit)](https://tesseractocr.streamlit.app/)

## App Usage :computer:

1. Upload an image with text on it
2. Select the language
3. Select the image preprocessing options (if needed) and check the result in the preview
4. Run the OCR and check the result in the text preview
5. Adjust the settings or image preprocessing and run the OCR again (if needed)
6. Download the result as a text file or copy from the text preview

## Status :heavy_check_mark:

> First running Streamlit application - 01.06.2024

## ToDo :pencil:

- [ ] Update README.md
- [ ] Change layout to 3 columns(?)
- [ ] Add some more CSS styling
- [ ] Cleanup of app and repository

## Future Ideas :bulb:

- Use Pillow for image preprocessing instead of OpenCV
  - any advantages?
- Add Ace Editor for text preview
  - any advantages?
- Add other OCR engines and test them
- Add `easyocr` and test it
  - <https://github.com/JaidedAI/EasyOCR>
- Try `tesserocr` instead of `pytesseract`
  - <https://github.com/sirfz/tesserocr>
- Add `PyMuPDF` and test it
  - <https://github.com/pymupdf/PyMuPDF>
- Add `ocrmypdf` and test it
  - <https://github.com/ocrmypdf/OCRmyPDF>
- Add `PaddleOCR` and test it
  - <https://github.com/PaddlePaddle/PaddleOCR>
- Add `keras-ocr` and test it
  - <https://github.com/faustomorales/keras-ocr>

## Libraries :books:

### Tesseract

- Tesseract Documentation
  - <https://tesseract-ocr.github.io/>
- pytesseract Documentation
  - <https://github.com/madmaze/pytesseract>
- OCR with Tesseract
  - <https://nanonets.com/blog/ocr-with-tesseract/>

### EasyOCR

- <https://github.com/JaidedAI/EasyOCR>

### pdf2image

- <https://github.com/Belval/pdf2image>

### OpenCV

OpenCV is used for image preprocessing before running OCR with Tesseract.

- OpenCV Image Processing Documentation
  - <https://docs.opencv.org/4.x/d2/d96/tutorial_py_table_of_contents_imgproc.html>
- OpenCV Python Tutorial
  - <https://www.geeksforgeeks.org/opencv-python-tutorial/>
- OCR in Python Tutorials
  - <https://www.youtube.com/watch?v=tQGgGY8mTP0&list=PL2VXyKi-KpYuTAZz__9KVl1jQz74bDG7i>

### Pillow

- <https://pillow.readthedocs.io/en/stable/>

## Image Preprocessing :framed_picture:

### Grayscale Conversion

```python
import cv2
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# or
coefficients = [1,0,0] # Gives blue channel all the weight
# for standard gray conversion, coefficients = [0.114, 0.587, 0.299]
m = np.array(coefficients).reshape((1,3))
blue = cv2.transform(im, m)
```

### Brightness and Contrast

- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- <https://www.tutorialspoint.com/how-to-change-the-contrast-and-brightness-of-an-image-using-opencv-in-python>
- <https://stackoverflow.com/questions/50474302/how-do-i-adjust-brightness-contrast-and-vibrance-with-opencv-python>
- <https://stackoverflow.com/questions/32609098/how-to-fast-change-image-brightness-with-python-opencv>
- <https://github.com/milahu/document-photo-auto-threshold>
- <https://stackoverflow.com/questions/56905592/automatic-contrast-and-brightness-adjustment-of-a-color-photo-of-a-sheet-of-pape>
- <https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv>
- <https://stackoverflow.com/questions/63243202/how-to-auto-adjust-contrast-and-brightness-of-a-scanned-image-with-opencv-python>

### Image Rotation :arrows_counterclockwise:

Methods to rotate an image with different libraries.

#### ... with Pillow :arrows_counterclockwise:

<https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.rotate>

```python
from PIL import Image
with Image.open("hopper.jpg") as im:
    # Rotate the image by 60 degrees counter clockwise
    theta = 60
    white = (255,255,255)
    # Angle is in degrees counter clockwise
    im_rotated = im.rotate(angle=theta, resample=Image.Resampling.BICUBIC, expand=1, fillcolor=white)
```

#### ... with OpenCV :arrows_counterclockwise:

> destructive rotation, loses image data

```python
import cv2
(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1)
rotated = cv2.warpAffine(image, M, (w, h))
```

#### ... with imutils :arrows_counterclockwise:

> non-destructive rotation, keeps image data

```python
import imutils
rotate = imutils.rotate_bound(image, angle)
```

#### ... with scipy :arrows_counterclockwise:

> destructive or non-destructive rotation, can be chosen py parameter `reshape`

```python
from scipy.ndimage import rotate as rotate_image
rotated_img1 = rotate_image(input, angle, reshape, mode, cval)
```
