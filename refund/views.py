from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView, View
from .form import RefundForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.conf import settings
# Create your views here.

class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form, 
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
            form = RefundForm(self.request.POST,self.request.FILES)
            if form.is_valid():
                ref_code = form.cleaned_data.get('ref_code')
                message = form.cleaned_data.get('message')
                email  = form.cleaned_data.get('email')
                image=form.cleaned_data.get('image')
                # edit the order
                try:
                    order = Order.objects.get(ref_code=ref_code,received=True,refund_requested=False,user=self.request.user)
                    order.refund_requested = True
                    order.save()
                    # store the refund
                    refund = Refund()
                    refund.order = order
                    refund.reason = message
                    refund.email = email
                    refund.image=image
                    refund.user=self.request.user
                    refund.save()

                    messages.info(self.request, "Your request was received.")
                    return redirect("refund:request_refund")

                except ObjectDoesNotExist:
                    messages.info(self.request, "This order does not exist.")
                    return redirect("refund:request_refund")

    
