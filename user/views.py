import binascii

from django_filters.rest_framework import DjangoFilterBackend
from paycomuz import Paycom
from rest_framework import generics, status, authentication, permissions, filters
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import base64, zlib, logging
from rest_framework.views import APIView

from cargo.models import Cargo
from config import settings

logger = logging.getLogger(__name__)
from .models import *
from .pagination import CustomPagination
from user.payment import *
from .serializers import *
from .send_message import verify
# from geopy.geocoders import Nominatim

from paycomuz.views import MerchantAPIView
# from paycomuz import Paycom


class RegisterPhoneView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        phone = request.data.get('phone')
        user  = User.objects.filter(phone=phone).last()
        if user is None:
            if serializer.is_valid():
                code = str(random.randint(100000, 1000000))
                if VerifyEmail.objects.filter(phone=phone).first():
                    vers = VerifyEmail.objects.filter(phone=phone)
                    for ver in vers:
                        ver.delete()
                if len(phone) == 13:
                    verify(phone, code)
                    msg_s = "Отправлен одноразовый код для подтверждения номера телефона."
                    VerifyEmail.objects.create(phone=phone, code=code)
                    return Response({
                        "phone": phone,
                        "msg": msg_s
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "msg": "Номер телефона введен неправильно"
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        else:
            return Response({
                "msg": "Пользователь уже зарегистрирован"
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(generics.GenericAPIView):
    serializer_class = VerifySerializer

    def post(self, request):
        # try:
        phone = request.data.get('phone')
        code = request.data.get('code')
        verify = VerifyEmail.objects.filter(phone=phone, code=code).last()
        if verify:
            verify.is_verify = True
            verify.save()
            return Response({
                'msg': "Пользователь проверен",
            }, status=status.HTTP_200_OK)
        else:
            return Response("Номер телефона или код неверно", status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response("Номер телефона или код неверно", status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get('phone')
        user_type = request.data.get('user_type')
        verify = VerifyEmail.objects.filter(phone=phone).last()
        if verify and verify.is_verify == True:
            if user_type == 'driver':
                car_number = request.data.get('car_number')
                # drive_doc = request.data.get('drive_doc')
                car_image_1 = request.data.get('car_image_1')
                car_image_2 = request.data.get('car_image_2')
                car_type = request.data.get('car_type')
                user = User.objects.create_user(username=username, password=password, phone=phone, user_type=user_type,
                                                car_number=car_number, car_image_1=car_image_1,
                                                car_image_2=car_image_2, car_type=car_type, is_verified = True)
                user.save()
                verify.delete()
            else:
                User.objects.create_user(username=username, password=password, phone=phone, user_type=user_type, is_verified = True)
                verify.delete()
            return Response({
                'msg': "Регистрация прошла успешно"
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'msg': "Пользователь не проверен"
            }, status=status.HTTP_400_BAD_REQUEST)


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
                }, status=status.HTTP_200_OK)
            else:
                return Response("Неверное имя пользователя или пароль", status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
        works = len(user.works)
        cargos = len(user.cargos)


        if check:
            if works == 0:
                user.delete()
                return Response({
                    "msg": "Аккаунт удален"
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "msg": "У вас есть незаконченное дело",
                    'работы': f"{works} штук",
                    'доставкы': f"{cargos} штук",
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "msg": "Неверный пароль"
            }, status=status.HTTP_400_BAD_REQUEST)


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

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request):
        phone = request.data.get('phone')
        user = User.objects.filter(phone=phone).first()
        if phone and user:
            code = str(random.randint(100000, 1000000))
            ver = verify(phone, code)
            if ver:
                VerifyEmail.objects.create(phone=phone, code=code)
                return Response({"message": "SMS код отправлено"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Неверный номер телефона"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_400_BAD_REQUEST)


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


class UserUpdateView(generics.UpdateAPIView):

    serializer_class = EditProfileSerializer
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
            'status': 'Успешно',
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
        return works 
        #return Response({"results": works}, status=status.HTTP_200_OK)


class UserJobsView(generics.ListAPIView):
    serializer_class = WorkListSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        works = Work.objects.filter(doer=user.id).order_by('-id')
        result = works.exclude(status='finished')
        return result 
        #return Response({"jobs": result}, status=status.HTTP_200_OK)


#Payment system
class CartCreate(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        number = request.data.get('card')
        expire = request.data.get('expire')
        result = payme_subscribe_cards._cards_create(123, number, expire, True)
        if "error" in result:
            return Response({
                "msg": "Неверные данные",
                "error": result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            token = result['result']['card']['token']
            ver_code = payme_subscribe_cards._card_get_verify_code(123, token)
            if "error" in ver_code:
                return Response({
                    "msg": "Неверные данные",
                    "error": result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "msg": "Регистрация прошла успешно",
                    "token": token,
                    "result": ver_code['result']
                }, status=status.HTTP_200_OK)


class CartVerify(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        code = str(request.data.get('code'))
        token = request.data.get('token')
        result = payme_subscribe_cards._cards_verify(123, code, token)
        if "error" in result:
            return Response({
                "msg": "Неверные данные",
                "error": result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "msg": "Верификация прошла успешно",
                'result': result['result']
            }, status=status.HTTP_200_OK)

class CartCheck(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = request.data.get('token')
        card = request.data.get('card')
        account_id = request.user.account
        result = payme_subscribe_cards._cards_check(123, token)
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        if "error" in result:
            return Response({
                "msg": "Неверные данные",
                "error": result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.carddata_set.get_or_create(card=card, account=account_id)
            return Response({
                "msg": "Прошла успешно",
                "result": result['result'],
                "user": request.user.account

            }, status=status.HTTP_200_OK)


class CartRemove(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = request.data.get('token')
        account_id = request.user.account
        result = payme_subscribe_cards._cards_remove(123, token)
        if "error" in result:
            return Response({
                "msg": "Неверные данные",
                "error": result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            card = CardData.objects.filter(account=account_id).last()
            card.delete()
            return Response({
                "msg": "Прошла успешно",
                "result": result['result']
            }, status=status.HTTP_200_OK)


class CreateInvoice(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        amount = float(request.data.get('amount'))*100
        account_id = request.user.account
        result = payme_subscribe_receipts._receipts_create(123, amount, account_id)
        client = User.objects.filter(account=account_id).first()
        card = CardData.objects.filter(account=account_id).last()
        if not card or not client or "error" in result:
            return Response({
                "msg": "Неверные данные",
                "error": result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "msg": "Прошла успешно",
                "result": result['result']
            }, status=status.HTTP_200_OK)


class PayInvoice(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        invoice_id = request.data.get('invoice_id')
        token = request.data.get('token')
        phone = request.data.get('phone')
        amount = int(request.data.get('amount'))
        user = request.user
        result = payme_subscribe_receipts._receipts_pay(123, invoice_id, token, phone)
        if "error" in result:
            return Response({
                "msg": "Неверные данные",
                "error": result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.money += amount
            user.save()
            return Response({
                "msg": "Прошла успешно",
                "result": result['result']
            }, status=status.HTTP_200_OK)


class CheckPaymentView(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        invoice_id = request.data.get('invoice_id')
        result = payme_subscribe_receipts._receipts_check(123, invoice_id)
        if "error" in result:
            return Response({
                "msg": "Неверные данные",
                "error": result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            state = result['result']['state']
            if state == 4:

                return Response({
                    "msg": "Оплата успешно",
                    "result": result['result']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "msg":"Произошла ошибка при оплате"}, status=status.HTTP_400_BAD_REQUEST
                )


class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        return self.ORDER_FOUND


    def successfully_payment(self, account, transaction, *args, **kwargs):
        print(account)


    def cancel_payment(self, account, transaction, *args, **kwargs):
        print(account)


class CheckMerchantView(MerchantAPIView):
    serializer_class = UserCashSerializer
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)


    # should this be in settings.py ?
    """
    Return request's 'X-Mirror-Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """

    # @staticmethod
    # def authorize(password: str) -> None:
    #     # if not isinstance(password, str):
    #     #     logger.error("Request from an unauthorized source!")
    #     #     raise PermissionDenied()
    #
    #     password = password.split()[-1]
    #     print(password)
    #     # try:
    #     #     password = base64.b64decode(password).decode('utf-8')
    #     # except (binascii.Error, UnicodeDecodeError):
    #     #     logger.error("Error when authorize request to merchant!")
    #     #     raise PermissionDenied()
    #
    #     merchant_key = password.split(':')[-1]

        # фильтруем метод по ключу, если ключа нету у нас в системе возвращаем ошибку авторизации
        # if merchant_key == settings.PAYCOM_KEY:
        #     return BasePaycomMerchantMethod.ORDER_DEBT
        # elif merchant_key == settings.PAYCOM_DRIVER_KEY:
        #     return BasePaycomMerchantMethod.DRIVER_REFILL
        # else:
        #     logger.error("Invalid key in request!")
        #     raise PermissionDenied()




        # logger.info(f'Method: {data["method"]}')
        #
        # try:
        #     # определяем какой ПЕЙКОМ МЕТОД
        #     # ссылочка на список мерчант методов пейкома - https://developer.help.paycom.uz/ru/metody-merchant-api
        #     paycom_method = self.get_paycom_method_by_name(data.get('method'))
        # except ValidationError:
        #     logger.error(f'Paycom method not found. Request data: \n{request.data}')
        #     raise MethodNotFoundError()

        # result = paycom_method(data.get('params'), merchant_method)
        # print(request.data)
        # paycom_method = self.get_paycom_method_by_name(data.get('method'))
        # result = paycom_method(data.get('params'), merchant_method)
        # return Response({"jsonrpc": "2.0",  "id": 1, "error": {"code": -32504, "message": "Invalid Request."}})

    # def post(self, request):
    #     auth = request.headers
    #     # meta = request.META
    #     password = request.META.get('HTTP_AUTHORIZATION')
    #     print(password)
    #     if auth:
    #         return Response(auth)
    #     else:
    #         return Response("Authorization")

        # AUTHORIZATION_HEADER = 'HTTP_X_CUSTOM_AUTHORIZATION'
        # auth = request.META.get(AUTHORIZATION_HEADER) #(AUTHORIZATION_HEADER, b'')
        # if isinstance(auth):
        #     # Work around django test client oddness
        #     auth = auth.encode(HTTP_HEADER_ENCODING)
        #
        #     account_id = request.data.get('account_id')
        #     amount = int(request.data.get('amount'))
        #     if account_id and amount:
        #         return Response({
        #             "msg": "Success",
        #             "header": auth
        #         }, status=status.HTTP_200_OK)
        #     else:
        #         return Response({
        #             "msg": "Неверные данные",
        #
        #         }, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(request.headers)


# class GetStreetView(generics.GenericAPIView):
#     serializer_class = AddressSerializer
#
#     def post(self, request):
#         locator = Nominatim(user_agent="myGeocoder")
#         lat = request.data.get("lat")
#         lng = request.data.get("lng")
#         if lat and lng:
#             geocode = lambda query: locator.geocode("%s, Tashkent City" % query)
#             print(geocode("Muhammad Yusuf"))
#             return Response(geocode("Muhammad Yusuf"))
#             # from geopy.geocoders import GoogleV3
#             # geolocator = GoogleV3(api_key='AIzaSyBrrRsUfg7xCMN4-nRb47Wb98WmZS65VkM')
#             # location = geolocator.reverse([lat, lng], timeout=25, sensor=True)
#             # print(location)
#             # print(location.address)
#
#             # location = locator.reverse(f"{lat}, {lng}")
#             # print(location.raw)
#             # return Response({
#             #     "msg": location.raw['display_name']
#             # }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#                 "msg": "Неверные данные"
#             }, status=status.HTTP_400_BAD_REQUEST)


class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder

    # @staticmethod
    # def authorize(password: str) -> None:
    #     # if not isinstance(password, str):
    #     #     logger.error("Request from an unauthorized source!")
    #     #     raise PermissionDenied()
    #
    #     password = password.split()[-1]
    #     print(password)
    #     # try:
    #     #     password = base64.b64decode(password).decode('utf-8')
    #     # except (binascii.Error, UnicodeDecodeError):
    #     #     logger.error("Error when authorize request to merchant!")
    #     #     raise PermissionDenied()
    #
    #     merchant_key = password.split(':')[-1]


