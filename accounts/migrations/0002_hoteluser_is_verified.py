# Generated by Django 5.1 on 2024-08-26 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoteluser',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
