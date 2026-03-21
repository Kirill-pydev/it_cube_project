import re
from PyQt6.QtCore import Qt


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def is_valid_name(name):
    if re.match("^[а-яА-ЯёЁa-zA-Z]+$", name) and 1 <= len(name) <= 50:
        return True
    return False

def is_valid_surname(last_name: str) -> bool:
    pattern = r"^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$"
    return bool(re.match(pattern, last_name))


def is_valid_father_name(middle_name: str) -> bool:
    pattern = r"^[А-ЯЁ][а-яё]+$"
    return bool(re.match(pattern, middle_name))


def is_valid_phone_number(phone_number):
    pattern = r'^(?:\+7|8)[0-9]{10}$'
    return bool(re.match(pattern, phone_number))


def repair_lst(a):
    return a[0]


def disabling_buttons(window):
    flags = window.windowFlags()
    flags &= ~Qt.WindowType.WindowMinimizeButtonHint
    flags &= ~Qt.WindowType.WindowMaximizeButtonHint
    flags &= ~Qt.WindowType.WindowCloseButtonHint
    window.setWindowFlags(flags)
