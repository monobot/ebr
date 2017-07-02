import hashlib
import requests
import decimal

from django.utils import timezone

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.exceptions import NotAcceptable

from .currencies import CURRENCIES


class Trade(models.Model):
    # TR428YR1O
    identifier = models.CharField(
        null=False, max_length=9, unique=True, blank=True
    )

    sell_currency = models.CharField(choices=CURRENCIES, max_length=3)
    sell_amount = models.DecimalField(max_digits=11, decimal_places=2)

    buy_currency = models.CharField(choices=CURRENCIES, max_length=3)
    buy_amount = models.DecimalField(
        blank=True, null=True, max_digits=11, decimal_places=2
    )

    rate = models.DecimalField(max_digits=11, decimal_places=7)

    date_booked = models.DateTimeField(auto_now_add=True)

    @property
    def date(self):
        return self.date_booked.strftime('%Y/%m/%d %H:%M')

    @staticmethod
    def get_hashedid(obj_id, date):
        saltedstring = '{}thisismy=saltedstring{}'.format(obj_id, date)
        saltedstring = saltedstring.encode('utf8')

        return 'TR{}'.format(hashlib.sha512(saltedstring).hexdigest())[:9]

    def confirm_identifier(self, identifier):
        # its low but can exist collision for hashed indentifiers
        if not Trade.objects.filter(identifier=identifier):
            return identifier
        return self.confirm_identifier(
            self.get_hashedid(self.id, timezone.now())
        )

    def __str__(self):
        return '{} {}{} at {} = {}{} on {}'.format(
            self.identifier,
            self.sell_currency,
            self.sell_amount,
            self.rate,
            self.buy_currency,
            self.buy_amount,
            self.date,
        )

    class Meta:
        ordering = ('date_booked', )


@receiver(pre_save, sender=Trade, dispatch_uid="before_trade_save")
def before_trade_save(sender, instance, **kwargs):
    # if its a new trade
    if not instance.identifier:
        # aply a correct identifier
        instance.identifier = instance.confirm_identifier(
            instance.get_hashedid(instance.id, instance.date_booked)
        )

        # locate the exact exchange in real
        url = 'http://api.fixer.io/latest?base={}&symbols={}'.format(
            instance.sell_currency,
            instance.buy_currency,
        )
        exchange_request = requests.get(url)

        # raise an error if the exchange provider is not online
        # the cached version is only for preview purposes
        if exchange_request.status_code != 200:
            raise NotAcceptable(
                'can not get exchange information right now, please try '
                'again later'
            )

        instance.rate = exchange_request.json()['rates'][instance.buy_currency]
        instance.buy_amount = (
            instance.sell_amount * decimal.Decimal(instance.rate)
        )
