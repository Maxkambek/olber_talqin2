# Generated by Django 4.0.4 on 2022-08-30 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0063_alter_cargo_description_alter_cargo_description_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='car_number',
            field=models.CharField(default='01A000AA', max_length=8, verbose_name='Davlat raqami'),
            preserve_default=False,
        ),
    ]
