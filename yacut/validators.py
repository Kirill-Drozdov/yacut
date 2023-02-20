import re

from yacut.constants import WRONG_CASES


def validate_short_url(short: str) -> bool:
    if len(short) > 16:
        return False
    if re.search(r'[а-яА-Я]', short) is not None:
        return False
    for case in WRONG_CASES:
        if case in short:
            return False
    return True
