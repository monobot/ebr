from rest_framework import serializers

from currency.models import Trade


class TradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = (
            'identifier',
            'sell_currency',
            'sell_amount',
            'buy_currency',
            'buy_amount',
            'rate',
            'date',
        )


class TradePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        # I want all these fields to be returned when the process finish
        fields = (
            'identifier',
            'sell_currency',
            'sell_amount',
            'buy_currency',
            'buy_amount',
            'rate',
            'date',
        )
        # but these fields not available in the api form
        read_only_fields = (
            'buy_amount',
            'rate',
            'identifier',
            'date',
        )
