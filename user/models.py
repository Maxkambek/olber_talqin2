from django.db import models
from django.contrib.auth.models import AbstractUser

from user.calculation import calc_distance


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
    distance = models.FloatField(null=True, blank=True)


    def save(self, *args, **kwargs):
        self.distance = calc_distance(self.from_adrress, self.to_adrress)
        self.distance = round(self.distance, 2)
        super(Cargo, self).save(*args, **kwargs)


class Car(models.Model):
    CAR_TYPES = (
        ('1', "Kichik"),
        ('2', "O'rta"),
        ('3', "Katta"),
    )
    user = models.ForeignKey(User, verbose_name="Haydovchi", on_delete=models.CASCADE)
    car_type = models.CharField(max_length=15, verbose_name="Mashina turi", choices=CAR_TYPES)
    drive_license = models.CharField(max_length=50, verbose_name="Guvohnoma raqami")
    drive_doc = models.CharField(max_length=50, verbose_name="Guvohnoma raqami")
    tech_inspect = models.CharField(max_length=50, verbose_name="Texnik ko'rik")


class VerifyEmail(models.Model):
    class Meta:
        verbose_name="Email tasdiqlash"
        verbose_name_plural="Email tasdiqlash"

    email = models.CharField(max_length=100, verbose_name="Email")
    code = models.CharField(max_length=10, verbose_name="Kod")