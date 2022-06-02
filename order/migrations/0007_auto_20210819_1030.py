# Generated by Django 3.2.4 on 2021-08-19 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_address_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mobile',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]