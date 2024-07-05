# Generated by Django 5.0.4 on 2024-07-05 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_product_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DrivingLicense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=10, unique=True)),
                ('issue_date', models.DateField()),
                ('driver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='license', to='main_app.drivinglicense')),
            ],
        ),
    ]
