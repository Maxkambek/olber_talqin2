# Generated by Django 3.1.14 on 2022-05-05 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220505_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='image1',
            field=models.ImageField(upload_to=''),
        ),
    ]