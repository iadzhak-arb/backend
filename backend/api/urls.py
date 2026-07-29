from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import (
    MarketViewSet, ArbitrageViewSet,
    TokenViewSet, ExchangeViewSet, SummaryView
)

router = DefaultRouter()
router.register('arbitrage', ArbitrageViewSet, 'arbitrage')
router.register('markets', MarketViewSet, 'markets')
router.register('exchanges', ExchangeViewSet, 'exchanges')
router.register('tokens', TokenViewSet, 'tokens')

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', SummaryView.as_view(), name='summary'),
    path('auth/', include('auth_kit.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
