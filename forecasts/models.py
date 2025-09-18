from django.db import models
from django.contrib.auth.models import User

class Ticker(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ticker} - {self.name}"

class Forecast(models.Model):
    PERIOD_CHOICES = [
        ("1M", "1 Month"),
        ("3M", "3 Months"),
        ("12M", "12 Months"),
    ]
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    analyst = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=3, choices=PERIOD_CHOICES)
    direction = models.FloatField(help_text="Predicted EPS (can be positive or negative)")
    view = models.TextField(blank=True)  # Optional detailed view
    is_current = models.BooleanField(default=True, help_text="Is this the latest forecast for this analyst/ticker/period?")
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{str(self.ticker)} ({self.period}) by {str(self.analyst)} at {self.updated_at} EPS: {self.direction}"
