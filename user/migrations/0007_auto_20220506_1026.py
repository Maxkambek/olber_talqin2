# Generated by Django 3.1.14 on 2022-05-06 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_cargo_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_email_verified',
            new_name='is_verified',
        ),
    ]
