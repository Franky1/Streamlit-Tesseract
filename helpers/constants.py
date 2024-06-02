#  all application constants are defined here as dictionaries or lists

languages = {
    "eng": "🇬🇧 English",
    "spa": "🇪🇸 Spanish",
    "fra": "🇫🇷 French",
    "deu": "🇩🇪 German",
    "ita": "🇮🇹 Italian",
    "por": "🇵🇹 Portuguese",
    "ces": "🇨🇿 Czech",
    "pol": "🇵🇱 Polish",
    "tur": "🇹🇷 Turkish",
    "rus": "🇷🇺 Russian",
}

# sort languages by index
languages_sorted = dict(sorted(languages.items(), key=lambda item: item[0]))
# get index of english language as default
default_language_index = list(languages_sorted.keys()).index("eng")

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
    "tur": "tr",
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
    "tur": "🇹🇷",
    "rus": "🇷🇺",
}

# sort flags by index
flags_sorted = dict(sorted(flags.items(), key=lambda item: item[0]))
flag_string = " ".join(flags_sorted.values())


if __name__ == "__main__":
    """This is a constants file, not meant to be run directly.
    Only for testing purposes of this module."""
    print(languages_sorted.keys())
    print(flags_sorted.keys())
    print(default_language_index)
