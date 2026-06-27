from django.db import models
from django.db.models import Window, Subquery, OuterRef, F
from django.db.models.functions import RowNumber


class LatestArbitrageDataManager(models.Manager):
    def get_queryset(self):
        from .models import Arbitrage
        qs = super().get_queryset()
        window = Window(
            expression=RowNumber(),
            partition_by=models.F('arbitrage'),
            order_by=models.F('timestamp').desc()
        )
        qs = qs.annotate(row_num=window).filter(row_num=1)
        subquery = Subquery(
            Arbitrage.objects.filter(
                ob_buy=OuterRef('arbitrage__ob_sell'),
                ob_sell=OuterRef('arbitrage__ob_buy'),
            ).values('id')
        )
        qs = qs.select_related(
            'arbitrage__ob_buy__symbol',
            'arbitrage__ob_buy__exchange',
            'arbitrage__ob_sell__symbol',
            'arbitrage__ob_sell__exchange',
        ).annotate(
            open_id=F('arbitrage__id'),
            close_id=subquery
        )
        return qs
