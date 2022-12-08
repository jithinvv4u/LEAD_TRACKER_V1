from rest_framework import pagination


class LargePaginator(pagination.PageNumberPagination):
    page_size = 999
