# Generated by Django 3.2.4 on 2021-09-20 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0055_shop_followers'),
        ('order', '0032_orderitem_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_order', to='product.shop'),
        ),
    ]
