from django.db import models


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

    class Meta:
        unique_together = ('symbol', 'exchange')

    def __str__(self) -> str:
        return f'{self.exchange} {self.symbol}'


class OrderbookData(models.Model):
    orderbook = models.ForeignKey(
        Orderbook,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField()
    asks = models.JSONField()
    bids = models.JSONField()

    class Meta:
        unique_together = ('orderbook', 'timestamp')

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

    class Meta:
        unique_together = ('ob_buy', 'ob_sell')

    def __str__(self) -> str:
        return f'Buy:{self.ob_buy} | Sell: {self.ob_sell}'


class ArbitrageData(models.Model):
    arbitrage = models.ForeignKey(
        Arbitrage,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField()
    margin = models.FloatField()
    volume_base = models.FloatField()
    volume_quote = models.FloatField()
