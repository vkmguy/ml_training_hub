from rest_framework import serializers

from .models import StockData, MLAccuracy


class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = '__all__'


class MLAccuracySerializer(serializers.ModelSerializer):
    class Meta:
        model = MLAccuracy
        fields = ['metrics', 'timestamp']
