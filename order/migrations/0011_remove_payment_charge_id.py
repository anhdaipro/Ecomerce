# Generated by Django 3.2.4 on 2021-08-24 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_payment_charge_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='charge_id',
        ),
    ]