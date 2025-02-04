from rest_framework import pagination


class CatsPagination(pagination.PageNumberPagination):
    page_size = 20