from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
import random


class User(AbstractUser):
    USER_CHOICES = (
        ("client", "Mijoz"),
        ("worker", "Ishchi"),
        ("driver", "Haydovchi")
    )
    CAR_TYPES = (
        ('0', "0"),
        ('S', "S"),
        ('M', "M"),
        ('L', "L"),
        ('XL', "XL"),
        ('XXL', "XXL"),
    )

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")

    is_verified = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(choices=USER_CHOICES, max_length=25, default="client")
    rating = models.FloatField(verbose_name="Reyting", validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0)
    point = models.FloatField(verbose_name="Umumiy ball", default=0)
    count = models.IntegerField(verbose_name="Ishlar soni", default=0)
    works = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    cargos = ArrayField(models.CharField(max_length=50), blank=True, default=list)
    status = models.BooleanField(default=False)
    car_type = models.CharField(max_length=15, verbose_name="Mashina turi", choices=CAR_TYPES, default="0")
    drive_doc = models.ImageField(verbose_name="Guvohnoma", null=True, blank=True)
    car_image_1 = models.ImageField(verbose_name="Mashina rasmi", null=True, blank=True)
    car_image_2 = models.ImageField(verbose_name="Mashina rasmi", null=True, blank=True)
    car_number = models.CharField(max_length=8, verbose_name="Mashina raqami", null=True, blank=True)
    account = models.CharField(max_length=50, unique=True)
    money = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.count > 0:
            self.rating = (self.point)/int(self.count)
            self.rating = round(self.rating, 1)
            super(User, self).save(*args, **kwargs)
        else:
            self.rating = 0
            self.point = 0
            super(User, self).save(*args, **kwargs)
        if not self.account:
            self.account = str(random.randint(100000, 1000000))
            super(User, self).save(*args, **kwargs)


class VerifyEmail(models.Model):
    class Meta:
        verbose_name = _("Email tasdiqlash")
        verbose_name_plural = _("Email tasdiqlash")

    phone = models.CharField(max_length=15, verbose_name="Telefon raqam")
    code = models.CharField(max_length=10, verbose_name="Kod")
    is_verify = models.BooleanField(default=False)


class CardData(models.Model):
    class Meta:
        verbose_name = _("Karta ma'lumotlari")
        verbose_name_plural = _("Karta ma'lumotlari")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.CharField(max_length=20, verbose_name="Card number")
    account = models.CharField(max_length=10, verbose_name="Account id")
