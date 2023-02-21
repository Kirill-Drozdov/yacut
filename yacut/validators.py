import re

from yacut.constants import WRONG_CASES, WRONG_RU_CASE


def validate_short_url(short: str) -> bool:
    if len(short) > 16:
        return False
    if re.search(WRONG_RU_CASE, short) is not None:
        return False
    for case in WRONG_CASES:
        if case in short:
            return False
    return True
