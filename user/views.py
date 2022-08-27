from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, authentication, permissions, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import *
from .pagination import CustomPagination
from user.payment import *
from .serializers import *
from .send_message import verify


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(request):
        serializer = RegisterSerializer(data=request.data)
        phone = request.data.get('phone')
        password = request.data.get('password')
        username = request.data.get('username')
        user = User.objects.filter(phone=phone).first()
        registered = 1
        if user and user.is_verified == True:
            return Response({
                "msg": "Ushbu raqam registratsiya qilingan"
            }, status=status.HTTP_409_CONFLICT)
        elif user is None:
            registered = 0
        else:
            user.delete()
            registered = 0

        if registered == 0 and serializer.is_valid():
            code = str(random.randint(100000, 1000000))
            if VerifyEmail.objects.filter(phone=phone).first():
                ver = VerifyEmail.objects.get(phone=phone)
                ver.delete()
            if len(phone) == 13:
                verify(phone, code)
                msg_s = "Telefon nomerni tasdiqlash uchun bir martalik kod jo'natildi."
                VerifyEmail.objects.create(phone=phone, code=code)
                User.objects.create_user(username=username, password=password, phone=phone)
            else:
                return Response(
                    {"msg": "Telefon raqami noto'g'ri kiritilgan"},
                    status=status.HTTP_400_BAD_REQUEST)
            if verify:
                return Response({
                    "phone": phone,
                    "username": username,
                    "msg": msg_s
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "username": username,
                    "msg": "Sms yuborishda xatolik"
                }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request):
        try:
            phone = request.data.get('phone')
            code = request.data.get('code')
            verify = VerifyEmail.objects.filter(phone=phone, code=code).first()
            if verify:
                user = User.objects.filter(phone=phone).first()
                user.is_verified = True
                user.save()
                verify.delete()
                return Response({
                    'msg': "Phone number is verified",
                    'phone': phone
                }, status=status.HTTP_200_OK)
            else:
                return Response("Phone number or code invalid", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Phone number or code invalid", status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            phone = request.data.get('phone')
            password = request.data.get('password')
            user = User.objects.get(phone=phone)
            check = user.check_password(password)
            verify = user.is_verified
            if check and verify:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'phone': phone,
                    'user_type': user.user_type,
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
    serializer_class = PhoneSerializer

    def post(self, request):
        phone = request.data.get('phone')
        if phone:
            code = str(random.randint(100000, 1000000))
            ver = verify(phone, code)
            if ver:
                VerifyEmail.objects.create(phone=phone, code=code)
                return Response({"message": "SMS jo'natildi"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Phone number is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetSerializer

    def post(self, request):
        try:
            phone = request.data.get('phone')
            code = request.data.get('code')
            password = request.data.get('password')
            ver = VerifyEmail.objects.filter(phone=phone, code=code).last()
            if ver:
                user = User.objects.get(phone=phone)
                user.set_password(password)
                user.save()
                ver.delete()
                return Response({
                    'msg': "Password changed",
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Code invalid"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Code invalid"}, status=status.HTTP_400_BAD_REQUEST)


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
            itemss = user.items.all()
            return itemss.exclude(status='finished')


class UserWorkesView(generics.ListAPIView):
    serializer_class = WorkListSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Work.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user:
            print(user)
            return user.workss.all()


class UserTypeView(generics.GenericAPIView):
    serializer_class = UserTypeSerializer

    def post(self, request):
        serializer = UserTypeSerializer(data=request.data)
        try:
            if serializer.is_valid():
                phone = serializer.data.get('phone')
                user_type = serializer.data.get('user_type')
                user = User.objects.get(phone=phone)
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
    serializer_class = UserPointSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        point = float(request.data.get('point'))
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        user.point += point
        user.count += 1
        user.rating = user.point/user.count
        user.save()
        return Response({
            'msg': f"{point} ball qo'yildi"
        }, status=status.HTTP_200_OK)


class CargoCreateView(generics.CreateAPIView):
    serializer_class = CargoCreateSerializer
    queryset = Cargo.objects.all()


class CargoListView(generics.ListAPIView):
    serializer_class = CargoListSerializer
    queryset = Cargo.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'cargo_type']
    pagination_class = CustomPagination
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        statusfilter = self.request.query_params.get('status', None)
        typefilter = self.request.query_params.get('cargo_type', None)
        serializer = self.get_serializer(queryset, many=True)
        count = Cargo.objects.count()
        if count > 0:

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
                queryset = Cargo.objects.filter(price__range=(p_min, p_max), distance__range=(d_min, d_max), weight__range=(w_min, w_max),).order_by('-id')
            else:
                queryset = Cargo.objects.all().order_by('-id')

            if statusfilter is not None:
                queryset = Cargo.objects.filter(status=statusfilter)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            return Response({
                'results': serializer.data,
            }, status=status.HTTP_200_OK)#.exclude(user=self.request.user)
        else:
            queryset = "Hozircha e'lonlar yo'q"
            return Response({queryset}, status=status.HTTP_204_NO_CONTENT)


class CargoDetailView(generics.RetrieveUpdateAPIView):
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
            if len(user.works) < 3:

                cargo.offers.add(*[user,])
                cargo.save()
                return Response({
                    'msg': f"{cargo.title} uchun offer belgilandi."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'msg': f"Siz maksimal 3 ta ish olishingiz mumkin"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'msg': "Offer yozilib bo'lingan"
            }, status=status.HTTP_423_LOCKED)


class CargoAcceptView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = CargoAcceptSerializer(data = request.data)
        user_id = request.user.id
        if serializer.is_valid():
            item_id = request.data.get("id")
            doer_id = request.data.get("doer")
            cargo = Cargo.objects.filter(id=item_id).first()
            if cargo.user_id == user_id:
                user = User.objects.get(id=doer_id)
                check = cargo.offers.filter(id=doer_id).first()
                if cargo.status != 'new':
                    return Response({
                        'msg': "Bu zakaz band qilingan"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if not check:
                    return Response({
                        'msg': "Taklif bermagan odamlarni tanlab bo'lmaydi"
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    cargo.doer = user
                    cargo.status = 'selected'
                    if user.works:
                        user.works.append(item_id)
                    else:
                        user.works.insert(0, item_id)
                        print('none')
                    cargo.offers.clear()

                    user.save()
                    cargo.save()
                    return Response({
                        'msg': "Success",
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'msg': "User not owner"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CloseItemView(generics.GenericAPIView):
    serializer_class = CargoSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, pk=None):
        cargo = Cargo.objects.get(id=pk)
        user = request.user
        if cargo.user_id == user.id:
            cargo.status = 'finished'
            cargo.save()
            if cargo.doer:
                doer = cargo.doer
                doer.works.remove(str(pk))
                doer.save()
            return Response({
                'msg': "Cargo closed"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'msg': "User not owner"
            }, status=status.HTTP_400_BAD_REQUEST)


class UserAccountView(generics.GenericAPIView):
    serializer_class = UserAccountSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        user = request.user
        if user.image:
            image = user.image.url
        else:
            image = None
        return Response({
            'status': 'Success',
            'username': user.username,
            'image': image,
            'account': user.account,
            'money': user.money

        }, status=status.HTTP_200_OK)


class UserWorksView(generics.ListAPIView):
    serializer_class = CargoListSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        works = Cargo.objects.filter(doer=user.id).order_by('-id')
        return works #Response({"works"}, status=status.HTTP_200_OK)


class UserJobsView(generics.ListAPIView):
    serializer_class = WorkListSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        works = Work.objects.filter(doer=user.id).order_by('-id')
        result = works.exclude(status='finished')
        return result #Response({"works"}, status=status.HTTP_200_OK)


class WorkListView(generics.ListAPIView):
    serializer_class = WorkListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    pagination_class = CustomPagination
    queryset = Work.objects.all().order_by('-id')


class WorkView(generics.CreateAPIView):
    serializer_class = WorkSerializer
    pagination_class = None
    queryset = Work.objects.all()


class WorkDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = WorkDetailSerializer
    queryset = Work.objects.all()


class WorkOfferView(generics.GenericAPIView):
    serializer_class = WorkSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, pk=None):
        work = Work.objects.get(id=pk)
        user = request.user

        if not work.offers.filter(id=user.id).exists():
            work.offers.add(*[user, ])
            work.save()
            return Response({
                'msg': f"Offer belgilandi {work.title} uchun"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'msg': "Offer yozilib bo'lingan"
            }, status=status.HTTP_400_BAD_REQUEST)


class WorkAcceptView(generics.GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        # try:
        serializer = WorkAcceptSerializer(data = request.data)
        user_id = request.user.id
        if serializer.is_valid():
            item_id = request.data.get("id")
            doer_id = request.data.get("doer")
            work = Work.objects.filter(id=item_id).first()
            if work.user_id == user_id:
                user = User.objects.get(id=doer_id)
                check = work.offers.filter(id=doer_id).first()
                if work.status != 'new':
                    return Response({
                        'msg': "Bu zakaz band qilingan"
                    }, status=status.HTTP_400_BAD_REQUEST)
                if not check:
                    return Response({
                        'msg': "Taklif bermagan odamlarni tanlab bo'lmaydi"
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    work.doer = user
                    work.status = 'selected'
                    # if user.works is not None:
                    # user.works.append(item_id)
                    # else:
                    #     print('Yo')
                    #     user.works = list(item_id)
                    user.save()
                    work.offers.clear()
                    work.save()
                    return Response({
                        'msg': "Success"
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'msg': "User not owner"
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response({
        #         'msg': "Bad request"
        #     }, status=status.HTTP_400_BAD_REQUEST)


class CloseWorkView(generics.GenericAPIView):
    serializer_class = WorkSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, pk=None):
        work = Work.objects.get(id=pk)
        user = request.user
        if work.user_id == user.id:
            work.status = 'finished'
            work.save()
            return Response({
                'msg': "Work closed"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'msg': "User not owner"
            }, status=status.HTTP_400_BAD_REQUEST)


#Payment system
class CartCreate(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        number = request.data.get('card')
        expire = request.data.get('expire')
        result = payme_subscribe_cards._cards_create(123, number, expire, True)
        print(result)
        return Response(result)

class CartGetVerify(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = request.data.get('token')
        result = payme_subscribe_cards._card_get_verify_code(123, token)
        return Response(result)

class CartVerify(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        code = request.data.get('code')
        token = request.data.get('token')
        result = payme_subscribe_cards._cards_verify(123, code, token)
        return Response(result)

class CartCheck(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = request.data.get('token')
        result = payme_subscribe_cards._cards_check(123, token)
        return Response(result)

class CartCheck(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = request.data.get('token')
        result = payme_subscribe_cards._cards_check(123, token)
        return Response(result)


class CartRemove(generics.GenericAPIView):
    serializer_class = UserSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = request.data.get('token')
        result = payme_subscribe_cards._cards_remove(123, token)
        return Response(result)


class CreateInvoice(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        amount = float(request.data.get('amount'))
        order_id = request.data.get('order_id')
        result = payme_subscribe_receipts._receipts_create(123, amount, order_id)
        print(result)
        return Response(result)


class PayInvoice(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        invoice_id = request.data.get('invoice_id')
        token = request.data.get('token')
        phone = request.data.get('phone')
        result = payme_subscribe_receipts._receipts_pay(123, invoice_id, token, phone)
        print(result)
        return Response(result)


class CheckPayment(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        invoice_id = request.data.get('invoice_id')
        account_id = request.data.get('account_id')
        amount = int(request.data.get('amount'))
        result = payme_subscribe_receipts._receipts_check(123, invoice_id)
        print(result)
        state = result['result']['state']
        if state == 4 and user.account == account_id:
            user.money += (amount/100)
            user.save()
            return Response("Payment success", status=status.HTTP_200_OK)
        else:
            return Response("To'lov bilan bog'liq xatolik bo'ldi")
