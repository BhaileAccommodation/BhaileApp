# Generated by Django 4.0.1 on 2022-01-16 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_booking_date_booked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('TWN', 'Twin'), ('SIN', 'Single'), ('DOB', 'Double'), ('SIN-EN', 'Single EnSuite'), ('DOB-EN', 'Double EnSuite'), ('HSE', 'Whole House')], max_length=6, null=True),
        ),
    ]
