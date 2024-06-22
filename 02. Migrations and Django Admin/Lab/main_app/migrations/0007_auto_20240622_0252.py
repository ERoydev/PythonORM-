# Generated by Django 5.0.4 on 2024-06-21 23:52

from django.db import migrations
import random


class Migration(migrations.Migration):

    def generate_barcodes(apps, schema_editor):
        Product = apps.get_model('main_app', 'Product')
        all_products = Product.objects.all()

        all_barcodes = random.sample(range(100000000, 1000000000), len(all_products))

        for i in range(len(all_products)):
            product = all_products[i]
            product.barcode = all_barcodes[i]
            product.save()

    def reverse_barcodes(apps, schema_editor):
        Product = apps.get_model('main_app', 'Product')

        for prod in Product.objects.all():
            if prod.barcode != 0:
                prod.barcode = 0

                prod.save()


    dependencies = [
        ('main_app', '0006_product_barcode'),
    ]

    operations = [
        migrations.RunPython(generate_barcodes, reverse_code=reverse_barcodes)
    ]
