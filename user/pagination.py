from rest_framework import pagination


class CustomPagination(pagination.CursorPagination):
    page_size = 10
    cursor_query_param = 'c'
    ordering = '-created'