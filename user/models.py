from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from user.calculation import calc_distance


class User(AbstractUser):
    USER_CHOICES = (
        ("client", "Mijoz"),
        ("worker", "Ishchi"),
        ("driver", "Haydovchi")
    )

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    is_verified = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.CharField(choices=USER_CHOICES, max_length=25, default="client")
    rating = models.FloatField(verbose_name="Reyting", validators=[MinValueValidator(0.0), MaxValueValidator(5.0)], default=0)
    point = models.FloatField(verbose_name="Umumiy ball", default=0)
    count = models.IntegerField(verbose_name="Ishlar soni", default=1)
    works = ArrayField(models.CharField(max_length=50), null=True, blank=True)

    def save(self, *args, **kwargs):
        self.rating = (self.point)/(self.count)
        self.rating = round(self.rating, 1)
        super(User, self).save(*args, **kwargs)


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
    price = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    from_address = models.CharField(max_length=255)
    from_floor = models.PositiveIntegerField()
    from_kv = models.PositiveIntegerField()
    from_persons = models.PositiveIntegerField()
    to_address = models.CharField(max_length=255)
    to_floor = models.PositiveIntegerField()
    to_kv = models.PositiveIntegerField()
    to_persons = models.PositiveIntegerField()
    time_when = models.CharField(max_length=55)#DateField()
    description = models.TextField(verbose_name="Tafsilot")
    image1 = models.ImageField()
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="new")
    cargo_type = models.CharField(max_length=100, null=True, choices=TYPE_CHOICES, default="disabled")
    distance = models.FloatField(null=True, blank=True)
    offers = models.ManyToManyField(User, verbose_name="Takliflar", null=True, blank=True)
    doer = models.PositiveIntegerField(default=0)

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
