# Generated by Django 5.0.4 on 2024-06-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0019_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='warranty',
            field=models.CharField(default='No warranty', max_length=50),
        ),
    ]