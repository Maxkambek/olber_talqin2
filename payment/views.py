import base64
import binascii
from paycomuz.views import MerchantAPIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from config import settings
from payment.libs.create_transaction import CreateTransaction
from logging import getLogger

from user.views import CheckOrder
logger = getLogger(__name__)


class CreateTransactionView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder

    def post(self, request):
        password = request.META.get('HTTP_AUTHORIZATION')
        merchant_method = self.authorize(password)
        # method = request.data.get('method')
        paycom_method = self.get_paycom_method_by_name(
            name=request.data.get('method')
        )
        paycom_method(request.data.get('params'))

        return Response({'result': "Success"})

    @staticmethod
    def authorize(password: str) -> None:
        if not isinstance(password, str):
            logger.error("Request from an unauthorized source!")
            raise PermissionDenied()
        password = password.split()[-1]
        try:
            password = base64.b64decode(password).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            logger.error("Error when authorize request to merchant!")
            raise PermissionDenied()

        merchant_key = password.split(':')[-1]

        if merchant_key == settings.PAYCOM_KEY:
            return "test"
        else:
            logger.error("Invalid key in request")

    @staticmethod
    def get_paycom_method_by_name(name: str):
        available_methods = {
            'CreateTransaction': CreateTransaction,
        }

        try:
            MerchantMethod = available_methods[name]
            print(type(MerchantMethod))
            # return available_methods[name]
        except:
            pass
        merchant_method = MerchantMethod()
        return merchant_method
