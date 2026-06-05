import datetime as dt
import itertools

from django.db import transaction
from django.utils import timezone
from django.conf import settings
from faststream import Logger
from faststream.rabbit import RabbitRouter, RabbitQueue

from .dto import OrderbookDTO
from .models import Exchange, Token, Symbol, Market, Orderbook, Arbitrage
from .utils import calculate_max_arbitrage

router = RabbitRouter()
queue = RabbitQueue(settings.QUEUE_ORDERBOOKS, durable=True)


@router.subscriber(queue)
def handle_orderbooks(data: list[OrderbookDTO], logger: Logger):
    # Save orderbooks data
    orderbooks = []
    for d in data:
        base, _ = Token.objects.get_or_create(id=d.symbol.base)
        quote, _ = Token.objects.get_or_create(id=d.symbol.base)
        if d.symbol.settle:
            settle, _ = Token.objects.get_or_create(id=d.symbol.settle)
        else:
            settle = None
        market, _ = Market.objects.get_or_create(id=d.symbol.market)
        symbol, _ = Symbol.objects.get_or_create(
            id=d.symbol.id,
            market=market,
            base=base,
            quote=quote,
            settle=settle
        )
        exchange, _ = Exchange.objects.get_or_create(
            id=d.exchange.id,
            name=d.exchange.name
        )
        timestamp = dt.datetime.fromtimestamp(
            d.timestamp,
            tz=timezone.get_default_timezone()
        )
        orderbooks.append(
            Orderbook(
                symbol=symbol,
                exchange=exchange,
                timestamp=timestamp,
                asks=d.asks,
                bids=d.bids)
        )
    with transaction.atomic():
        Orderbook.objects.bulk_create(orderbooks, ignore_conflicts=True)
    logger.info(f'Proceeded {len(orderbooks)} new orderbooks.')
    # Calculate arbitrage
    arbitrages = []
    for ob_buy, ob_sell in itertools.product(orderbooks, repeat=2):
        try:
            result = calculate_max_arbitrage(ob_buy.asks, ob_sell.bids)
        except ValueError:
            continue
        margin, volume_base, volume_quote = result
        arbitrages.append(
            Arbitrage(
                buy_exchange=ob_buy.exchange,
                buy_symbol=ob_buy.symbol,
                sell_exchange=ob_sell.exchange,
                sell_symbol=ob_sell.symbol,
                timestamp=min(ob_buy.timestamp, ob_sell.timestamp),
                margin=margin,
                volume_base=volume_base,
                volume_quote=volume_quote
            )
        )
    with transaction.atomic():
        Arbitrage.objects.bulk_create(arbitrages, ignore_conflicts=True)

    logger.info(f'Proceeded {len(arbitrages)} new arbitrages.')
