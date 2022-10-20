from rest_framework.mixins import CreateModelMixin, \
                                    RetrieveModelMixin, \
                                    ListModelMixin, \
                                    UpdateModelMixin, \
                                    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404


class ResponseMixin:

    @staticmethod
    def get_response(res, success=True):
        res.data = {
            'success': success,
            'status_code': res.status_code,
            'data': res.data
        }
        return res

    @staticmethod
    def return_404():
        data = {
            'success': False,
            'status_code': status.HTTP_404_NOT_FOUND,
            'data': {
                'error': 'not found'
            }
        }
        return Response(data)

    @staticmethod
    def return_400():
        data = {
            'success': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'data': {
                'error': 'invalid input'
            }
        }
        return Response(data)


class CustomCreateMixin(ResponseMixin, GenericViewSet, CreateModelMixin):
    """
        Overriding the default CreateModelMixin to unify the response structure with get_response of BaseView
    """

    def create(self, request, serializer=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) if serializer is None else serializer
        if serializer.is_valid():
            self.perform_create(serializer)
            res = Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            res = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return self.get_response(res=res,
                                 success=res.status_code == status.HTTP_201_CREATED)


class CustomRetrieveMixin(ResponseMixin, GenericViewSet, RetrieveModelMixin):

    def retrieve(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            res = Response(serializer.data)
        except Http404:
            return self.return_404()

        return self.get_response(res=res, success=res.status_code == status.HTTP_200_OK)


class CustomListMixin(ResponseMixin, GenericViewSet, ListModelMixin):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            res = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            res = Response(serializer.data)

        return self.get_response(res=res, success=res.status_code == status.HTTP_200_OK)


class CustomUpdateMixin(ResponseMixin, GenericViewSet, UpdateModelMixin):

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_object()
        except Http404:
            return self.return_404()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            res = Response(serializer.data, status=status.HTTP_200_OK)
        else:
            res = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.get_response(res=res, success=res.status_code == status.HTTP_200_OK)


class CustomDestroyMixin(ResponseMixin, GenericViewSet, DestroyModelMixin):

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            self.perform_destroy(instance)
            res = Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            return self.get_response(res=res, success=res.status_code == status.HTTP_204_NO_CONTENT)
        except Http404:
            return self.return_404()


class CustomModelViewSet(CustomDestroyMixin,
                         CustomRetrieveMixin,
                         CustomUpdateMixin,
                         CustomListMixin,
                         CustomCreateMixin):
    pass