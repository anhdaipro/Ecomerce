# Generated by Django 3.2.4 on 2022-07-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0003_auto_20220717_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy_with_shock_deal',
            name='list_byproducts',
            field=models.TextField(null=True),
        ),
    ]
