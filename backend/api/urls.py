from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ArbitrageViewSet

router = DefaultRouter()
router.register('arbitrage', ArbitrageViewSet, 'arbitrage')

urlpatterns = [
    path('', include(router.urls))
]
