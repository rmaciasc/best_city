from better_profanity import profanity
import string


def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation)).lower()


def detect_bad_words(text: str) -> str:
    if not isinstance(text, str):
        str(text)
    profanity.load_censor_words()
    text = remove_punctuation(text)
    censored_txt = set(profanity.censor(text).split())
    text = set(text.split())
    return ", ".join(text - censored_txt)
