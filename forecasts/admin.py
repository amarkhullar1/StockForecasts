from django.contrib import admin
from .models import Ticker, Forecast

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name')
    search_fields = ('ticker', 'name')

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'analyst', 'period', 'direction', 'updated_at')
    list_filter = ('period', 'ticker')
    search_fields = ('ticker__ticker', 'ticker__name', 'analyst__username')
