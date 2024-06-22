# Generated by Django 5.0.6 on 2024-06-21 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.RemoveField(
            model_name='user',
            name='childrens',
        ),
        migrations.RemoveField(
            model_name='user',
            name='description',
        ),
        migrations.RemoveField(
            model_name='user',
            name='salary',
        ),
        migrations.AddField(
            model_name='user',
            name='number',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
