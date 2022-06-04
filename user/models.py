from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from user.calculation import calc_distance


class User(AbstractUser):
    GENDER_CHOICES = (
        ("null", "Tanlanmagan"),
        ("men", "Erkak"),
        ("women", "Ayol")
    )

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    is_verified = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=25, default="null")
    rating = models.FloatField(verbose_name="Reyting", validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
                               default=None, null=True, blank=True)


class Cargo(models.Model):
    class Meta:
        verbose_name = "Jo'natma"
        verbose_name_plural = "Jo'natmalar"

    STATUS_CHOICES = (
        ('new', "Ko'rib chiqilmoqda"),
        ('sent', "Yo'lda"),
        ('finished', "Yopilgan"),
    )
    TYPE_CHOICES = (
        ('disabled', "Tanlanmagan"),
        ('small', "Kichik"),
        ('big', "Katta"),
        ('ice_car', "Sovutgich"),
    )
    user = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=150)
    price = models.CharField(max_length=150)
    weight = models.CharField(max_length=10)
    from_address = models.CharField(max_length=255)
    from_floor = models.PositiveIntegerField()
    from_kv = models.PositiveIntegerField()
    from_persons = models.PositiveIntegerField()
    to_address = models.CharField(max_length=255)
    to_floor = models.PositiveIntegerField()
    to_kv = models.PositiveIntegerField()
    to_persons = models.PositiveIntegerField()
    when = models.DateField()
    description = models.TextField(verbose_name="Tafsilot")
    image1 = models.ImageField()
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="new")
    cargo_type = models.CharField(max_length=100, null=True, choices=TYPE_CHOICES, default="disabled")
    distance = models.FloatField(null=True, blank=True)
    offers = models.ManyToManyField(User, verbose_name="Takliflar", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.distance = calc_distance(self.from_address, self.to_address)
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
        verbose_name = "Email tasdiqlash"
        verbose_name_plural = "Email tasdiqlash"

    email = models.CharField(max_length=100, verbose_name="Email")
    code = models.CharField(max_length=10, verbose_name="Kod")


class TestModel(models.Model):
    class Meta:
        verbose_name = "Test uchun"
        verbose_name_plural = "Test uchun"
        db_table = "test"

    title = models.CharField(max_length=100, unique=False)
    image = models.ImageField()
