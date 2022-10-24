from rest_framework.decorators import action
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models.admins import Admins
from core.models.authors import Author
from core.views import CustomCreateMixin, ResponseMixin
from core.permissions import DjangoModelPermissions

from .serializers import RegisterSerializer, VerifyEmailSerializer, AdminRegisterSerializer


class RegisterView(CustomCreateMixin):

    authentication_classes = []
    serializer_class = RegisterSerializer
    queryset = Author.objects.all()

    @action(methods=['patch'], detail=True,
            url_name='verify-account',
            url_path='verify_account',
            name='Email verification')
    def verify_account(self, request, pk=None):

        data = request.data
        user = self.get_object()

        if self.error_res is not None:
            return self.error_res

        serializer = VerifyEmailSerializer(user, data=data)

        return self.serialize_extra_action(serializer=serializer, message='verification successful')


class AdminRegisterView(CustomCreateMixin):

    queryset = Admins.objects.all()
    serializer_class = AdminRegisterSerializer
    permission_classes = (DjangoModelPermissions,)


class LoginView(ResponseMixin, TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        res = super().post(request)
        return self.get_response(res=res, success=res.status_code == status.HTTP_200_OK)


















