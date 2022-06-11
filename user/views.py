import random
from django.conf import settings
from django.contrib import auth
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, authentication, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User, Cargo, VerifyEmail
from django.db.models import Max
from .serializers import LoginSerializer, CargoSerializer, CargoListSerializer, RegisterSerializer, \
    VerifySerializer, UserListSerializer, UserProfileSerializer, CargoCreateSerializer, \
    UserSerializer, ChangePasswordSerializer, CargoAcceptSerializer, UserTypeSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        user = User.objects.filter(email=email).first()
        registered = 1
        if user and user.is_verified == True:
            return Response({
                "msg": "Ushbu email registratsiya qilingan"
            }, status=status.HTTP_409_CONFLICT)
        elif user is None:
            registered = 0
        else:
            user.delete()
            registered = 0

        if registered == 0 and serializer.is_valid():
            subject = "Emailni tasdiqlash"
            code = str(random.randint(100000, 1000000))
            msg = f"Emailni tasdiqlash uchun bir martalik kod: {code}"
            to = request.data.get('email')
            # result = send_mail(subject, str(msg), settings.EMAIL_HOST_USER, [to])
            # if VerifyEmail.objects.filter(email=email).first():
            #     verify = VerifyEmail.objects.get(email=email)
            #     verify.delete()
            # if (result == 1):
            #     msg1 = f"Emailni tasdiqlash uchun bir martalik kod {to} ga jo'natildi."
            VerifyEmail.objects.create(email=email, code=code)
            User.objects.create_user(email=email, username=username, password=password)
            print(code)
            # else:
            #     return Response(
            #         {"msg": "Ma'lumotlarda xatolik bor yoki verifikatsiya uchun kod emailingizga jo'natilgan!"},
            #         status=status.HTTP_400_BAD_REQUEST)
            return Response({
                "email": email,
                "username": username,
                # "msg": msg1
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    serializer_class = UserSerializer

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


class ChangePasswordView(generics.UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': {
                    'username': user.username,
                }
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request):
        email = self.request.data.get('email')
        if email:
            code = str(random.randint(100000, 1000000))
            send_mail("Kod:", code, settings.EMAIL_HOST_USER, [email])
            VerifyEmail.objects.create(email=email, code=code)
            return Response("SMS jo'natildi")
        else:
            return Response("Email is required", status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetPasswordView(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request):
        try:
            email = request.data.get('email')
            code = request.data.get('code')
            password = request.data.get('password')
            verify = VerifyEmail.objects.filter(email=email, code=code).first()
            if verify:
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                verify.delete()
                return Response({
                    'msg': "Password changed",
                    'email': email
                }, status=status.HTTP_200_OK)
            else:
                return Response("Code invalid", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Code invalid", status=status.HTTP_400_BAD_REQUEST)


class UsersView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()


class UserItemsView(generics.ListAPIView):
    serializer_class = CargoListSerializer
    queryset = Cargo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    pagination_class = None

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        if user:
            print(user)
            return user.items.all()


class UserTypeView(generics.GenericAPIView):
    serializer_class = UserTypeSerializer

    def post(self, request):
        serializer = UserTypeSerializer(data=request.data)
        try:
            if serializer.is_valid():
                email = serializer.data.get('email')
                user_type = serializer.data.get('user_type')
                user = User.objects.get(email=email)
                user.user_type = user_type
                user.save()

                return Response({
                        'msg': "User type changed",
                    }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                        'msg': "User not found",
                    }, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


class AddPointView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    def post(self, request):
        rating = request.data.get('rating')
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        user.point += rating
        user.count += 1
        user.rating = user.point/user.count
        user.save()
        return Response(f"{rating} ball qo'yildi")


class CargoCreateView(generics.CreateAPIView):
    serializer_class = CargoCreateSerializer
    queryset = Cargo.objects.all()


class CargoListView(generics.ListAPIView):
    serializer_class = CargoListSerializer
    queryset = Cargo.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'cargo_type']
    ordering_fields = ['price', 'distance', 'weight']
    pagination_class = PageNumberPagination
    def get_queryset(self):
        p_min = self.request.GET.get('p_min')
        p_max = self.request.GET.get('p_max')
        d_min = self.request.GET.get('d_min')
        d_max = self.request.GET.get('d_max')
        w_min = self.request.GET.get('w_min')
        w_max = self.request.GET.get('w_max')
        if not p_min or p_min == '':
            p_min = 0
        if not p_max or p_max == '':
            p_max = Cargo.objects.all().order_by('-price').first().price
        if not d_min or d_min == '':
            d_min = 0
        if not d_max or d_max == '':
            d_max = Cargo.objects.all().order_by('-distance').first().distance
        if not w_min or w_min == '':
            w_min = 0
        if not w_max or w_max == '':
            w_max = Cargo.objects.all().order_by('-weight').first().weight

        if p_min or p_max or d_min or d_max or w_min or w_max:
            items = Cargo.objects.filter(price__range=(p_min, p_max), distance__range=(d_min, d_max), weight__range=(w_min, w_max),).order_by('-id')
        else:
            items = Cargo.objects.all().order_by('-id')
        return items

class CargoDetailView(generics.RetrieveAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()


class CargoUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CargoSerializer
    queryset = Cargo.objects.all()


class OfferView(generics.GenericAPIView):
    serializer_class = CargoSerializer
    authentication_classes = [authentication.TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated,]

    def post(self, request, pk=None):
        cargo = Cargo.objects.get(id=pk)
        user = request.user

        if not cargo.offers.filter(id=user.id).exists():
            cargo.offers.add(*[user.id, ])
            cargo.save()
            return Response(f"Offer belgilandi {cargo.title} uchun", status=status.HTTP_200_OK)
        else:
            return Response("Offer yozilib bo'lingan", status=status.HTTP_400_BAD_REQUEST)


class CargoAcceptView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = CargoAcceptSerializer(data = request.data)
        user_id = request.user.id
        if serializer.is_valid():
            item_id = request.data.get("id")
            doer_id = request.data.get("doer")
            cargo = Cargo.objects.get(id=item_id)
            if cargo.user_id == user_id:
                user = User.objects.get(id=doer_id)
                if item_id not in user.works:
                    user.works.append(item_id)
                    user.save()
                cargo.doer = doer_id
                cargo.status = 'finished'
                cargo.save()
                return Response("Success", status=status.HTTP_200_OK)
            else:
                return Response("User not owner", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
