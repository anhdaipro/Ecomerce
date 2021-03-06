# Generated by Django 3.2.4 on 2021-09-18 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0050_alter_variant_likeed'),
        ('order', '0030_payment_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupon', to='product.shop'),
        ),
        migrations.AddField(
            model_name='shipping',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shipping', to='product.shop'),
        ),
    ]
