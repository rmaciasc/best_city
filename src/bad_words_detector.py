from profanity_filter import ProfanityFilter

pf = ProfanityFilter()


def detect_bad_words(text: str):
    censored_txt = set(pf.censor(text).split())
    text = set(text.split())
    return text - censored_txt
