from django.db import models
from django.db.models import OuterRef, Subquery, Window
from django.db.models.functions import RowNumber


class LatestArbitrageDataManager(models.Manager):
    def get_queryset(self):
        window = Window(
            expression=RowNumber(),
            partition_by=models.F('arbitrage'),
            order_by=models.F('timestamp').desc()
        )
        return (
            super().get_queryset()
            .annotate(row_num=window)
            .filter(row_num=1)
        )
