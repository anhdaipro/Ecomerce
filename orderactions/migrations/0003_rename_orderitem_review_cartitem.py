# Generated by Django 3.2.4 on 2022-07-12 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orderactions', '0002_alter_review_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='orderitem',
            new_name='cartitem',
        ),
    ]