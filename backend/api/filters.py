from django.db.models import Q
from django_filters import rest_framework as filters

from orderbooks.models import ArbitrageData


class ArbitrageDataFilter(filters.FilterSet):
    token = filters.CharFilter(method='token_filter')
    quote = filters.CharFilter(method='quote_filter')
    market_buy = filters.CharFilter(
        field_name='arbitrage__ob_buy__symbol__market__id'
    )
    market_sell = filters.CharFilter(
        field_name='arbitrage__ob_sell__symbol__market__id'
    )
    margin_min = filters.NumberFilter(field_name='margin', lookup_expr='gte')
    margin_max = filters.NumberFilter(field_name='margin', lookup_expr='lte')

    class Meta:
        model = ArbitrageData
        fields = ('market_buy', 'market_sell', 'margin_min', 'margin_max', 'token', 'quote')
        exclude = ('pk',)

    def token_filter(self, queryset, name, value):
        if not value:
            return queryset
        tokens = value.upper().split(',')
        return queryset.filter(
            arbitrage__ob_buy__symbol__base__id__in=tokens,
            arbitrage__ob_sell__symbol__base__id__in=tokens,
        )

    def token_not_filter(self, queryset, name, value):
        if not value:
            return queryset
        tokens = value.upper().split(',')
        return queryset.exclude(
            arbitrage__ob_buy__symbol__base__id__in=tokens
        ).exclude(
            arbitrage__ob_sell__symbol__base__id__in=tokens,
        )

    def quote_filter(self, queryset, name, value):
        if not value:
            return queryset
        quotes = value.upper().split(',')
        return queryset.filter(
            Q(arbitrage__ob_buy__symbol__quote__id__in=quotes),
            Q(arbitrage__ob_sell__symbol__quote__id__in=quotes),
        )
