# Generated by Django 4.0.6 on 2025-05-08 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('canteen', '0010_schoolholidaycredit'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyAdjustments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('holiday_date', models.DateField(blank=True, null=True)),
                ('considered_next_month', models.BooleanField(default=False)),
                ('month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='SchoolHolidayCredit',
        ),
    ]
