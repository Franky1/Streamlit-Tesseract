#  all tesseract constants are defined here as dictionaries or lists

languages = {
    "eng": "🇬🇧 English",
    "spa": "🇪🇸 Spanish",
    "fra": "🇫🇷 French",
    "deu": "🇩🇪 German",
    "ita": "🇮🇹 Italian",
    "por": "🇵🇹 Portuguese",
}

flags = {
    "eng": "🇬🇧",
    "spa": "🇪🇸",
    "fra": "🇫🇷",
    "deu": "🇩🇪",
    "ita": "🇮🇹",
    "por": "🇵🇹",
}

flag_string = ' '.join(flags.values())

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
