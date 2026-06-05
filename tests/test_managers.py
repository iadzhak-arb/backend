import datetime as dt

import pytest
from django.utils import timezone

from orderbooks.models import Arbitrage, Symbol, Market, Token, Exchange


@pytest.mark.django_db
def test_latest_arbitrage_manager():
    t2 = timezone.now()
    t1 = t2 - dt.timedelta(minutes=5)
    exchange = Exchange.objects.create(id='e', name='E')
    symbol = Symbol.objects.create(
        id='A/B',
        base=Token.objects.create(id='A'),
        quote=Token.objects.create(id='B'),
        market=Market.objects.create(id='m')
    )

    Arbitrage.objects.all().delete()

    arb1 = Arbitrage.objects.create(
        buy_exchange=exchange,
        buy_symbol=symbol,
        sell_exchange=exchange,
        sell_symbol=symbol,
        timestamp=t1,
        margin=0,
        volume_base=0,
        volume_quote=0,
    )
    arb2 = Arbitrage.objects.create(
        buy_exchange=exchange,
        buy_symbol=symbol,
        sell_exchange=exchange,
        sell_symbol=symbol,
        timestamp=t2,
        margin=0,
        volume_base=0,
        volume_quote=0,
    )

    all_arb = Arbitrage.objects.all().order_by('timestamp')
    assert len(all_arb) == 2
    assert arb1.timestamp == all_arb[0].timestamp
    assert arb2.timestamp == all_arb[1].timestamp

    latest_arb = Arbitrage.latest.all()
    assert len(latest_arb) == 1
    assert arb2.timestamp == latest_arb[0].timestamp
