from rest_framework import serializers

from orderbooks.models import Arbitrage, ArbitrageData, Orderbook, Market


class OrderbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderbook
        fields = ('exchange', 'symbol')


class ArbitrageDataSerializer(serializers.ModelSerializer):
    buy = OrderbookSerializer(source='arbitrage.ob_buy')
    sell = OrderbookSerializer(source='arbitrage.ob_sell')
    arbitrage = serializers.SerializerMethodField()

    class Meta:
        model = ArbitrageData
        fields = ('arbitrage', 'buy', 'sell', 'margin', 'timestamp')

    def get_arbitrage(self, obj):
        return {
            'open_id': getattr(obj, 'open_id', None),
            'close_id': getattr(obj, 'close_id', None),
        }


class ArbitrageHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageData
        fields = ('timestamp', 'margin')


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('id',)
