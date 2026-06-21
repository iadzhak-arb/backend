from rest_framework import serializers

from orderbooks.models import Arbitrage, ArbitrageData, Orderbook, Market


class OrderbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderbook
        fields = ('exchange', 'symbol')


class ArbitrageDataSerializer(serializers.ModelSerializer):
    buy = OrderbookSerializer(source='arbitrage.ob_buy')
    sell = OrderbookSerializer(source='arbitrage.ob_sell')

    class Meta:
        model = ArbitrageData
        fields = ('arbitrage', 'buy', 'sell', 'margin', 'timestamp')


class ArbitrageHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageData
        fields = ('arbitrage', 'timestamp', 'margin')


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ('id',)
