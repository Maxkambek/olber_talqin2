# Generated by Django 3.1.14 on 2022-06-28 09:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0050_auto_20220627_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='offers',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='Takliflar'),
        ),
    ]
