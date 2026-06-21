from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from .views import ArbitrageViewSet, MarketViewSet

router = DefaultRouter()
router.register('arbitrage', ArbitrageViewSet, 'arbitrage')
router.register('markets', MarketViewSet, 'markets')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', )
]
