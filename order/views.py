import json
from django.http import request
from stripe.api_resources import charge
from django.db.models import  Q
from order.form import CouponForm,CheckoutForm,PaymentForm,ShippingForm,AddCartForm,CheckForm
from django.db.models import Max, Min, Count, Avg
from django.views import generic
from .models import WhishItem,OrderItem,Order,Variant,Coupon,Payment,Address,User,Shipping,Shop
from django.http.response import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  View
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import stripe
from django.conf import settings
import random
import string
import datetime
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

def create_ref_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=14))

def sendEmail(request, order):
    mail_subject = 'Thank you for your order!'
    message = render_to_string('order/order_recieved_email.html', {
        'user': request.user,
        'order': order
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.fil(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True,
            }
            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "order/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("order:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.fil(user=self.request.user, ordered=False)
            if form.is_valid():
                phone_number=form.cleaned_data.get('phone_number')
                name=form.cleaned_data.get('name')
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "No default shipping address available")
                        return redirect('order:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    city = form.cleaned_data.get('city')
                    if is_valid_form([shipping_address1]):
                        shipping_address = Address(
                            user=self.request.user,
                            address=shipping_address1,
                            city=city,
                            name=name,
                            phone_number=phone_number,
                            address_type='S'
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()
                elif use_default_billing:
                    print("Using the deault billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request, "No default billing address available")
                        return redirect('order:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get('billing_address')
                    city2 = form.cleaned_data.get('city2')
                    if is_valid_form([billing_address1]):
                        billing_address = Address(
                            user=self.request.user,
                            address=billing_address1,
                            city=city2,
                            name=name,
                            phone_number=phone_number,
                            address_type='B'
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()
                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')
                if payment_option == 'S':
                    return redirect('order:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('order:payment', payment_option='paypal')
                elif payment_option == 'After':
                    payment = Payment(
                    user=self.request.user,
                    amount=order.total_final_shipping(),
                    payment_method="A"
                    )
                    payment.save()
                    order.ordered = True
                    order.payment=payment
                    order.ref_code = create_ref_code()
                    order.save()
                    order_items = order.items.all()
                    order_items.update(ordered=True)
                            
                    for item in order_items:
                        item.save()   
                        products=Variant.objects.get(orderitem=item.id)
                        products.stock -= item.quantity
                        products.save()
                    messages.success(self.request,'success payment')
                    return redirect('/')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("order:order-summary")

def payment_complete(request):
    body = json.loads(request.body)
    print('BODY :', body)
    order = Order.objects.fil(
        user=request.user, ordered=False, id=body['orderID'])
    payment = Payment(
        user=request.user,
        stripe_charge_id=body['payID'],
        amount=order.total_final_shipping(),
        payment_method="P"
    )
    payment.save()

    order.payment = payment
    order.ordered = True
    order.ref_code = create_ref_code()
    order.save()
    order_items = order.items.all()
    order_items.update(ordered=True)     
    for item in order_items:
        item.save()   
        products=Variant.objects.get(orderitem=item.id)
        products.stock -= item.quantity
        products.save()
    sendEmail(request=request, order=order)
    messages.success(request, "payment was successful")
    return redirect('/')       
        
class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.fil(user=self.request.user, ordered=False)
        context = {
            'order': order,
            "DISPLAY_COUPON_FORM": False
        }
        return render(self.request, 'order/payment.html', context)

    def post(self, *args, **kwargs):
        order = Order.objects.fil(user=self.request.user, ordered=False)
        try:
            customer = stripe.Customer.create(
                email=self.request.user.email,
                description=self.request.user.username,
                source=self.request.POST['stripeToken']
            )
            amount = int(order.total_final_shipping() * 100)
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                customer=customer,
                description="Test payment for buteks online",
            )
            payment = Payment(
                user=self.request.user,
                stripe_charge_id=charge['id'],
                amount=order.total_final_shipping(),
                payment_method="S"
            )
            payment.save()
            order.ordered = True
            order.payment = payment
            order.ref_code = create_ref_code()
            order.save()
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()
                products=Variant.objects.get(orderitem=item.id)
                products.stock -= item.quantity
                products.save()
            messages.success(self.request, "payment was successful")
            return redirect('/')
        except stripe.error.CardError as e:
            messages.info(self.request, f"{e.error.message}")
            return redirect('/')
        except stripe.error.InvalidRequestError as e:
            messages.success(self.request, "Invalid request")
            return redirect('/')
        except stripe.error.AuthenticationError as e:
            messages.success(self.request, "Authentication error")
            return redirect('/')
        except stripe.error.APIConnectionError as e:
            messages.success(self.request, "Check your connection")
            return redirect('/')
        except stripe.error.StripeError as e:
            messages.success(
                self.request, "There was an error please try again")
            return redirect('/')
        except Exception as e:
            messages.success(
                self.request, "A serious error occured we were notified")
            return redirect('/')
    
class WhishItemView(generic.View):
    login_url = '/account/signin/'
    def get(self,request):
        whish_item=WhishItem.objects.filter(user=request.user)
        context={ 'whish_item':whish_item}
        return render(request,'order/order.html',context)
    
class OrderSummaryView(LoginRequiredMixin,View):
    login_url = '/account/signin/'
    def get(self, requset, *args, **kwargs):
        try:
            time_reorder=10
            time_quarter=90
            time_month=30
            order = Order.objects.filter(user=self.request.user, ordered=False)
            order_shop = Order.objects.filter(user=self.request.user,ordered=False)
            shops=Shop.objects.filter(variants__orderitem__order__in=order_shop)
            orders = Order.objects.filter(user=self.request.user,canceled=True).count()
            if orders >0:
                time_start=Order.objects.filter(user=self.request.user,ordered=True).first().ordered_date
                time_end=Order.objects.filter(user=self.request.user,ordered=True).last().ordered_date
                time=(time_end-time_start).days
                current_time=timezone.now()
                times=(current_time-time_end).days
                return render(requset, 'order/order_summary.html',{'time':time,'times':times})
            products=Variant.objects.annotate(count=Count('likeed')).filter(count__gte=2)
            context = {
                'object': order,
                'products':products,
                'couponform': CouponForm(),
                
                'orders':orders,
                
                'time_reorder':time_reorder,
                'time_quarter':time_quarter,
                'time_month':time_month,
                'shops':shops,
            }
            return render(requset, 'order/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(requset, "You do not have an active order")
            return redirect("/")

@login_required(login_url='/account/signin/') 
def check(request)  :
     if request.method=='POST':
        color=request.POST.get('color')
        form=CheckForm(request.POST)
        if form.is_valid():
            order_item=OrderItem.objects.get(id=color)
            order_item.check=form.cleaned_data.get('check')
            order_item.save()
            return HttpResponseRedirect(reverse('order:order_summary'))




def check_order(request):
    if request.method=='POST':
        form=CheckForm(request.POST)
        if form.is_valid():
            order = Order.objects.filter(user=request.user, ordered=False)
            order.check=form.cleaned_data.get('check')
            order.save()
            for order_item in order.items.all():
                if order.check==True:
                    order_item.check=True
                else:
                    order_item.check=False
                order_item.save()
            return HttpResponseRedirect(reverse('order:order_summary'))
@login_required(login_url='/account/signin/')
def add_to_cart(request):
    url = request.META.get('HTTP_REFERER')
    if request.method=='POST':
        color=request.POST.get('color')
        quantity= request.POST.get('quantity')
        product=Variant.objects.get(id=color)
        try:
            order_item=OrderItem.objects.get(
                product=product,
                user=request.user,
                ordered=False,
                )
            order_item.quantity =order_item.quantity+int(quantity)
            order_item.save()
            if order_item.quantity>order_item.product.stock:
                order_item.quantity-=int(quantity)
                order_item.save()
                messages.error(request,'over quantity')
                return redirect(url)
            else:
                messages.success(request,'item has update')
                return redirect(url)
        except Exception:
            form=AddCartForm(request.POST)
            if form.is_valid():
                order_item=OrderItem.objects.create(
                product=product,
                user=request.user,
                ordered=False,
                quantity=form.cleaned_data['quantity'],
                shop=product.shop,
                )
                order_qs = Order.objects.filter(Q(user=request.user) & Q(ordered=False))
                if order_qs.exists():
                    order = order_qs[0]
                    if order.items.filter(Q(product = product,shop=product.shop)):
                        order.items.add(order_item)
                        return redirect(url)
                    else:
                        ordered_date = timezone.now()
                        order = Order.objects.filate(
                        user=request.user, ordered_date=ordered_date,ordered=False,shop=order_item.shop)
                        order.items.add(order_item)
                        return redirect(url)
                else:    
                    ordered_date = timezone.now()
                    order = Order.objects.filate(
                    user=request.user, ordered_date=ordered_date,ordered=False,shop=order_item.shop)
                    order.items.add(order_item)
                    messages.info(request, "This item was added to your cart.")
                    return redirect(url)
            
def shop_check(request):
    if request.method=='POST':
        name=request.POST.get('name')
        
        form=CheckForm(request.POST)
        if form.is_valid():
            shop=Shop.objects.get(name=name)
            order=OrderItem.objects.filter(user=request.user,ordered=False)
            shop.check=form.cleaned_data.get('check')
            shop.save()
            for order_item in order:
                if str(shop.name)==str(order_item.shop) and shop.check==True:
                    order_item.check=True
                    order_item.save()
                else:
                    order_item.check=False
                order_item.save()
            return HttpResponseRedirect(reverse('order:order_summary'))

@login_required(login_url='/account/signin/')
def remove_from_cart(request):
    if request.method=='POST':
        color=request.POST.get('color')
        order_item=OrderItem.objects.get(id=color)
        order_item.delete()
        return HttpResponseRedirect(reverse('order:order_summary'))
        
        
@login_required(login_url='/account/signin/')
def remove_single_item_from_cart(request):
    if  request.method=='POST':
        color=request.POST.get('color')
        order_item=OrderItem.objects.get(id=color)
        if order_item.quantity==1:
            order_item.delete()
        else:
            order_item.quantity -=1
            order_item.save()
        return HttpResponseRedirect(reverse('order:order_summary'))
    
@login_required(login_url='/account/signin/')
def add_single_item_from_cart(request):
    if  request.method=='POST':
        color=request.POST.get('color')
        order_item=OrderItem.objects.get(id=color)
        order_item.quantity +=1
        order_item.save()
        return redirect('order:order_summary')

class AddCouponView(View):
    def post(self,request):
        url = request.META.get('HTTP_REFERER')
        coupon_form= CouponForm(request.POST)
        if coupon_form.is_valid():
            try:
                current_time=timezone.now()
                code=coupon_form.cleaned_data.get('code')
                coupon_object=Coupon.objects.get(code=code)
                order=Order.objects.fil(user=request.user,ordered=False)
                if coupon_object.valid_to >= current_time and coupon_object.active == True and order.total_price() > 0:
                    order.coupon=coupon_object
                    order.save()
                    messages.success(self.request, "Successfully added coupon")
                    return redirect(url)
                else:
                    messages.info(request, "This coupon exprite")
                    return redirect(url)
            except ObjectDoesNotExist:
                messages.info(self.request, "coupon doesn't exist")
                return redirect(url)

def shipping(request):
    if request.method=="POST":
        method=request.POST.get('method') 
        shipping=Shipping.objects.get(method=method)
        order=Order.objects.fil(user=request.user,ordered=False)
        order.shipping=shipping
        order.save()
        return redirect('order:checkout')

    
        
              