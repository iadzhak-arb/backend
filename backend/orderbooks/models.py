from django.db import models
from django.urls import reverse
from django.utils.http import urlencode

from .managers import ArbitrageManager, LatestArbitrageManager


class Exchange(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField()

    def __str__(self) -> str:
        return self.name


class Token(models.Model):
    id = models.CharField(primary_key=True)

    def __str__(self) -> str:
        return self.id


class Market(models.Model):
    id = models.CharField(primary_key=True)

    def __str__(self) -> str:
        return self.id


class Symbol(models.Model):
    id = models.CharField(primary_key=True)
    market = models.ForeignKey(
        Market,
        on_delete=models.CASCADE
    )
    base = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        related_name='+'
    )
    quote = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        related_name='+'
    )
    settle = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='+'
    )

    def __str__(self) -> str:
        return self.id


class Orderbook(models.Model):
    symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
    )
    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField()
    asks = models.JSONField()
    bids = models.JSONField()

    class Meta:
        unique_together = ('symbol', 'exchange', 'timestamp')

    def __str__(self) -> str:
        return f'{self.timestamp} {self.exchange} {self.symbol}'

    @property
    def name(self) -> str:
        return f'{self.exchange} {self.symbol}'


class Arbitrage(models.Model):
    pk = models.CompositePrimaryKey('buy_exchange', 'buy_symbol', 'sell_exchange', 'sell_symbol', 'timestamp')
    buy_exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name='+'
    )
    buy_symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        related_name='+'
    )
    sell_exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name='+'
    )
    sell_symbol = models.ForeignKey(
        Symbol,
        on_delete=models.CASCADE,
        related_name='+'
    )
    timestamp = models.DateTimeField()
    margin = models.FloatField()
    volume_base = models.FloatField()
    volume_quote = models.FloatField()

    objects = ArbitrageManager()
    latest = LatestArbitrageManager()

    def __str__(self) -> str:
        return f'{self.buy_exchange} {self.buy_symbol} - {self.sell_exchange} {self.sell_symbol}: {self.margin}%'

    def history_url(self) -> str:
        params = {
            'buy_exchange': self.buy_exchange,
            'buy_symbol': self.buy_symbol,
            'sell_exchange': self.sell_exchange,
            'sell_symbol': self.sell_symbol
        }
        url = reverse('history')
        return url + '?' + urlencode(params)
