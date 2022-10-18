from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.response import Response


class ResponseMixin:

    @staticmethod
    def get_response(res, success=True):

        res.data = {
            'success': success,
            'status_code': res.status_code,
            'data': res.data
        }
        return res


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

    def perform_create(self, serializer):
        return serializer.save()

