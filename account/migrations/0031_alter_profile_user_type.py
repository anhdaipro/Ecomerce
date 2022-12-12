# Generated by Django 3.2.4 on 2022-04-26 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_alter_profile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(blank=True, choices=[('C', 'Customer'), ('S', 'Seller')], default='C', max_length=10),
        ),
    ]