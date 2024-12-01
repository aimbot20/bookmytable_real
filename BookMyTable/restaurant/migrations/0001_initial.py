# Generated by Django 5.1.1 on 2024-11-29 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0004_alter_customer_options_alter_owner_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('M_ID', models.AutoField(primary_key=True, serialize=False)),
                ('M_TotalItems', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Door',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_position', models.IntegerField()),
                ('y_position', models.IntegerField()),
                ('D_Length', models.IntegerField()),
                ('D_Width', models.IntegerField(default=5)),
                ('layout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doors', to='restaurant.layout')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('D_ID', models.AutoField(primary_key=True, serialize=False)),
                ('D_Name', models.CharField(max_length=100)),
                ('D_Description', models.TextField(blank=True, null=True)),
                ('D_Price', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('D_PrepTime', models.IntegerField()),
                ('D_Category', models.CharField(max_length=100)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='restaurant.menu')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('R_ID', models.AutoField(primary_key=True, serialize=False)),
                ('R_Name', models.CharField(max_length=100)),
                ('R_EmailAddress', models.EmailField(max_length=254, unique=True)),
                ('R_ContactNumber', models.CharField(max_length=15, unique=True)),
                ('R_Address', models.TextField()),
                ('R_Description', models.TextField(blank=True, null=True)),
                ('R_CuisineTypes', models.CharField(max_length=100)),
                ('R_ReservationCost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('R_OpenHours', models.CharField(max_length=100)),
                ('Rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('NetRevenue', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='users.owner')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to='restaurant.restaurant'),
        ),
        migrations.AddField(
            model_name='layout',
            name='restaurant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='layout', to='restaurant.restaurant'),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_position', models.IntegerField()),
                ('y_position', models.IntegerField()),
                ('T_SeatingCapacity', models.IntegerField()),
                ('is_reserved', models.BooleanField(default=False)),
                ('color', models.CharField(choices=[('red', 'Reserved'), ('blue', 'Available'), ('yellow', 'Selected')], default='blue', max_length=6)),
                ('layout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='restaurant.layout')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_position', models.IntegerField()),
                ('y_position', models.IntegerField()),
                ('W_Length', models.IntegerField()),
                ('W_Width', models.IntegerField(default=5)),
                ('layout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='windows', to='restaurant.layout')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
