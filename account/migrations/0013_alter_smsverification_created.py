# Generated by Django 3.2.4 on 2022-04-19 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_smsverification_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsverification',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]