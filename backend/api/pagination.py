from users.pagination import CustomPageNumberPagination


class ApiPageNumberPagination(CustomPageNumberPagination):
    default_page_size = 6
