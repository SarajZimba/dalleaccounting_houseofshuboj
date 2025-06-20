# Generated by Django 4.0.6 on 2025-04-18 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_product_lunch_type'),
        ('user', '0007_customer_discount_applicable'),
        ('canteen', '0008_tblmissedattendance_considered_next_month_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblmissedattendance_butcharged',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('Lunchtype', models.CharField(blank=True, max_length=255, null=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('missed_date', models.DateField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.customer')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
