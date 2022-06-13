# Generated by Django 4.0.4 on 2022-06-11 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0032_user_car_image_1_user_car_image_2_user_car_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='car_type',
            field=models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], default='S', max_length=15, verbose_name='Mashina turi'),
        ),
    ]