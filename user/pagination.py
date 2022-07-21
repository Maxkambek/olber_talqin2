from rest_framework import pagination


class CustomPagination(pagination.LimitOffsetPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200
    page_query_param = 'p'