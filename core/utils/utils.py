import random
import string
from json import JSONDecodeError

from requests import Response


def generate_string(letters: bool = True, digits: bool = True, punctuation: bool = False, length: int = 5) -> str:
    source_string = ""
    if letters:
        source_string += string.ascii_letters
    if digits:
        source_string += string.digits
    if punctuation:
        source_string += string.punctuation

    return ''.join(random.choices(source_string, k=length))


def get_response_content(response: Response):
    try:
        response_content = response.json()
    except JSONDecodeError:
        response_content = response.text
    return response_content