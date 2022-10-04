from django.db import models

class PaymeTransaction(models.Model):
    account_id = models.CharField(max_length=10)
    amount = models.CharField(max_length=25)
    trx_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)