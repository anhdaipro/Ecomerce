# Generated by Django 3.2.4 on 2022-07-30 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0012_alter_award_shop_award'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follower_offer',
            old_name='maximun_discount',
            new_name='maximum_discount',
        ),
    ]
