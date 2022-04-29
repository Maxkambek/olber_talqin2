from django.contrib import auth
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User, Cargo
from .serializers import LoginSerializer, UserSerializer, CargoSerializer
from .utils import check_email



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = auth.authenticate(email=email, password=password)
            checked = check_email(email)
            if checked and user is not None:
                user_email = User.objects.get(email=email)
                token, created = Token.objects.get_or_create(user=user)
                user_email.is_email_verified = True
                user_email.save()
                return Response({
                    'token': token.key,
                    'email': email
                })
            else:
                return Response("Неверное имя пользователя или пароль", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CargoView(generics.ListCreateAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()