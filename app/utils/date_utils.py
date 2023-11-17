from datetime import timedelta

import pytimeparse


def parse_str_to_timedelta(value: str) -> timedelta | str:
    seconds = pytimeparse.parse(value)
    if not seconds:
        return value
    return timedelta(seconds=seconds)
