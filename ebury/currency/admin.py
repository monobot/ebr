from django.contrib import admin

from currency.models import Trade


@admin.register(Trade)
class TradesAdmin(admin.ModelAdmin):
    list_display = (
        'identifier',
        'sell_currency',
        'sell_amount',
        'buy_currency',
        'buy_amount',
        'rate',
        'date_booked',
    )
    list_filter = (
        'date_booked',
        'sell_currency',
        'buy_currency',
    )
