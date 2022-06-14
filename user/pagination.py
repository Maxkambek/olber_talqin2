from rest_framework import pagination


class CustomPagination(pagination.CursorPagination):
    page_size = 5
    cursor_query_param = 'c'
    ordering = '-created'