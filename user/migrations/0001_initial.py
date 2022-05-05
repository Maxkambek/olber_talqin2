# Generated by Django 3.1.14 on 2022-05-05 04:53

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_email_verified', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('price', models.CharField(max_length=150)),
                ('weight', models.CharField(max_length=10)),
                ('from_adrress', models.CharField(max_length=255)),
                ('from_floor', models.PositiveIntegerField()),
                ('from_kv', models.PositiveIntegerField()),
                ('from_persons', models.PositiveIntegerField()),
                ('to_adrress', models.CharField(max_length=255)),
                ('to_floor', models.PositiveIntegerField()),
                ('to_kv', models.PositiveIntegerField()),
                ('to_persons', models.PositiveIntegerField()),
                ('when', models.DateField()),
                ('description', models.TextField(verbose_name='Tafsilot')),
                ('image1', models.ImageField(upload_to='')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='')),
                ('status', models.CharField(choices=[('new', "Ko'rib chiqilmoqda"), ('sent', "Yo'lda"), ('finished', 'Yopilgan')], default='new', max_length=25)),
                ('distance', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': "Jo'natma",
                'verbose_name_plural': "Jo'natmalar",
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_type', models.CharField(choices=[('1', 'Kichik'), ('2', "O'rta"), ('3', 'Katta')], max_length=15, verbose_name='Mashina turi')),
                ('drive_license', models.CharField(max_length=50, verbose_name='Guvohnoma raqami')),
                ('drive_doc', models.CharField(max_length=50, verbose_name='Guvohnoma raqami')),
                ('tech_inspect', models.CharField(max_length=50, verbose_name="Texnik ko'rik")),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Haydovchi')),
            ],
        ),
    ]
