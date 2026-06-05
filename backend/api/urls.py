from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HistoryViewSet, ArbitrageViewSet

router = DefaultRouter()
router.register('arbitrage', ArbitrageViewSet, 'arbitrage')
router.register('history', HistoryViewSet, 'history')

urlpatterns = [
    path('', include(router.urls))
]
