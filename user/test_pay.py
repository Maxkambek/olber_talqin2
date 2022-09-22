from django.conf import settings
import base64
from decimal import Decimal

assert settings.PAYCOM_SETTINGS.get('KASSA_ID') != None
assert settings.PAYCOM_SETTINGS.get('ACCOUNTS') != None
assert settings.PAYCOM_SETTINGS['ACCOUNTS'].get('KEY') != None

TOKEN = settings.PAYCOM_SETTINGS['KASSA_ID']
KEY = settings.PAYCOM_SETTINGS['ACCOUNTS']['KEY']


class PayComResponse(object):
    LINK = 'https://checkout.paycom.uz'

    def create_initialization(self, amount: Decimal, order_id: str, return_url: str) -> str:
        """
        documentation : https://help.paycom.uz/ru/initsializatsiya-platezhey/otpravka-cheka-po-metodu-get
        >>> self.create_initialization(amount=Decimal(5000.00), order_id='1', return_url='https://2d78-213-230-121-237.ngrok.io/user/check-merchant/')
        """

        params = f"m={TOKEN};ac.{KEY}={order_id};a={amount};c={return_url}"
        encode_params = base64.b64encode(params.encode("utf-8"))
        encode_params = str(encode_params, 'utf-8')
        print(encode_params)
        url = f"{self.LINK}/{encode_params}"
        return url

    @staticmethod
    def authorize(password: str) -> None:
        # if not isinstance(password, str):
        #     logger.error("Request from an unauthorized source!")
        #     raise PermissionDenied()

        password = password.split()[-1]
        print(password)