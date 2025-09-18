from django import template

register = template.Library()

@register.filter
def filter_current(forecasts, period):
    """Filter forecasts to get the current one for a specific period."""
    current_forecast = forecasts.filter(period=period, is_current=True).first()
    return current_forecast 