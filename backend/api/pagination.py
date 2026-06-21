from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageLimitPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 20
    page_size_query_param = 'limit'
