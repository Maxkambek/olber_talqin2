from payment.models import PaymeTransaction
from payment.serializers import PaymentSerializer
from logging import getLogger
logger = getLogger(__name__)

class CreateTransaction:
    def __call__(self, params: dict = None) -> None:
        if params is not None:
            serializer = PaymentSerializer(data={
                    'trx_id': params.get('id'),
                    'account_id': params.get('account').get('account_id'),
                    'amount': params.get('amount'),
                    'time': params.get('time')
                })
            serializer.is_valid(raise_exception=True)
            logger.info(params)
            cleaned_data = serializer.validated_data
            PaymeTransaction.objects.create(
                account_id=cleaned_data.get('account_id'),
                amount=cleaned_data.get('amount'),
                trx_id=cleaned_data.get('trx_id')
            )
        else:
            pass