"""
URL configuration for stock_forecast_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.views.generic import TemplateView
from forecasts.views import TickerListView, ForecastCreateView, ForecastHistoryView
import markdown
import os

def readme_view(request):
    """Serve README.md as formatted HTML"""
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        html = markdown.markdown(content)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stock Forecast App - README</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
                h1, h2, h3 {{ color: #333; }}
                code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                .nav {{ margin-bottom: 30px; }}
                .nav a {{ margin-right: 15px; }}
            </style>
        </head>
        <body>
            <div class="nav">
                <a href="/">← Back to App</a>
                <a href="/admin/">Admin Panel</a>
                <a href="/forecast/history/">Forecast History</a>
            </div>
            {html}
        </body>
        </html>
        """
        return HttpResponse(html_content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("README.md not found", status=404, content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TickerListView.as_view(), name='ticker-list'),
    path('forecast/new/', ForecastCreateView.as_view(), name='forecast-create'),
    path('forecast/history/', ForecastHistoryView.as_view(), name='forecast-history'),
    path('readme/', readme_view, name='readme'),
]
