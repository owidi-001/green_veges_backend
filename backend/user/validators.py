import re


def email_validator(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(pattern, email)


def phone_number_validator(phone_number):
    pattern = r"\+254\w{9}"
    return re.match(pattern, phone_number)
