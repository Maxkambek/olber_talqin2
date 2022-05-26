import random
from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, authentication, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, Cargo, Car, VerifyEmail, TestModel
from .serializers import LoginSerializer, CargoSerializer, CargoListSerializer, CarSerializer, \
    RegisterSerializer, VerifySerializer, UserListSerializer, UserProfileSerializer, CargoCreateSerializer, \
    TestSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        user = User.objects.filter(email=email).first()
        if user is None:
            if serializer.is_valid():
                subject = "Emailni tasdiqlash"
                code = str(random.randint(100000, 1000000))
                msg = f"Emailni tasdiqlash uchun bir martalik kod: {code}"
                to = request.data.get('email')
                result = send_mail(subject, str(msg), settings.EMAIL_HOST_USER, [to])
                if VerifyEmail.objects.filter(email=email).first():
                    verify = VerifyEmail.objects.get(email=email)
                    verify.delete()
                if (result == 1):
                    msg1 = f"Emailni tasdiqlash uchun bir martalik kod {to} ga jo'natildi "
                    VerifyEmail.objects.create(email=email, code=code)
                    User.objects.create_user(email=email, username=username, password=password)
                    print(code)
                else:
                    return Response(
                        {"msg": "Ma'lumotlarda xatolik bor yoki verifikatsiya uchun kod emailingizga jo'natilgan!"},
                        status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    "email": email,
                    "username": username,
                    "msg": msg1
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                    "msg": "Ushbu email registratsiya qilingan"
                }, status=status.HTTP_409_CONFLICT)

class VerifyView(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request):
        try:
            email = request.data.get('email')
            code = request.data.get('code')
            verify = VerifyEmail.objects.filter(email=email, code=code).first()
            if verify:
                user = User.objects.filter(email=email).first()
                user.is_verified = True
                user.save()
                verify.delete()
                return Response({
                    'msg': "Email is verified",
                    'email': email
                }, status=status.HTTP_200_OK)
            else:
                return Response("Email or code invalid", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Email or code invalid", status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = User.objects.get(email=email)
            check = user.check_password(password)
            verify = user.is_verified
            if check and verify:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'email': email,
                    'id': user.id
                })
            else:
                return Response("Неверное имя пользователя или пароль", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LogoutView(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({
                "msg": "Logout Success"
            }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeleteAccountView(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        id = request.user.id
        user = User.objects.get(id=id)
        password = request.data.get('password')
        check = user.check_password(password)
        if check:
            user.delete()
            return Response({
                "msg": "Account deleted"
            }, status=status.HTTP_200_OK)
        else:
            return Response("Invalid password", status=status.HTTP_400_BAD_REQUEST)


class UsersView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class UserItemsView(generics.ListAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self, *args, **kwargs):
        try:
            user = User.objects.get(id=self.kwargs['pk'])
            print(user)
            return user.items.all()
        except:
            return Response("User not found")


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


class CargoCreateView(generics.CreateAPIView):
    serializer_class = CargoCreateSerializer
    queryset = Cargo.objects.all()


class CargoListView(generics.ListAPIView):
    serializer_class = CargoListSerializer
    queryset = Cargo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'cargo_type']


class CargoDetailView(generics.RetrieveAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()


class CarCreateView(generics.CreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()


class CargoUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()


class TestCreateListView(generics.ListCreateAPIView):
    serializer_class = TestSerializer
    queryset = TestModel.objects.all()


class TestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestSerializer
    queryset = TestModel.objects.all()