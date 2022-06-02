from django.contrib import admin
from .models import Refund,CancelOrder
# Register your models here.
class RefundAdmin(admin.ModelAdmin):
    list_display=['user','order','email','accepted']
    actions=['set_accepted_true']
    def set_accepted_true(self,request,queryset):
        queryset.update(accepted=True)
admin.site.register(Refund,RefundAdmin)
admin.site.register(CancelOrder)
