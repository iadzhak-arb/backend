import datetime as dt
import itertools
import functools

from django.db import transaction, IntegrityError
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from faststream import Logger
from faststream.rabbit import RabbitRouter, RabbitQueue

from .dto import OrderbookDTO, ExchangeDTO, SymbolDTO
from .models import Exchange, Token, Symbol, Market, Orderbook, Arbitrage, OrderbookData, ArbitrageData
from .utils import calculate_max_arbitrage

router = RabbitRouter()
queue = RabbitQueue(settings.QUEUE_ORDERBOOKS, durable=True)


@functools.lru_cache(maxsize=10)
def get_token(t: str) -> Token:
    token, _ = Token.objects.get_or_create(id=t)
    return token


@functools.lru_cache(maxsize=5)
def get_market(m: str) -> Market:
    market, _ = Market.objects.get_or_create(id=m)
    return market


@functools.lru_cache(maxsize=5)
def get_symbol(id: str, market: str, base: str, quote: str, settle: str | None) -> Symbol:
    try:
        symbol = Symbol.objects.get(id=id)
    except ObjectDoesNotExist:
        try:
            symbol = Symbol.objects.create(
                id=id,
                market=get_market(market),
                base=get_token(base),
                quote=get_token(quote),
                settle=get_token(settle) if settle else None,
            )
        except IntegrityError:
            symbol = Symbol.objects.get(id=id)
    return symbol


@functools.lru_cache(maxsize=7)
def get_exchange(id: str, name: str) -> Exchange:
    exchange, _ = Exchange.objects.get_or_create(id=id, defaults={'name': name})
    return exchange


def get_orderbook(ob: OrderbookDTO) -> Orderbook:
    try:
        orderbook = Orderbook.objects.get(
            symbol__id=ob.symbol.id,
            exchange__id=ob.exchange.id,
        )
    except ObjectDoesNotExist:
        symbol = get_symbol(**ob.symbol.model_dump())
        exchange = get_exchange(**ob.exchange.model_dump())
        try:
            orderbook = Orderbook.objects.create(
                symbol=symbol,
                exchange=exchange
            )
        except IntegrityError:
            orderbook = Orderbook.objects.get(
                symbol=symbol,
                exchange=exchange
            )
    return orderbook


@router.subscriber(queue)
def handle_orderbooks(data: list[OrderbookDTO], logger: Logger):
    # Save orderbooks data
    orderbooks_data = []
    for d in data:
        orderbook = get_orderbook(d)
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
    arbitrage_data = []
    for ob_buy, ob_sell in itertools.product(orderbooks_data, repeat=2):
        try:
            result = calculate_max_arbitrage(ob_buy.asks, ob_sell.bids)
        except ValueError:
            continue
        margin, volume_base, volume_quote = result
        arbitrage, _ = Arbitrage.objects.get_or_create(
            ob_buy=ob_buy.orderbook,
            ob_sell=ob_sell.orderbook,
        )
        arbitrage_data.append(
            ArbitrageData(
                arbitrage=arbitrage,
                timestamp=min(ob_buy.timestamp, ob_sell.timestamp),
                margin=margin,
                volume_base=volume_base,
                volume_quote=volume_quote
            )
        )
    with transaction.atomic():
        ArbitrageData.objects.bulk_create(arbitrage_data, ignore_conflicts=True)

    logger.info(f'Proceeded {len(arbitrage_data)} new arbitrages.')
