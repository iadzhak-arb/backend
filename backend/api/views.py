from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import ArbitrageHistoryFilter
from .serializers import ArbitrageSerializer, HistorySerializer
from orderbooks.models import Arbitrage


class ArbitrageViewSet(ReadOnlyModelViewSet):
    queryset = Arbitrage.latest.all()
    serializer_class = ArbitrageSerializer
    pagination_class = PageNumberPagination


class HistoryViewSet(ReadOnlyModelViewSet):
    queryset = Arbitrage.objects.all()
    serializer_class = HistorySerializer
    filterset_class = ArbitrageHistoryFilter

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Доступ к отдельным объектам запрещён.'},
            status=status.HTTP_403_FORBIDDEN
        )
