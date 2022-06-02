
from django.db import models
from product.models import Variant,Item,Shop
from account.models import User
from django.conf import settings
from django_countries.fields import CountryField
# Create your models here.
class WhishItem(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity=models.SmallIntegerField(default=1)
    create_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"(self.quantity) of (self.variany)"

class OrderItem(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,null=True,related_name='shop_order')
    product=models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity=models.SmallIntegerField()
    updated_at = models.DateField(auto_now=True) 
    ordered=models.BooleanField(default=False)
    check=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.quantity} of {self.product.name} {self.product.shop}"

    def price_item(self):
        return self.quantity * self.product.price
    def discount_price_item(self):
        return self.quantity * self.product.discount_price
    def save_item(self):
        return self.price_item() - self.discount_price_item()
    def final_price_item(self):
        if product.discount_price:
            return self.discount_price_item()
        return self.price_item()
DEFAULT_SHIPPING_ID = 1
class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,null=True,related_name='order_shop')
    ordered=models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    shipping = models.ForeignKey(
        'Shipping',on_delete=models.CASCADE,default=DEFAULT_SHIPPING_ID)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    canceled=models.BooleanField(default=False)
    check=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.ref_code)
    def not_price(self):
        return 0
    def total_price(self):
        total=0
        for order_item in self.items.all():
            if order_item.check==True:
                total += order_item.discount_price_item()
        return total

    def total_final(self):
        total=0
        for order_item in self.items.all():
            if order_item.check==True:
                total += order_item.discount_price_item() 
                if self.coupon :
                    total -= self.coupon.amount 
        return total

    def total_final_shipping(self):
        total=0
        for order_item in self.items.all():
            if order_item.check==True:
                total += order_item.discount_price_item()
                if self.coupon and self.shipping:
                    total = total - self.coupon.amount + self.shipping.charge
                elif self.shipping:
                    total = total + self.shipping.charge 
        return total
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    phone_number=models.PositiveIntegerField(null=True)
    country = CountryField(multiple=False,null=True)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES,null=True)
    zip = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural = 'Addresses'
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal'),
    ('After','Payment on delivery')
)
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(choices=PAYMENT_CHOICES,max_length=10,null=True)
    def __str__(self):
        return str(self.user)

class Shipping(models.Model):
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='shipping',null=True)
    method=models.CharField(max_length=100)
    shipping_unit = models.CharField(max_length=1000)
    charge=models.FloatField()
    

class Coupon(models.Model):
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='coupon',null=True)
    code = models.CharField(max_length=15)
    amount = models.FloatField()
    active=models.BooleanField(default=False)
    valid_from=models.DateTimeField(null=True)
    valid_to=models.DateTimeField(null=True)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.code


