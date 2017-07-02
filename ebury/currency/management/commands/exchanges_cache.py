import requests
import logging
import json


from django.core.cache import cache
from django.core.management.base import BaseCommand

from currency.currencies import CURRENCIES

logger = logging.getLogger('ebury')


class Command(BaseCommand):

    def handle(self, *args, **options):
        exchanges_cache = {}
        for cur, verbose_cur in CURRENCIES:
            url = 'http://api.fixer.io/latest?base={}'.format(cur)
            exchange_request = requests.get(url)

            logging.info(exchange_request.json())
            exchanges_cache.update({cur: exchange_request.json()['rates']})
        cache.set(
            'exchanges_cache',
            json.dumps(exchanges_cache),
            timeout=86400
        )
