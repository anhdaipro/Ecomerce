# Generated by Django 3.2.4 on 2022-07-11 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0016_shop_description_url'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_type', models.CharField(choices=[('All', 'All shop'), ('Product', 'Product')], max_length=10)),
                ('name_of_the_discount_program', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=5)),
                ('active', models.BooleanField(default=False)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('discount_type', models.CharField(choices=[('1', 'Percent'), ('2', 'Money')], max_length=15, null=True)),
                ('amount', models.FloatField(null=True)),
                ('percent', models.FloatField(null=True)),
                ('maximum_usage', models.IntegerField(null=True)),
                ('voucher_type', models.CharField(choices=[('Offer', 'Offer'), ('Complete coin', 'Complete coin')], max_length=15)),
                ('minimum_order_value', models.IntegerField(default=0)),
                ('maximum_discount', models.IntegerField(null=True)),
                ('setting_display', models.CharField(choices=[('Show many', 'Show many places'), ('Not public', 'not public'), ('Share', 'Share througth code vourcher')], max_length=20)),
                ('created', models.DateTimeField(auto_now=True)),
                ('product', models.ManyToManyField(blank=True, related_name='voucher', to='shop.Item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
                ('user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Shop_program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_program', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('product', models.ManyToManyField(blank=True, related_name='shop_program', to='shop.Item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Shop_award',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('type_voucher', models.CharField(default='Offer', max_length=100)),
                ('discount_type', models.CharField(choices=[('1', 'Percent'), ('2', 'Money')], max_length=15, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('percent', models.FloatField(blank=True, null=True)),
                ('minimum_order_value', models.IntegerField(null=True)),
                ('code_number', models.IntegerField(default=1)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
                ('user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion_combo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_combo_name', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('combo_type', models.CharField(choices=[('1', 'percentage discount'), ('2', 'discount by amount'), ('3', 'special sale')], max_length=100)),
                ('discount_percent', models.IntegerField(blank=True, null=True)),
                ('discount_price', models.IntegerField(blank=True, default=0, null=True)),
                ('price_special_sale', models.IntegerField(null=True)),
                ('limit_order', models.IntegerField(default=100)),
                ('quantity_to_reduced', models.IntegerField(default=2)),
                ('created', models.DateTimeField(auto_now=True)),
                ('product', models.ManyToManyField(blank=True, related_name='promotion_combo', to='shop.Item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Follower_offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('type_offer', models.CharField(default='Voucher', max_length=100)),
                ('discount_type', models.CharField(choices=[('1', 'Percent'), ('2', 'Money')], max_length=15, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('percent', models.FloatField(blank=True, null=True)),
                ('voucher_type', models.CharField(choices=[('Offer', 'Offer'), ('Complete coin', 'Complete coin')], max_length=15)),
                ('maximum_discount', models.CharField(choices=[('L', 'Limited'), ('U', 'Unlimited')], max_length=15)),
                ('max_price', models.IntegerField(null=True)),
                ('minimum_order_value', models.IntegerField(null=True)),
                ('maximum_usage', models.IntegerField(null=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
                ('user', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flash_sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now=True)),
                ('product', models.ManyToManyField(blank=True, related_name='flash_sale', to='shop.Item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Buy_with_shock_deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shock_deal_type', models.CharField(choices=[('1', 'Buy With Shock Deal'), ('2', 'Buy to receive gifts')], default='1', max_length=100)),
                ('program_name_buy_with_shock_deal', models.CharField(max_length=100)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('limited_product_bundles', models.IntegerField(null=True)),
                ('minimum_price_to_receive_gift', models.IntegerField(default=0, null=True)),
                ('number_gift', models.IntegerField(default=0, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('byproduct', models.ManyToManyField(blank=True, related_name='byproduct', to='shop.Item')),
                ('main_product', models.ManyToManyField(blank=True, related_name='main_product', to='shop.Item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop')),
            ],
        ),
    ]