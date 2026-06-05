import datetime as dt
import logging
from unittest import mock

import pytest

from orderbooks.models import Orderbook, Arbitrage
from orderbooks.consumers import handle_orderbooks
from orderbooks.dto import ExchangeDTO, SymbolDTO, OrderbookDTO


@pytest.mark.django_db
def test_handle_orderbooks():
    logger = mock.create_autospec(logging.getLogger())
    Orderbook.objects.all().delete()
    Arbitrage.objects.all().delete()

    mock_timestamp = dt.datetime.now().timestamp()
    mock_exchange = ExchangeDTO(id='test', name='Test')
    mock_symbol = SymbolDTO(id='BTC/USDT', market='spot', base='BTC', quote='USDT', settle=None)
    mock_orderbook = OrderbookDTO(
        symbol=mock_symbol, exchange=mock_exchange, timestamp=mock_timestamp, asks=[[100., 1.]], bids=[[90., 1.]])
    mock_data = [mock_orderbook]

    handle_orderbooks(mock_data, logger)

    assert Orderbook.objects.count() == 1
    ob = Orderbook.objects.select_related('symbol', 'exchange').get()
    assert ob.symbol.id == mock_symbol.id
    assert ob.exchange.id == mock_exchange.id
    assert ob.exchange.name == mock_exchange.name
    assert ob.timestamp.timestamp() == mock_timestamp
    assert ob.asks == mock_orderbook.asks
    assert ob.bids == mock_orderbook.bids

    assert Arbitrage.objects.count() == 1
    arb = Arbitrage.objects.get()
    assert arb.buy_exchange == ob.exchange
    assert arb.buy_symbol == ob.symbol
    assert arb.sell_exchange == ob.exchange
    assert arb.sell_symbol == ob.symbol
    assert arb.timestamp == ob.timestamp
    assert arb.margin == -10
    assert arb.volume_base == 1
    assert arb.volume_quote == 100
