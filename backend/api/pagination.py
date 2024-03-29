from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class ApiPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = settings.MAX_PAGE_SIZE
    page_size = settings.PAGE_SIZE
    default_page_size = settings.DEFAULT_PAGE_SIZE
