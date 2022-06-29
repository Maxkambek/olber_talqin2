from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from user.calculation import calc_distance
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER_CHOICES = (
        ("client", "Mijoz"),
        ("worker", "Ishchi"),
        ("driver", "Haydovchi")
    )
    CAR_TYPES = (
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
    works = ArrayField(models.CharField(max_length=50), null=True, blank=True)
    status = models.BooleanField(default=False)
    car_type = models.CharField(max_length=15, verbose_name="Mashina turi", choices=CAR_TYPES, default="S")
    drive_doc = models.ImageField(verbose_name="Guvohnoma", null=True, blank=True)
    car_image_1 = models.ImageField(verbose_name="Mashina rasmi", null=True, blank=True)
    car_image_2 = models.ImageField(verbose_name="Mashina rasmi", null=True, blank=True)
    account = models.CharField(max_length=50, null=True, blank=True)
    money = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.count > 0:
            self.rating = (self.point)/int(self.count)
            self.rating = round(self.rating, 1)
            super(User, self).save(*args, **kwargs)
        else:
            self.rating = 0
            self.point = 0
            super(User, self).save(*args, **kwargs)


class Cargo(models.Model):
    class Meta:
        verbose_name = _("Jo'natma")
        verbose_name_plural = _("Jo'natmalar")

    STATUS_CHOICES = (
        ('new', "Yangi"),
        ('selected', "Tanlangan"),
        ('finished', "Yopilgan"),
    )
    TYPE_CHOICES = (
        ('disabled', "Tanlanmagan"),
        ('small', "Kichik"),
        ('big', "Katta"),
        ('ice_car', "Sovutgich"),
    )
    user = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    price = models.PositiveIntegerField(verbose_name=_('Price'))
    weight = models.PositiveIntegerField()
    from_address = models.CharField(max_length=255)
    address_from = models.CharField(max_length=255)
    from_floor = models.PositiveIntegerField()
    from_kv = models.PositiveIntegerField()
    from_persons = models.PositiveIntegerField()
    to_address = models.CharField(max_length=255)
    address_to = models.CharField(max_length=255)
    to_floor = models.PositiveIntegerField()
    to_kv = models.PositiveIntegerField()
    to_persons = models.PositiveIntegerField()
    time_when = models.CharField(max_length=35)
    description = models.TextField(verbose_name="Tafsilot")
    image1 = models.ImageField()
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="new")
    cargo_type = models.CharField(max_length=100, null=True, choices=TYPE_CHOICES, default="disabled")
    distance = models.FloatField(null=True, blank=True)
    offers = models.ManyToManyField(User, verbose_name="Takliflar", null=True, blank=True)
    doer = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='workes')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.distance = calc_distance(self.from_address, self.to_address)
        self.distance = round(self.distance, 2)
        super(Cargo, self).save(*args, **kwargs)


class Work(models.Model):
    STATUS_CHOICES = (
        ('new', "Yangi"),
        ('selected', "Tanlangan"),
        ('finished', "Yopilgan"),
    )
    user = models.ForeignKey(User, verbose_name="Ish beruvchi", on_delete=models.CASCADE, related_name='workss')
    title = models.CharField(max_length=150, verbose_name='Nomi')
    price = models.PositiveIntegerField(verbose_name='Narxi')
    image = models.ImageField()
    address = models.CharField(max_length=150)
    lat_lon = models.CharField(max_length=50)
    work_time = models.CharField(max_length=55)
    description = models.TextField(verbose_name="Tafsilot")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='new')
    offers = models.ManyToManyField(User, verbose_name="Takliflar", null=True, blank=True)
    doer = models.ForeignKey(User, blank=True, null=True, verbose_name="Bajaruvchi", on_delete=models.CASCADE, related_name="jobs")


class VerifyEmail(models.Model):
    class Meta:
        verbose_name = _("Email tasdiqlash")
        verbose_name_plural = _("Email tasdiqlash")

    email = models.CharField(max_length=100, verbose_name="Email")
    code = models.CharField(max_length=10, verbose_name="Kod")
