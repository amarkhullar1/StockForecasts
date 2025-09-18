from django.contrib.auth.models import User
from django.test import TestCase

from forecasts.models import Forecast, Ticker
from forecasts.templatetags.forecast_filters import filter_current


class FilterCurrentTests(TestCase):
    def setUp(self):
        self.ticker = Ticker.objects.create(ticker="AAPL", name="Apple Inc.")
        self.user = User.objects.create_user(username="analyst", password="pass1234")

    def test_returns_current_forecast_for_period(self):
        Forecast.objects.create(
            ticker=self.ticker,
            analyst=self.user,
            period="1M",
            direction=1.0,
            view="Old",
            is_current=False,
        )
        current = Forecast.objects.create(
            ticker=self.ticker,
            analyst=self.user,
            period="1M",
            direction=1.5,
            view="Current",
            is_current=True,
        )

        result = filter_current(self.ticker.forecast_set.all(), "1M")

        self.assertEqual(result, current)

    def test_returns_none_when_no_current_forecast(self):
        Forecast.objects.create(
            ticker=self.ticker,
            analyst=self.user,
            period="3M",
            direction=0.5,
            view="Historic",
            is_current=False,
        )

        result = filter_current(self.ticker.forecast_set.all(), "3M")

        self.assertIsNone(result)
