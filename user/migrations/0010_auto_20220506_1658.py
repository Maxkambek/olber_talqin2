# Generated by Django 3.1.14 on 2022-05-06 11:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20220506_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to=settings.AUTH_USER_MODEL, verbose_name='Foydalanuvchi'),
        ),
    ]
