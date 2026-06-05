import django_filters
from django.utils import choices

from .models import Arbitrage, Market, Exchange, Token, Symbol

markets = [
    (m.id, m.id)
    for m in Market.objects.all()
]
exchanges = [
    (ex.name, ex.name)
    for ex in Exchange.objects.all()
]
tokens = [
    (t.id, t.id)
    for t in Token.objects.all()
]
symbols = [
    (s.id, s.id)
    for s in Symbol.objects.all()
]


class ArbitrageFilter(django_filters.FilterSet):
    margin__gt = django_filters.NumberFilter(field_name='margin', lookup_expr='gt')
    margin__lt = django_filters.NumberFilter(field_name='margin', lookup_expr='lt')

    market_buy = django_filters.ChoiceFilter(
        field_name='buy_symbol__market__id',
        choices=markets
    )
    market_sell = django_filters.ChoiceFilter(
        field_name='sell_symbol__market__id',
        choices=markets
    )
    exchange_buy = django_filters.ChoiceFilter(
        field_name='buy_exchange__name',
        choices=exchanges
    )
    exchange_sell = django_filters.ChoiceFilter(
        field_name='sell_exchange__name',
        choices=exchanges
    )
    base = django_filters.ChoiceFilter(
        field_name='buy_symbol__base__id',
        choices=tokens,
    )

    class Meta:
        model = Arbitrage
        fields = []


class ArbitrageHistoryFilter(django_filters.FilterSet):
    buy_exchange = django_filters.ChoiceFilter(
        field_name='buy_exchange__name',
        choices=exchanges,
    )
    buy_symbol = django_filters.ChoiceFilter(
        field_name='buy_symbol__id',
        choices=symbols,
    )
    sell_exchange = django_filters.ChoiceFilter(
        field_name='sell_exchange__name',
        choices=exchanges,
    )
    sell_symbol = django_filters.ChoiceFilter(
        field_name='sell_symbol__id',
        choices=symbols,
    )

    class Meta:
        model = Arbitrage
        fields = ('buy_exchange', 'buy_symbol', 'sell_exchange', 'sell_symbol')
