from django.db import models

from user.models import User


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
    description = models.TextField(verbose_name="Tafsilot", blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='new')
    offers = models.ManyToManyField(User, verbose_name="Takliflar", null=True, blank=True)
    doer = models.ForeignKey(User, blank=True, null=True, verbose_name="Bajaruvchi", on_delete=models.CASCADE, related_name="jobs")
