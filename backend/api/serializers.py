from rest_framework import serializers

from orderbooks.models import Arbitrage


class ArbitrageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arbitrage
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Arbitrage
        fields = ('timestamp', 'margin')
