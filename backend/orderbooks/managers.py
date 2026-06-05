from django.db import models
from django.db.models.functions import RowNumber


class ArbitrageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('buy_symbol', 'sell_symbol', 'buy_exchange', 'sell_exchange')


class LatestArbitrageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            row_number=models.Window(
                expression=RowNumber(),
                partition_by=[
                    'buy_exchange',
                    'buy_symbol',
                    'sell_exchange',
                    'sell_symbol'
                ],
                order_by=models.F('timestamp').desc()
            )
        ).select_related('buy_symbol', 'sell_symbol', 'buy_exchange', 'sell_exchange').filter(row_number=1)
