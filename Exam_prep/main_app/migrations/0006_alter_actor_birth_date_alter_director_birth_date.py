# Generated by Django 5.0.4 on 2024-07-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_actor_birth_date_alter_director_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='birth_date',
            field=models.DateField(default='1900-01-01'),
        ),
        migrations.AlterField(
            model_name='director',
            name='birth_date',
            field=models.DateField(default='1900-01-01'),
        ),
    ]
