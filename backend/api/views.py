from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet

from .constants import RESPONSE_LIST_STR, DELTA_FRESH, RESPONSE_STR, DEMO_SIZE, RESPONSE_SUMMARY
from .filters import ArbitrageDataFilter
from .pagination import PageLimitPagination
from .serializers import ArbitrageDataSerializer, ArbitrageSerializer, \
    ArbitrageRetrieveSerializer
from orderbooks.models import Arbitrage, ArbitrageData, Market, Token, Exchange, Symbol


class ArbitrageViewSet(ReadOnlyModelViewSet):
    queryset = Arbitrage.objects.with_name()
    serializer_class = ArbitrageSerializer
    pagination_class = PageLimitPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = None

    def get_queryset(self):
        if self.action == 'retrieve':
            return Arbitrage.objects.with_history()
        if self.action == 'demo_spot_spot':
            return ArbitrageData.latest.demo('spot', 'spot', size=DEMO_SIZE)
        if self.action == 'demo_spot_swap':
            return ArbitrageData.latest.demo('spot', 'swap', size=DEMO_SIZE)
        if self.action == 'latest':
            return ArbitrageData.latest.by_time(DELTA_FRESH).order_by('-margin')
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action in {'retrieve', 'back'}:
            return ArbitrageRetrieveSerializer
        if self.action in {'latest', 'demo_spot_swap', 'demo_spot_spot'}:
            return ArbitrageDataSerializer
        return ArbitrageSerializer

    @action(detail=True, methods=['get'])
    def back(self, request, pk=None):
        obj = self.get_object()
        back = get_object_or_404(
            Arbitrage.objects.with_name(),
            ob_buy=obj.ob_sell,
            ob_sell=obj.ob_buy,
        )
        serializer = ArbitrageRetrieveSerializer(back)
        return Response(serializer.data)

    @extend_schema(responses=ArbitrageDataSerializer(many=True))
    @action(
        detail=False,
        methods=['get'],
        queryset=ArbitrageData.latest.by_time(DELTA_FRESH).order_by('-margin'),
        pagination_class=PageLimitPagination,
        filter_backends=[DjangoFilterBackend],
        filterset_class=ArbitrageDataFilter,
    )
    def latest(self, request):
        qs = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @extend_schema(responses=ArbitrageDataSerializer(many=True))
    @action(
        detail=False,
        methods=['get'],
        url_path='demo-spot',
        pagination_class=None,
        filter_backends=[],
    )
    def demo_spot_spot(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ArbitrageDataSerializer(many=True))
    @action(
        detail=False,
        methods=['get'],
        url_path='demo-swap',
        pagination_class=None,
        filter_backends=[]
    )
    def demo_spot_swap(self, request):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class MarketViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=RESPONSE_STR)
    def list(self, request):
        market_ids = Market.objects.values_list('id', flat=True)
        return Response(market_ids)


class TokenViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    @extend_schema(responses=RESPONSE_STR)
    def list(self, request):
        token_ids = Token.objects.all_list()
        return Response(token_ids)

    @extend_schema(responses=RESPONSE_LIST_STR)
    @action(detail=False, methods=['get'])
    def base(self, request):
        token_ids = Token.objects.base_list()
        return Response(token_ids)

    @extend_schema(responses=RESPONSE_LIST_STR)
    @action(detail=False, methods=['get'])
    def quote(self, request):
        token_ids = Token.objects.quote_list()
        return Response(token_ids)

    @extend_schema(responses=RESPONSE_LIST_STR)
    @action(detail=False, methods=['get'])
    def settle(self, request):
        token_ids = Token.objects.settle_list()
        return Response(token_ids)


class ExchangeViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=RESPONSE_STR)
    def list(self, request):
        exchange_names = Exchange.objects.name_list()
        return Response(exchange_names)


class SummaryView(APIView):
    @extend_schema(responses=RESPONSE_SUMMARY)
    def get(self, request):
        exchanges_count = Exchange.objects.values('name').distinct().count()
        symbols_count = Symbol.objects.count()
        deals_profit_count = ArbitrageData.latest.filter(
            margin__gt=0.5,
            margin__lt=100
        ).count()
        uptime = ArbitrageData.latest.uptime()
        data = {
            'exchanges': exchanges_count,
            'symbols': symbols_count,
            'profit_deals': deals_profit_count,
            'uptime': uptime
        }
        return Response(data)
