# Generated by Django 4.1.3 on 2022-11-08 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_price_product_unit_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='promotions',
            field=models.ManyToManyField(blank=True, null=True, related_name='promotions_products', to='shop.promotion'),
        ),
    ]