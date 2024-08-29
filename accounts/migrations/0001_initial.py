# Generated by Django 5.1 on 2024-08-25 04:47

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ameneties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenetie_name', models.CharField(max_length=100)),
                ('icon', models.ImageField(upload_to='hotels')),
            ],
        ),
        migrations.CreateModel(
            name='Hoteluser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.ImageField(upload_to='profiles')),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('email_token', models.CharField(blank=True, max_length=50, null=True)),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HotelVendor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('profile_picture', models.ImageField(upload_to='profiles')),
                ('phone_number', models.CharField(max_length=100, unique=True)),
                ('email_token', models.CharField(blank=True, max_length=50, null=True)),
                ('otp', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=100)),
                ('hotel_description', models.TextField()),
                ('hotel_slug', models.SlugField(max_length=100, unique=True)),
                ('hotel_price', models.FloatField()),
                ('hotel_offer_price', models.FloatField()),
                ('hotel_location', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('ameneties', models.ManyToManyField(to='accounts.ameneties')),
                ('hotel_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='accounts.hotelvendor')),
            ],
        ),
        migrations.CreateModel(
            name='HotelImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_images', to='accounts.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='HotelManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_name', models.CharField(max_length=100)),
                ('manager_contact', models.CharField(max_length=100)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_managers', to='accounts.hotel')),
            ],
        ),
    ]
