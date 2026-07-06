from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .views import (
    MarketViewSet, ArbitrageViewSet,
    TokenViewSet, ExchangeViewSet
)

router = DefaultRouter()
router.register('arbitrage', ArbitrageViewSet, 'arbitrage')
router.register('markets', MarketViewSet, 'markets')
router.register('exchanges', ExchangeViewSet, 'exchanges')
router.register('tokens', TokenViewSet, 'tokens')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
