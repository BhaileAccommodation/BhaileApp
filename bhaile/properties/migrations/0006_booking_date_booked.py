# Generated by Django 4.0.1 on 2022-01-16 20:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0005_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='date_booked',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
