from better_profanity import profanity
import string


def detect_bad_words(text: str):
    if not isinstance(text, str):
        str(text)
    profanity.load_censor_words()
    text = text.translate(str.maketrans("", "", string.punctuation)).lower()

    censored_txt = set(profanity.censor(text).split())
    text = set(text.split())
    return ", ".join(text - censored_txt)
