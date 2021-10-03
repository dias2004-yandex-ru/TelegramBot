# УТИЛИТЫ БОТА (классы)
import requests
import json
from MyBotConfig import currency, SITE, ACCESS_KEY


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):
        try:
            base_key = currency[base.lower()]
        except KeyError:
            raise APIException(f'недопустимая валюта:\n{base}')

        try:
            quote_key = currency[quote.lower()]
        except KeyError:
            raise APIException(f'недопустимая валюта:\n{quote}')

        try:
            amount = round(float(amount), 2)
        except ValueError:
            raise APIException(f'недопустимое значение количества:\n{amount}')

        r = requests.get(f'{SITE}latest?access_key={ACCESS_KEY}&base=EUR&symbols=EUR,USD,RUB')
        t = json.loads(r.content)
        res = round(t['rates'][quote_key] / t['rates'][base_key] * amount, 2)
        return f'Цена за {amount} {base} в валюте {quote} = {res}'
