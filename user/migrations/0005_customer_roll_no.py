# Generated by Django 4.0.6 on 2025-04-07 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_customer_roll_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='roll_no',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
