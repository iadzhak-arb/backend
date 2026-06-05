from django_filters.views import FilterView

from .filters import ArbitrageFilter, ArbitrageHistoryFilter
from .models import Arbitrage


class ArbitrageListView(FilterView):
    model = Arbitrage
    template_name = 'orderbooks/index.html'
    filterset_class = ArbitrageFilter
    queryset = Arbitrage.latest.all()
    paginate_by = 10
    ordering = '-margin'


class ArbitrageDetailView(FilterView):
    model = Arbitrage
    template_name = 'orderbooks/index.html'
    filterset_class = ArbitrageHistoryFilter
    paginate_by = 20
