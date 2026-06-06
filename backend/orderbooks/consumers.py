import datetime as dt
import itertools

from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from faststream import Logger
from faststream.rabbit import RabbitRouter, RabbitQueue
from faststream.rabbit.schemas import exchange

from .dto import OrderbookDTO, ExchangeDTO, SymbolDTO
from .models import Exchange, Token, Symbol, Market, Orderbook, Arbitrage, OrderbookData
from .utils import calculate_max_arbitrage

router = RabbitRouter()
queue = RabbitQueue(settings.QUEUE_ORDERBOOKS, durable=True)


@router.subscriber(queue)
def handle_orderbooks(data: list[OrderbookDTO], logger: Logger):
    # Save orderbooks data
    orderbooks_data = []
    for d in data:
        try:
            orderbook = Orderbook.objects.get(
                symbol__id=d.symbol.id,
                exchange__id=d.exchange.id,
            )
        except ObjectDoesNotExist:
            try:
                symbol = Symbol.objects.get(id=d.symbol.id)
            except ObjectDoesNotExist:
                symbol, _ = Symbol.objects.get_or_create(
                    id=d.symbol.id,
                    defaults={
                        'base': Token.objects.get_or_create(id=d.symbol.base)[0],
                        'quote': Token.objects.get_or_create(id=d.symbol.quote)[0],
                        'settle': Token.objects.get_or_create(id=d.symbol.settle)[0] if d.symbol.settle else None,
                        'market': Market.objects.get_or_create(id=d.symbol.market)[0]
                    }
                )
            exchange, _ = Exchange.objects.get_or_create(
                id=d.exchange.id,
                defaults={
                    'name': d.exchange.name,
                }
            )
            orderbook, _ = Orderbook.objects.get_or_create(
                symbol=symbol,
                exchange=exchange,
            )
        timestamp = dt.datetime.fromtimestamp(
            d.timestamp,
            tz=timezone.get_default_timezone()
        )
        orderbooks_data.append(
            OrderbookData(
                orderbook=orderbook,
                timestamp=timestamp,
                asks=d.asks,
                bids=d.bids)
        )
    with transaction.atomic():
        OrderbookData.objects.bulk_create(orderbooks_data, ignore_conflicts=True)
    logger.info(f'Proceeded {len(orderbooks_data)} new orderbooks.')
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
