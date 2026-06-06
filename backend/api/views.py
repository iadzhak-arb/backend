from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import ArbitrageSerializer
from orderbooks.models import Arbitrage, ArbitrageData


class ArbitrageViewSet(ReadOnlyModelViewSet):
    queryset = ArbitrageData.latest.all()
    serializer_class = ArbitrageSerializer
