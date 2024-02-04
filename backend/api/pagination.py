from rest_framework.pagination import PageNumberPagination

from foodgram_backend.settings import (
    MAX_PAGE_SIZE, PAGE_SIZE, DEFAULT_PAGE_SIZE
)


class ApiPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = MAX_PAGE_SIZE
    page_size = PAGE_SIZE
    default_page_size = DEFAULT_PAGE_SIZE
