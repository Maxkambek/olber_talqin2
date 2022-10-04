from rest_framework import serializers

from payment.models import PaymeTransaction


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymeTransaction
        fields = "__all__"