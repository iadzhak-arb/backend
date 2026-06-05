import pytest

from orderbooks.utils import calculate_max_arbitrage, get_next_price_and_volume


class TestCalculateMaxArbitrage:
    @pytest.mark.parametrize(
        'asks, bids, expected',
        (
                (
                        [[100, 1, 3], [200, 1]], [[100, 1], [80, 1]], (0, 1, 100)
                ),
                (
                        [[100, 2], [150, 1]], [[110, 1, 2], [100, 1]], (10, 1, 110)
                ),
                (
                        [[100, 1], [150, 1]], [[90, 1], [80, 1]], (-10, 1, 100)
                ),
        ),
        ids=('eq', 'asc', 'desc')
    )
    def test_valid(self, asks, bids, expected):
        assert calculate_max_arbitrage(asks, bids) == expected

    def test_empty(self):
        with pytest.raises(ValueError):
            calculate_max_arbitrage([], [])
        with pytest.raises(ValueError):
            calculate_max_arbitrage([[1, 2]], [])


class TestGetNextPriceAndVolume:
    def test_valid(self):
        expected = [[100, 1, 3], [200, 1]]
        iterator = iter(expected)
        p, v = get_next_price_and_volume(iterator)
        assert p, v == expected[0][:2]
        p, v = get_next_price_and_volume(iterator)
        assert p, v == expected[1][:2]
        p, v = get_next_price_and_volume(iterator)
        assert p == 0
        assert v == 0

    def test_empty(self):
        iterator = iter([])
        p, v = get_next_price_and_volume(iterator)
        assert p == 0
        assert v == 0
