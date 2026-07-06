from django.db import models

from .managers import ArbitrageDataLatestManager, ArbitrageManager, TokenManager, ExchangeManager


class Exchange(models.Model):
    id = models.CharField(primary_key=True)
    name = models.CharField()

    objects = ExchangeManager()

    def __str__(self) -> str:
        return self.name


class Token(models.Model):
    id = models.CharField(primary_key=True)

    objects = TokenManager()

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
        related_name='symbol_base'
    )
    quote = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        related_name='symbol_quote'
    )
    settle = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='symbol_settle'
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

    class Meta:
        unique_together = ('symbol', 'exchange')

    def __str__(self) -> str:
        return f'{self.exchange} {self.symbol}'


class OrderbookData(models.Model):
    pk = models.CompositePrimaryKey('orderbook_id', 'timestamp')
    orderbook = models.ForeignKey(
        Orderbook,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField()
    asks = models.JSONField()
    bids = models.JSONField()

    def __str__(self) -> str:
        return f'{self.timestamp} {self.orderbook}'


class Arbitrage(models.Model):
    ob_buy = models.ForeignKey(
        Orderbook,
        on_delete=models.CASCADE,
        related_name='+',
    )
    ob_sell = models.ForeignKey(
        Orderbook,
        on_delete=models.CASCADE,
        related_name='+',
    )

    objects = ArbitrageManager()

    class Meta:
        unique_together = ('ob_buy', 'ob_sell')

    def __str__(self) -> str:
        return f'Buy:{self.ob_buy} | Sell: {self.ob_sell}'


class ArbitrageData(models.Model):
    arbitrage = models.ForeignKey(
        Arbitrage,
        on_delete=models.CASCADE,
        related_name='history'
    )
    timestamp = models.DateTimeField()
    margin = models.FloatField()
    volume_base = models.FloatField()
    volume_quote = models.FloatField()
    pk = models.CompositePrimaryKey('arbitrage_id', 'timestamp')

    objects = models.Manager()
    latest = ArbitrageDataLatestManager()
