# Generated by Django 3.1.14 on 2022-05-11 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_cargo_cargo_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='cargo_type',
            field=models.CharField(choices=[('null', 'Tanlanmagan'), ('small', 'Kichik'), ('big', 'Katta'), ('ice_car', 'Sovutgich'), ('worker', 'Ishchi')], default='null', max_length=100, null=True),
        ),
    ]
