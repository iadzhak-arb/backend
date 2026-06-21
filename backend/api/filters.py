from django_filters import rest_framework as filters

from orderbooks.models import Arbitrage, ArbitrageData


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


class ArbitrageFilter(filters.FilterSet):
    market_buy = filters.CharFilter(field_name='arbitrage__ob_buy__symbol__market__id')
    market_sell = filters.CharFilter(field_name='arbitrage__ob_sell__symbol__market__id')
    margin_min = filters.NumberFilter(field_name='margin', lookup_expr='gte')
    margin_max = filters.NumberFilter(field_name='margin', lookup_expr='lte')

    class Meta:
        model = ArbitrageData
        fields = ('market_buy', 'market_sell', 'margin_min', 'margin_max')
