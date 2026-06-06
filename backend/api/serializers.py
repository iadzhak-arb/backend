from rest_framework import serializers

from orderbooks.models import Arbitrage, ArbitrageData


class ArbitrageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrageData
        fields = '__all__'
