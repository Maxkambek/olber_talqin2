from django.db import models
from user.calculation import calc_distance
from user.models import User
from django.utils.translation import gettext_lazy as _


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
        ('S', "S"),
        ('M', "M"),
        ('L', "L"),
        ('XL', "XL"),
        ('XXL', "XXL"),
    )
    user = models.ForeignKey(User, verbose_name="Foydalanuvchi", on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    price = models.PositiveIntegerField(verbose_name=_('Price'))
    weight = models.PositiveIntegerField()
    from_address = models.CharField(max_length=255)
    address_from = models.CharField(max_length=255)
    from_floor = models.PositiveIntegerField(default=0)
    from_kv = models.PositiveIntegerField()
    to_address = models.CharField(max_length=255)
    address_to = models.CharField(max_length=255)
    to_floor = models.PositiveIntegerField(default=0)
    to_kv = models.PositiveIntegerField()
    time_when = models.CharField(max_length=35)
    description = models.TextField(verbose_name="Tafsilot", blank=True)
    image1 = models.ImageField()
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="new")
    cargo_type = models.CharField(max_length=100, null=True, choices=TYPE_CHOICES, default="S")
    distance = models.FloatField(null=True, blank=True)
    offers = models.ManyToManyField(User, verbose_name="Takliflar", null=True, blank=True)
    doer = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='workes')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.distance = calc_distance(self.from_address, self.to_address)
        self.distance = round(self.distance, 2)
        super(Cargo, self).save(*args, **kwargs)