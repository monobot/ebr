# -*- coding: utf-8 -*-
from model_mommy import mommy
import re

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase


class HelpMethods(object):

    def api_request(self, url, data=None, user=None, verb=None):
        if user:
            self.client.force_authenticate(user=user)

        if not data:
            return verb(url, theformat='json')
        return verb(url, data, theformat='json')

    def api_get(self, url, user=None):
        return self.api_request(
            url,
            user=user,
            verb=self.client.get
        )

    def api_put(self, url, data, user=None):
        return self.api_request(
            url,
            data=data,
            user=user,
            verb=self.client.put
        )

    def api_patch(self, url, data, user=None):
        return self.api_request(
            url,
            data=data,
            user=user,
            verb=self.client.patch
        )

    def api_post(self, url, data, user=None):
        return self.api_request(
            url,
            data=data,
            user=user,
            verb=self.client.post
        )

    def api_delete(self, url, data=None, user=None):
        return self.response(
            url,
            data=data,
            user=user,
            verb=self.client.delete
        )


class ApiViewTests(APITestCase, HelpMethods):
    def setUp(self):
        self.user = mommy.make(User)

        mommy.make(
            'currency.Trade',
            sell_currency='GBP',
            buy_currency='EUR',
            _quantity=25
        )

    def test_trades_get_not_logged(self):
        url = reverse('api:trades')

        # any user can get the list of trades
        response = self.api_get(url)

        self.assertEqual(response.status_code, 403)

    def test_trades_get_logged(self):
        url = reverse('api:trades')

        # any user can get the list of trades
        response = self.api_get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 25)

    def test_trades_post_not_logged(self):
        url = reverse('api:trades')
        data = {
            'sell_currency': 'GBP',
            'sell_amount': 1000,
            'buy_currency': 'EUR',
        }

        # any user can get the list of trades
        response = self.api_post(url, data)

        self.assertEqual(response.status_code, 403)

    def test_trades_post_logged(self):
        url = reverse('api:trades')
        data = {
            'sell_currency': 'GBP',
            'sell_amount': 1000,
            'buy_currency': 'EUR',
        }

        # any user can get the list of trades
        response = self.api_post(url, data, user=self.user)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get('identifier').startswith('TR'))
        self.assertEqual(len(response.data.get('identifier')), 9)
        self.assertTrue(
            re.match(
                r'[\d]{4}[/][\d]{2}[/][\d]{2} [\d]{2}[:][\d]{2}',
                response.data.get('date'),
            )
        )
