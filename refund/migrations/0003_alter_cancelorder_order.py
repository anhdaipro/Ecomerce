# Generated by Django 3.2.4 on 2021-08-30 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_order_canceled'),
        ('refund', '0002_cancelorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancelorder',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order'),
        ),
    ]