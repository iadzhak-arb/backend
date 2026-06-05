from django.urls import path

from .views import ArbitrageListView, ArbitrageDetailView

urlpatterns = [
    path('', ArbitrageListView.as_view(), name='arbitrage'),
    path('history/', ArbitrageDetailView.as_view(), name='history')
]
