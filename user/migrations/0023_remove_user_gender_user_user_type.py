# Generated by Django 4.0.4 on 2022-06-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0022_cargo_doer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('client', 'Mijoz'), ('worker', 'Ishchi'), ('driver', 'Haydovchi')], default='client', max_length=25),
        ),
    ]