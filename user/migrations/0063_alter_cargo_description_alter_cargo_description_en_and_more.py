# Generated by Django 4.0.4 on 2022-08-25 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0062_alter_user_car_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='description',
            field=models.TextField(blank=True, verbose_name='Tafsilot'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Tafsilot'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Tafsilot'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='description_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Tafsilot'),
        ),
        migrations.AlterField(
            model_name='user',
            name='car_type',
            field=models.CharField(choices=[('0', '0'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], default='0', max_length=15, verbose_name='Mashina turi'),
        ),
        migrations.AlterField(
            model_name='work',
            name='description',
            field=models.TextField(blank=True, verbose_name='Tafsilot'),
        ),
    ]
