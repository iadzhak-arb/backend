from rest_framework import serializers

from orderbooks.models import Arbitrage, ArbitrageData, Orderbook, Market, Token, Exchange


class OrderbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderbook
        fields = ('exchange', 'symbol')


class ArbitrageDataSerializer(serializers.ModelSerializer):
    buy = OrderbookSerializer(source='arbitrage.ob_buy')
    sell = OrderbookSerializer(source='arbitrage.ob_sell')
    id = serializers.IntegerField(source='arbitrage.id')

    class Meta:
        model = ArbitrageData
        fields = ('id', 'buy', 'sell', 'margin', 'volume_base', 'volume_quote', 'timestamp')


class ArbitrageHistoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageData
        fields = ('timestamp', 'margin')


class ArbitrageSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Arbitrage
        fields = ('id', 'name',)


class ArbitrageRetrieveSerializer(ArbitrageSerializer):
    history = ArbitrageHistoryDataSerializer(many=True)

    class Meta:
        model = Arbitrage
        fields = ('id', 'name', 'history')
