from decimal import Decimal
from typing import Iterator

book = list[list[float]]  # [[price, amount], ...]


def get_next_price_and_volume(iterator: Iterator[list[float]]) -> tuple[Decimal, Decimal]:
    try:
        price, volume, *_ = next(iterator)
        price = Decimal(str(price))
        volume = Decimal(str(volume))
    except StopIteration:
        price = Decimal('0')
        volume = Decimal('0')
    return price, volume


def calculate_max_arbitrage(asks: book, bids: book) -> tuple[float, float, float]:
    """asks - to buy, bids - to sell."""
    if not asks or not bids:
        raise ValueError('Empty order books.')
    asks_iter = iter(asks)
    bids_iter = iter(bids)

    ask_price, ask_volume = get_next_price_and_volume(asks_iter)
    bid_price, bid_volume = get_next_price_and_volume(bids_iter)

    total_buy_cost = total_sell_cost = Decimal('0')
    total_buy_volume = total_sell_volume = Decimal('0')

    best_profit = Decimal('-Infinity')
    margin = volume_base = volume_quote = 0

    while True:
        take = min(ask_volume, bid_volume)

        ask_volume -= take
        total_buy_volume += take
        total_buy_cost += take * ask_price

        if ask_volume == 0:
            ask_price, ask_volume = get_next_price_and_volume(asks_iter)

        bid_volume -= take
        total_sell_volume += take
        total_sell_cost += take * bid_price

        if bid_volume == 0:
            bid_price, bid_volume = get_next_price_and_volume(bids_iter)

        if total_buy_volume != total_sell_volume:
            raise ValueError('Volumes are different.')

        profit = total_sell_cost - total_buy_cost

        if profit > best_profit:
            best_profit = profit
            margin = float(round((profit / total_buy_cost) * 100, 2))
            volume_base = float(total_buy_volume)
            volume_quote = float(max(total_buy_cost, total_sell_cost))

        if ask_price == 0 or bid_price == 0:
            break

    return margin, volume_base, volume_quote
