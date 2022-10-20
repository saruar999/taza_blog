from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import status
from rest_framework.serializers import ValidationError

from rest_framework_simplejwt.views import TokenObtainPairView

from core.models.admins import Admins
from core.models.authors import Author
from core.views import CustomCreateMixin, ResponseMixin

from .serializers import RegisterSerializer, VerifyEmailSerializer, AdminRegisterSerializer


class RegisterView(CustomCreateMixin):

    serializer_class = RegisterSerializer
    queryset = Author.objects.all()

    @action(methods=['patch'], detail=True,
            url_name='verify-account',
            url_path='verify_account',
            name='Email verification')
    def verify_account(self, request, pk=None):

        data = request.data
        user = self.get_object()
        serializer = VerifyEmailSerializer(user, data=data)

        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        if not isinstance(data, ValidationError):
            return self.get_response(res=Response({'message': 'User has been verified'},
                                     status=status.HTTP_200_OK),
                                     success=True)
        else:
            return self.return_400()


class AdminRegisterView(CustomCreateMixin):

    queryset = Admins.objects.all()
    serializer_class = AdminRegisterSerializer
    permission_classes = (DjangoModelPermissions,)


class LoginView(ResponseMixin, TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        res = super().post(request)
        return self.get_response(res=res, success=res.status_code == status.HTTP_200_OK)


















