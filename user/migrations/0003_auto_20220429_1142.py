# Generated by Django 3.1.14 on 2022-04-29 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20220429_1138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cargo',
            options={'verbose_name': "Jo'natma", 'verbose_name_plural': "Jo'natmalar"},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Foydalanuvchi', 'verbose_name_plural': 'Foydalanuvchilar'},
        ),
        migrations.AlterField(
            model_name='cargo',
            name='from_kv',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='to_kv',
            field=models.PositiveIntegerField(),
        ),
    ]
