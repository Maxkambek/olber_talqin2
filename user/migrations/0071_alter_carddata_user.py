# Generated by Django 4.0.4 on 2022-09-06 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0070_carddata_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carddata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card', to=settings.AUTH_USER_MODEL),
        ),
    ]
