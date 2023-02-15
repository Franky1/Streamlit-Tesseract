#  all tesseract constants are defined here as dictionaries or lists
import cv2

languages = {
    "eng": "🇬🇧 English",
    "spa": "🇪🇸 Spanish",
    "fra": "🇫🇷 French",
    "deu": "🇩🇪 German",
    "ita": "🇮🇹 Italian",
    "por": "🇵🇹 Portuguese",
    "ces": "🇨🇿 Czech",
    "pol": "🇵🇱 Polish",
    "nor": "🇳🇴 Norwegian",
    "swe": "🇸🇪 Swedish",
    "dan": "🇩🇰 Danish",
    "ron": "🇷🇴 Romanian",
    "tur": "🇹🇷 Turkish",
    "hun": "🇭🇺 Hungarian",
    "rus": "🇷🇺 Russian",
}

# sort languages by index
languages_sorted = dict(sorted(languages.items(), key=lambda item: item[0]))
# get index of english language as default
default_language_index = list(languages_sorted.keys()).index('eng')

# easyocr uses different language codes, so we need to map them
languages_easyocr = {
    "eng": "en",
    "spa": "es",
    "fra": "fr",
    "deu": "de",
    "ita": "it",
    "por": "pt",
    "ces": "cs",
    "pol": "pl",
    "nor": "no",
    "swe": "sv",
    "dan": "da",
    "ron": "ro",
    "tur": "tr",
    "hun": "hu",
    "rus": "ru",
}

flags = {
    "eng": "🇬🇧",
    "spa": "🇪🇸",
    "fra": "🇫🇷",
    "deu": "🇩🇪",
    "ita": "🇮🇹",
    "por": "🇵🇹",
    "ces": "🇨🇿",
    "pol": "🇵🇱",
    "nor": "🇳🇴",
    "swe": "🇸🇪",
    "dan": "🇩🇰",
    "ron": "🇷🇴",
    "tur": "🇹🇷",
    "hun": "🇭🇺",
    "rus": "🇷🇺",
}

# sort flags by index
flags_sorted = dict(sorted(flags.items(), key=lambda item: item[0]))
flag_string = ' '.join(flags_sorted.values())

oem = [
    "Original Tesseract only",
    "Neural nets LSTM only  ",
    "Tesseract + LSTM       ",
    "Default                "
]

psm = [
"Orientation and script detection (OSD) only.                      ",
"Automatic page segmentation with OSD.                             ",
"Automatic page segmentation, but no OSD, or OCR. (not implemented)",
"Fully automatic page segmentation, but no OSD. (Default)          ",
"Assume a single column of text of variable sizes.                 ",
"Assume a single uniform block of vertically aligned text.         ",
"Assume a single uniform block of text.                            ",
"Treat the image as a single text line.                            ",
"Treat the image as a single word.                                 ",
"Treat the image as a single word in a circle.                     ",
"Treat the image as a single character.                            ",
"Sparse text. Find as much text as possible in no particular order.",
"Sparse text with OSD.                                             ",
"Raw line. Treat the image as a single text line.                  ",
]

angles = {
    0 : None,
    90 : cv2.ROTATE_90_CLOCKWISE,
    180 : cv2.ROTATE_180,
    270 : cv2.ROTATE_90_COUNTERCLOCKWISE,
}


if __name__ == "__main__":
    """This is a constants file, not meant to be run directly.
    Only for testing purposes of this module."""
    print(languages_sorted.keys())
    print(flags_sorted.keys())
    print(default_language_index)
    print(angles[90])
