from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from forecasts.models import Forecast, Ticker


class ForecastCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="analyst", password="pass1234")
        self.ticker = Ticker.objects.create(ticker="AAPL", name="Apple Inc.")

    def test_login_required(self):
        response = self.client.get(reverse("forecast-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_get_initial_ignores_invalid_ticker(self):
        self.client.login(username="analyst", password="pass1234")

        response = self.client.get(reverse("forecast-create") + "?ticker=invalid&period=3M")

        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIsNone(form["ticker"].value())
        self.assertEqual(form["period"].value(), "3M")

    def test_post_demotes_previous_current_forecast(self):
        self.client.login(username="analyst", password="pass1234")

        previous = Forecast.objects.create(
            ticker=self.ticker,
            analyst=self.user,
            period="1M",
            direction=1.25,
            view="Original forecast",
            is_current=True,
        )

        response = self.client.post(
            reverse("forecast-create"),
            {
                "ticker": self.ticker.id,
                "period": "1M",
                "direction": 1.5,
                "view": "Updated view",
            },
        )

        self.assertRedirects(response, "/")
        previous.refresh_from_db()
        self.assertFalse(previous.is_current)

        latest = Forecast.objects.exclude(pk=previous.pk).get()
        self.assertEqual(latest.analyst, self.user)
        self.assertTrue(latest.is_current)


class ForecastHistoryViewTests(TestCase):
    def setUp(self):
        self.ticker = Ticker.objects.create(ticker="AAPL", name="Apple Inc.")
        self.other_ticker = Ticker.objects.create(ticker="MSFT", name="Microsoft")
        self.analyst = User.objects.create_user(username="regular", password="pass1234")
        self.staff = User.objects.create_user(username="staff", password="pass1234", is_staff=True)

    def test_redirects_anonymous_users_to_login(self):
        response = self.client.get(reverse("forecast-history"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_denies_non_staff_users(self):
        self.client.login(username="regular", password="pass1234")

        response = self.client.get(reverse("forecast-history"))

        self.assertEqual(response.status_code, 403)

    def test_staff_can_filter_by_ticker_period_and_status(self):
        current = Forecast.objects.create(
            ticker=self.ticker,
            analyst=self.staff,
            period="1M",
            direction=2.5,
            view="Bullish",
            is_current=True,
        )
        Forecast.objects.create(
            ticker=self.other_ticker,
            analyst=self.staff,
            period="3M",
            direction=1.1,
            view="Different ticker",
            is_current=False,
        )

        self.client.login(username="staff", password="pass1234")

        response = self.client.get(
            reverse("forecast-history"),
            {
                "ticker": str(self.ticker.id),
                "period": "1M",
                "is_current": "true",
            },
        )

        self.assertEqual(response.status_code, 200)
        objects = list(response.context["object_list"])
        self.assertEqual(objects, [current])
        self.assertContains(response, self.ticker.ticker)


class AuthenticationViewsTests(TestCase):
    def test_login_page_renders(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
