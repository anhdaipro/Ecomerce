# Generated by Django 3.2.4 on 2021-09-08 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0027_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='check',
            field=models.BooleanField(default=False),
        ),
    ]