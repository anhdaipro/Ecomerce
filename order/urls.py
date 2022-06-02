from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import OrderSummaryView,AddCouponView,PaymentView,CheckoutView
app_name = 'order'
urlpatterns = [
    path('order_sumary/',OrderSummaryView.as_view(),name='order_summary'),
    path('add_to_cart/', views.add_to_cart ,name='add_to_cart') ,
    path('remove_single_product_from_cart/',views.remove_single_item_from_cart,name='remove_single_item_from_cart'),
    path('add_single_product_from_cart/',views.add_single_item_from_cart,name='add_single_item_from_cart'),
    path('remove_from_cart/',views.remove_from_cart,name='remove_from_cart'),
    path('payment-complete/',views.payment_complete, name="payment_complete"),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('add-coupon/',AddCouponView.as_view(),name='add_coupon'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('shipping/', views.shipping, name='shipping'),
    path('check/', views.check, name='check'),
    path('shop_check/', views.shop_check, name='shop_check'),
    path('check_order/', views.check_order, name='check_order'),
    
]