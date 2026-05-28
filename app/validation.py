import re
import unicodedata

# Keep only letters and numbers; ignore spaces/punctuation in matching.
NON_ALNUM_RE = re.compile(r"[^\w]+", flags=re.UNICODE)


def turkish_upper(text: str) -> str:
    result: list[str] = []
    for char in text:
        if char == "i":
            result.append("İ")
        elif char == "ı":
            result.append("I")
        else:
            result.append(char.upper())
    return "".join(result)


def normalize_guess(text: str) -> str:
    text = unicodedata.normalize("NFC", text.strip())
    text = turkish_upper(text)
    return NON_ALNUM_RE.sub("", text)


def answers_match(guess: str, answer: str) -> bool:
    return normalize_guess(guess) == normalize_guess(answer)
