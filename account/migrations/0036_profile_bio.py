# Generated by Django 3.2.4 on 2022-10-18 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0035_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(null=True),
        ),
    ]
