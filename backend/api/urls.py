from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework.routers import DefaultRouter

from .views import ArbitrageDataViewSet, MarketViewSet, ArbitrageHistoryViewSet

router = DefaultRouter()
router.register('arbitrage', ArbitrageDataViewSet, 'arbitrage')
router.register('history', ArbitrageHistoryViewSet, 'history')
router.register('markets', MarketViewSet, 'markets')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
