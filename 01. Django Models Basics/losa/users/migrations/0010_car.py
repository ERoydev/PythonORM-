# Generated by Django 5.0.4 on 2024-07-03 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_user_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=30)),
                ('registration_number', models.CharField(max_length=10)),
                ('user', models.ManyToManyField(to='users.user')),
            ],
        ),
    ]
