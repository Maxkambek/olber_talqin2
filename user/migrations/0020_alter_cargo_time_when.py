# Generated by Django 4.0.4 on 2022-06-07 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_rename_when_cargo_time_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='time_when',
            field=models.CharField(max_length=55),
        ),
    ]