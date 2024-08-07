# Generated by Django 5.0.4 on 2024-07-23 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(related_name='actors', to='main_app.actor'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='starring_actor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.actor'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='storyline',
            field=models.TextField(null=True),
        ),
    ]
