from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class CatsPagination(pagination.PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('cnt', self.page.paginator.count),
            ('nxt', self.get_next_link()),
            ('prev', self.get_previous_link()),
            ('results', data)
        ]))
