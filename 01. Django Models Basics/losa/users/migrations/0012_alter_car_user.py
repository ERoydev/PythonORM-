# Generated by Django 5.0.4 on 2024-07-03 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_car_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='user',
            field=models.ManyToManyField(related_name='car', to='users.user'),
        ),
    ]
