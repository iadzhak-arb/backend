import datetime as dt
import logging
from unittest import mock

import pytest

from orderbooks.models import Orderbook, Arbitrage, OrderbookData, ArbitrageData
from orderbooks.consumers import handle_orderbooks
from orderbooks.dto import ExchangeDTO, SymbolDTO, OrderbookDTO


@pytest.mark.django_db
def test_handle_orderbooks():
    logger = mock.create_autospec(logging.getLogger())
    Orderbook.objects.all().delete()
    OrderbookData.objects.all().delete()
    Arbitrage.objects.all().delete()

    mock_timestamp = dt.datetime.now().timestamp()
    mock_exchange = ExchangeDTO(id='test', name='Test')
    mock_symbol = SymbolDTO(id='BTC/USDT', market='spot', base='BTC', quote='USDT', settle=None)
    mock_orderbook = OrderbookDTO(
        symbol=mock_symbol, exchange=mock_exchange, timestamp=mock_timestamp, asks=[[100., 1.]], bids=[[90., 1.]])
    mock_data = [mock_orderbook]

    handle_orderbooks(mock_data, logger)

    assert Orderbook.objects.count() == 1
    ob = Orderbook.objects.get()
    assert ob.symbol.id == mock_symbol.id
    assert ob.exchange.id == mock_exchange.id
    assert ob.exchange.name == mock_exchange.name
    assert OrderbookData.objects.count() == 1
    ob_data = OrderbookData.objects.get()
    assert ob_data.orderbook == ob
    assert ob_data.timestamp.timestamp() == mock_timestamp
    assert ob_data.asks == mock_orderbook.asks
    assert ob_data.bids == mock_orderbook.bids

    assert Arbitrage.objects.count() == 1
    arb = Arbitrage.objects.get()
    assert arb.ob_buy == ob
    assert arb.ob_sell == ob
    assert ArbitrageData.objects.count() == 1
    arb_data = ArbitrageData.objects.get()
    assert arb_data.arbitrage == arb
    assert arb_data.timestamp == ob_data.timestamp
    assert arb_data.margin == -10
    assert arb_data.volume_base == 1
    assert arb_data.volume_quote == 100
