# Generated by Django 5.1.1 on 2024-11-17 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customer_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
        migrations.AlterModelOptions(
            name='owner',
            options={'verbose_name': 'Owner', 'verbose_name_plural': 'Owners'},
        ),
    ]
