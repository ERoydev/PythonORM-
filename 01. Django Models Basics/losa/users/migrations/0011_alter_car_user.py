# Generated by Django 5.0.4 on 2024-07-03 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_car'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='user',
            field=models.ManyToManyField(related_name='curr_user', to='users.user'),
        ),
    ]
