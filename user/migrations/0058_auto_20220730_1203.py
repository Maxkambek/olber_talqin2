# Generated by Django 3.1.14 on 2022-07-30 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0057_auto_20220730_1140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='from_persons',
        ),
        migrations.RemoveField(
            model_name='cargo',
            name='to_persons',
        ),
    ]