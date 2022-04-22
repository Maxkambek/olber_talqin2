from django.contrib import auth
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from .utils import check_email


# class RegisterView(generics.GenericAPIView):
#     serializer_class = UserRegisterSerializer
#
#     @staticmethod
#     def post(request):
#         serializer = UserRegisterSerializer(data=request.data)
#         confirmation_token = default_token_generator.make_token(user)
#         subject = "Emailni tasdiqlash"
#         kod = str(random.randint(100000, 1000000))
#         msg = "Emailni tasdiqlash uchun bir martalik kod: " + kod
#         to = request.data.get('email')
#         res = send_mail(subject, str(msg), settings.EMAIL_HOST_USER, [to])
#         if (res == 1):
#             msg1 = str(msg) + " " + to + " ga jo'natildi "
#         else:
#             msg1 = "Xabar jo'natishda xatolik!"
#         print(msg1)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.msg = kod
#             user.save()
#
#             return Response("Ro'yxatdan o'tish muvaffaqiyatli yakunlandi", status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         actiavation_link = f'{activate_link_url}?user_id={user.id}&confirmation_token={confirmation_token}'


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        # try:
        email = request.data.get('email')
        password = request.data.get('password')
        user = auth.authenticate(email=email, password=password)
        checked = check_email(email)
        print(checked)
        if checked and user is not None:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'email': email
            })
        else:
            return Response("Неверное имя пользователя или пароль", status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
