from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100
    page_size = 6


class ApiPageNumberPagination(CustomPageNumberPagination):
    default_page_size = 6
