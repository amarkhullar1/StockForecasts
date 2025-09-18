from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from .models import Ticker, Forecast

# Create your views here.

class TickerListView(ListView):
    model = Ticker
    template_name = 'forecasts/ticker_list.html'
    context_object_name = 'tickers'
    
    def get_queryset(self):
        queryset = Ticker.objects.all()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(ticker__icontains=search_query) | 
                Q(name__icontains=search_query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['periods'] = ['1M', '3M', '12M']
        return context

class ForecastCreateView(LoginRequiredMixin, CreateView):
    model = Forecast
    template_name = 'forecasts/forecast_form.html'
    fields = ['ticker', 'period', 'direction', 'view']
    
    def get_initial(self):
        initial = super().get_initial()
        # Prepopulate ticker and period from URL parameters
        ticker_id = self.request.GET.get('ticker')
        period = self.request.GET.get('period')
        
        if ticker_id:
            try:
                ticker = Ticker.objects.get(id=ticker_id)
                initial['ticker'] = ticker
            except Ticker.DoesNotExist:
                pass
        
        if period:
            initial['period'] = period
            
        return initial
    
    def form_valid(self, form):
        form.instance.analyst = self.request.user
        
        # Mark previous forecasts for this analyst/ticker/period as historic
        Forecast.objects.filter(
            analyst=self.request.user,
            ticker=form.instance.ticker,
            period=form.instance.period,
            is_current=True
        ).update(is_current=False)
        
        form.instance.is_current = True
        messages.success(self.request, 'Forecast submitted successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return '/'

class ForecastHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Forecast
    template_name = 'forecasts/forecast_history.html'
    context_object_name = 'forecasts'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        queryset = Forecast.objects.all().select_related('ticker', 'analyst')
        
        # Filter by ticker if provided
        ticker_id = self.request.GET.get('ticker')
        if ticker_id:
            queryset = queryset.filter(ticker_id=ticker_id)
        
        # Filter by period if provided
        period = self.request.GET.get('period')
        if period:
            queryset = queryset.filter(period=period)
        
        # Filter by analyst if provided
        analyst = self.request.GET.get('analyst')
        if analyst:
            queryset = queryset.filter(analyst__username__icontains=analyst)
        
        # Filter by current/historic if provided
        is_current = self.request.GET.get('is_current')
        if is_current in ['true', 'false']:
            queryset = queryset.filter(is_current=(is_current == 'true'))
        
        return queryset.order_by('-updated_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tickers'] = Ticker.objects.all()
        context['periods'] = ['1M', '3M', '12M']
        return context
