# Generated by Django 3.1.14 on 2022-06-26 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0045_auto_20220625_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='count',
            field=models.IntegerField(default=0, verbose_name='Ishlar soni'),
        ),
    ]
