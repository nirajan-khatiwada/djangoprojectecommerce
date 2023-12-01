from django.shortcuts import render
from . import forms
from django.template.loader import render_to_string
from uuid import uuid4
from cart.models import CartItem
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from .models import Order,OrderAddress
from django.shortcuts import redirect
from requests import post
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
def payment(request,total=0):
    try:
        print("error here")
        if request.method=="POST":
            form=forms.OrderForm(request.POST)
            if form.is_valid():
                try:
                    OrderAddress.objects.get(user=request.user,country=form.cleaned_data.get('country'),
                                                      state =form.cleaned_data.get('state'),
                                                     address_line_1 =form.cleaned_data.get('address_line_1'),
                                                    city = form.cleaned_data.get('city'))


                except:
                    OrderAddress.objects.create(user=request.user,country=form.cleaned_data.get('country'),
                                                      state =form.cleaned_data.get('state'),
                                                     address_line_1 =form.cleaned_data.get('address_line_1'),
                                                    city = form.cleaned_data.get('city'))
                data=CartItem.objects.filter(user=request.user,is_ordered=False) 
                for carts in data:
                    total=total+carts.subtotal()
                    tax=13/100*total
                    grandtotal=total+tax
                host=f'http://{request.META["HTTP_HOST"]}'
                
                header={ 'Authorization':'key live_secret_key_68791341fdd94846a146f0457ff7b455'}
                url = "https://a.khalti.com/api/v2/epayment/initiate/"
                payload ={
                        "return_url": f'{host}{reverse("verify")}',
                        "website_url": f"{host}/",
                        "amount": int(grandtotal*100),
                        "purchase_order_id": str(uuid4()),
                        "purchase_order_name": "Cart",
                        "customer_info": {
                        "name": f"{request.user.first_name} {request.user.last_name}",
                        "email": request.user.email,
                        "phone": request.user.phone_number}
                          }
                response=post(url,json=payload,headers=header)
                res=response.json()
                print(res)
                return redirect(res['payment_url'])
                
                 
                
                 
            else:
               
                return redirect(reverse("placeorder"))
    except:
        print("error here")
        return redirect(reverse("placeorder"))


@login_required(login_url="login")
def verify(request,total=0,grandtotal=0,tax=0):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    data={"pidx":request.GET.get("pidx")}
    header={ 'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455'}
    response=post(url,json=data,headers=header)
    res=response.json()
    
    if res.get('status')=="Completed":
        orderaddr=OrderAddress.objects.filter(user=request.user).first()
        
        data=CartItem.objects.filter(user=request.user,is_ordered=False) 
        
        for carts in data:
            total=total+carts.subtotal()
            tax=13/100*total
            grandtotal=total+tax
        if int(grandtotal*100)==res.get('total_amount'):
            data=CartItem.objects.filter(user=request.user,is_ordered=False)
            for x in data:
                x.product.stock=x.product.stock-x.quantity
                x.product.save()
                x.is_ordered=True
                x.save()
            Order.objects.create(user=request.user,Address=orderaddr,order_total=grandtotal,tax=tax,status="Paid")
        else:
            return  redirect(reverse("cart"))
        #cart=CartItem.objects.filter(request.user)
        
        data=render_to_string("order/order_complete.html",{'order':orderaddr,'total':total,'grandtotal':grandtotal,'tax':tax,'status':'paid','request':request})
        email=EmailMultiAlternatives("Invoices Of Product","Product detail","nepcart invoices <usa.nirajankhatiwada29@gmail.com>",to=[request.user.email])
        email.attach_alternative(data,'text/html')
        email.send()
        return redirect(reverse("homepage"))
    else:
        return redirect(reverse("placeorder"))