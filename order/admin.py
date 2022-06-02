from django.contrib import admin
from .models import OrderItem,Order,Payment,Coupon,Address,Shipping
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ref_code','ordered','being_delivered','canceled','received','refund_requested','refund_granted','shipping_address',
                    'billing_address','payment','coupon','ordered_date']
    list_display_links = ['user','shipping_address','billing_address','payment','coupon']
    list_filter = ['ordered','being_delivered','received','refund_requested','refund_granted']
    search_fields = ['user__username','ref_code']

    actions = ['set_order_received','set_order_being_delivered']

    def set_order_received(self,request,queryset):
        queryset.update(received=True)

    def set_order_being_delivered(self,request,queryset):
        queryset.update(being_delivered=True)
class CartAdmin(admin.ModelAdmin):
    list_display  = ['user','product','quantity',]
class CouponAdmin(admin.ModelAdmin):
    list_display  = ['code','valid_from','valid_to','active']
    list_filter = ['valid_from','valid_to']
    search_fields = ['code']
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['user','amount','timestamp','stripe_charge_id']
    search_fields = ['stripe_charge_id']
class AddressAdmin(admin.ModelAdmin):
    list_display  = ['id','user','name','address_type']
    
admin.site.register(OrderItem,CartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(Shipping)
admin.site.register(Address,AddressAdmin)



