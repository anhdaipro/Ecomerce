from . import views
from django.urls import path
from .views import RequestRefundView
app_name = 'refund'
urlpatterns = [
path('refund/',RequestRefundView.as_view(), name='request_refund'),]