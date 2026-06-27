from datetime import timedelta

from django.db.models import Subquery, OuterRef, F
from django.utils import timezone
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from .filters import ArbitrageDataFilter, HistoryFilter
from .pagination import PageLimitPagination
from .serializers import ArbitrageDataSerializer, ArbitrageHistoryDataSerializer, MarketSerializer
from orderbooks.models import Arbitrage, ArbitrageData, Market


class ListReadOnlyModelViewSet(ListModelMixin, GenericViewSet):
    pass


class ArbitrageDataViewSet(ListReadOnlyModelViewSet):
    queryset = ArbitrageData.latest.filter(timestamp__gte=timezone.now() - timedelta(hours=1))
    serializer_class = ArbitrageDataSerializer
    pagination_class = PageLimitPagination
    filterset_class = ArbitrageDataFilter
    ordering_fields = ('margin',)
    ordering = '-margin'


class ArbitrageHistoryViewSet(ListReadOnlyModelViewSet):
    queryset = ArbitrageData.objects.all()
    serializer_class = ArbitrageHistoryDataSerializer
    filterset_class = HistoryFilter
    ordering_fields = ('timestamp',)
    ordering = '-timestamp'


class MarketViewSet(ListReadOnlyModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
