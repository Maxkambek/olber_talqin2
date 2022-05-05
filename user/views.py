import random

from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User, Cargo, Car, VerifyEmail
from .serializers import LoginSerializer, UserSerializer, CargoSerializer, CargoListSerializer, CarSerializer, \
    RegisterSerializer, VerifySerializer


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
            verify = user.is_email_verified
            print(check)
            print(verify)
            if check and verify:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'email': email
                })
            else:
                return Response("Неверное имя пользователя или пароль", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        if serializer.is_valid():
            subject = "Emailni tasdiqlash"
            code = str(random.randint(100000, 1000000))
            msg = "Emailni tasdiqlash uchun bir martalik kod: " + code
            to = request.data.get('email')
            res = send_mail(subject, str(msg), settings.EMAIL_HOST_USER, [to])
            if (res == 1):
                msg1 = str(msg) + " " + to + " ga jo'natildi "
                VerifyEmail.objects.create(email=email, code=code)
                User.objects.create_user(email=email, username=username, password=password)
            else:
                msg1 = "Ma'lumotlarda xatolik!"
            print(msg1)
            print(email)
            return Response(msg1, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        if VerifyEmail.objects.filter(email=email, code=code).first():
            user = User.objects.get(email=email)
            user.is_email_verified = True
            user.save()
            return Response("Email is verified", status=status.HTTP_200_OK)
        else:
            return Response("Email or code invalid", status=status.HTTP_400_BAD_REQUEST)

class UsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CargoCreateView(generics.CreateAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()


class CargoListView(generics.ListAPIView):
    serializer_class = CargoListSerializer
    queryset = Cargo.objects.all()


class CarCreateView(generics.CreateAPIView):
    serializer_class = CarSerializer
    queryset = Car.objects.all()