from django.db import models


class StockData(models.Model):
    date = models.DateTimeField()
    open = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    dividends = models.FloatField()
    stock_splits = models.FloatField()
    tag = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ml_app_stockdata'


class MLAccuracy(models.Model):
    metrics = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Metrics: {self.metrics}% ({self.timestamp})"


class InputData(models.Model):
    open = models.FloatField(default=0.0)
    low = models.FloatField(default=0.0)
    high = models.FloatField(default=0.0)
    close = models.FloatField(default=0.0)
    volume = models.IntegerField(default=0)
    dividends = models.FloatField(default=0.0)
    stock_splits = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.open}, {self.low}, {self.high}, {self.close}, {self.volume}, {self.dividends}, {self.stock_splits}"
