from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 100

    # def paginate_queryset(self, queryset, request, view=None):
    #     if 'search' in request.query_params and len(request.query_params.get('search')) > 0\
    #             or 'top_results_by' in request.query_params and len(request.query_params.get('top_results_by')) > 0:
    #         return None
    #     else:
    #         return super().paginate_queryset(queryset, request, view)
