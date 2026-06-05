from django_filters import rest_framework as filters

from orderbooks.models import Arbitrage


class ArbitrageHistoryFilter(filters.FilterSet):
    buy_exchange = filters.CharFilter(
        field_name='buy_exchange__name',
        required=True
    )
    buy_symbol = filters.CharFilter(
        field_name='buy_symbol__id',
        required=True
    )
    sell_exchange = filters.CharFilter(
        field_name='sell_exchange__name',
        required=True
    )
    sell_symbol = filters.CharFilter(
        field_name='sell_symbol__id',
        required=True
    )

    class Meta:
        model = Arbitrage
        fields = ('buy_exchange', 'buy_symbol', 'sell_exchange', 'sell_symbol')
