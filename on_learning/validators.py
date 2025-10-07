import re

from rest_framework.exceptions import ValidationError

from config.settings import ALLOWED_URLS


class CorrectURLValidator:
    """ Проверка вводимого URL """

    def __init__(self, field):
        self.field = field

    def __call__(self, data):
        value = data.get(self.field)

        if value is None:
            return

        allowed_url = any(re.match(url, value) for url in ALLOWED_URLS)

        if not allowed_url:
            raise ValidationError(f"{value} не корректный URL !")
