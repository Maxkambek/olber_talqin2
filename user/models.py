from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta:
        verbose_name="Foydalanuvchi"
        verbose_name_plural="Foydalanuvchilar"

    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=True, blank=True)


class Cargo(models.Model):

    class Meta:
        verbose_name="Jo'natma"
        verbose_name_plural="Jo'natmalar"

    STATUS_CHOISES = (
        ('new', "Ko'rib chiqilmoqda"),
        ('sent', "Yo'lda"),
        ('finished', "Yopilgan"),
    )
    title = models.CharField(max_length=150)
    price = models.CharField(max_length=150)
    weight = models.CharField(max_length=10)
    from_adrress = models.CharField(max_length=255)
    from_floor = models.PositiveIntegerField()
    from_kv = models.PositiveIntegerField()
    from_persons = models.PositiveIntegerField()
    to_adrress = models.CharField(max_length=255)
    to_floor = models.PositiveIntegerField()
    to_kv = models.PositiveIntegerField()
    to_persons = models.PositiveIntegerField()
    when = models.DateField()
    description = models.TextField(verbose_name="Tafsilot")
    image1 = models.ImageField()
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOISES, default="new")

    def __str__(self):
        self.title