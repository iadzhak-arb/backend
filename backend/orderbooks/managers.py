from datetime import timedelta

from django.db import models
from django.db.models import Window, Subquery, OuterRef, F, Value, Prefetch
from django.db.models.functions import RowNumber, Concat
from django.utils import timezone


class ArbitrageDataLatestManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        window = Window(
            expression=RowNumber(),
            partition_by=models.F('arbitrage'),
            order_by=models.F('timestamp').desc()
        )
        qs = qs.annotate(row_num=window).filter(row_num=1)
        qs = qs.select_related(
            'arbitrage__ob_buy__symbol',
            'arbitrage__ob_buy__exchange',
            'arbitrage__ob_sell__symbol',
            'arbitrage__ob_sell__exchange',
        )
        return qs

    def by_time(self, delta: timedelta):
        return self.get_queryset().filter(
            timestamp__gte=timezone.now() - delta
        )

    def demo(
            self,
            market_buy: str,
            market_sell: str,
            margin_gte: float = 0.01,
            margin_lte: float = 0.5,
            size: int = 10
    ):
        return self.get_queryset().filter(
            arbitrage__ob_buy__symbol__market__id=market_buy,
            arbitrage__ob_sell__symbol__market__id=market_sell,
            margin__gte=margin_gte,
            margin__lte=margin_lte
        ).order_by('-margin', '-timestamp')[:size]


class ArbitrageManager(models.Manager):
    def with_name(self):
        return self.get_queryset().annotate(
            name=Concat(
                F('ob_buy__symbol'),
                Value(' '),
                F('ob_buy__exchange'),
                Value(' - '),
                F('ob_sell__symbol'),
                Value(' '),
                F('ob_sell__exchange')
            ),
        )

    def with_history(self):
        return self.with_name().prefetch_related('history')


class ExchangeManager(models.Manager):
    def name_list(self):
        return self.get_queryset().values_list(
            'name', flat=True
        ).distinct()


class TokenManager(models.Manager):

    def all_list(self):
        return self.get_queryset().values_list('id', flat=True)

    def base_list(self):
        return self.get_queryset().filter(
            symbol_base__isnull=False
        ).values_list('id', flat=True).distinct()

    def quote_list(self):
        return self.get_queryset().filter(
            symbol_quote__isnull=False
        ).values_list('id', flat=True).distinct()

    def settle_list(self):
        return self.get_queryset().filter(
            symbol_settle__isnull=False
        ).values_list('id', flat=True).distinct()
