from django.db.models import Min, Max
from django.shortcuts import get_list_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import ArbitrageFilter
from .pagination import PageLimitPagination
from .serializers import ArbitrageDataSerializer, ArbitrageHistoryDataSerializer, MarketSerializer
from orderbooks.models import Arbitrage, ArbitrageData, Market


class ArbitrageViewSet(ReadOnlyModelViewSet):
    queryset = ArbitrageData.latest.all().select_related(
        'arbitrage__ob_buy__symbol',
        'arbitrage__ob_buy__exchange',
        'arbitrage__ob_sell__symbol',
        'arbitrage__ob_sell__exchange',
    )
    serializer_class = ArbitrageDataSerializer
    pagination_class = PageLimitPagination
    filterset_class = ArbitrageFilter
    ordering = '-margin'

    def retrieve(self, request, *args, **kwargs):
        arbitrage = get_list_or_404(
            ArbitrageData.objects.filter(arbitrage=kwargs['pk'])
        )
        serializer = ArbitrageHistoryDataSerializer(arbitrage, many=True)
        return Response(serializer.data)


class MarketViewSet(ReadOnlyModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
