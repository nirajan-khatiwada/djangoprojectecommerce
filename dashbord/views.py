from django.shortcuts import render
from category.models import category
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from order.models import OrderAddress
from .forms import Cpassword
from account.models import Account
from django.contrib import messages
# Create your views here.

@login_required(login_url="login")
def dashbord(request,total=0,tax=0,grandtotal=0):
    data=CartItem.objects.filter(user=request.user,is_ordered=True)
    orderaddr=OrderAddress.objects.filter(user=request.user).order_by("-id").first()
    print(orderaddr)
    for carts in data:
        total=total+carts.subtotal()
        tax=13/100*total
        grandtotal=total+tax
    return render(request,"dashboard/dashboard.html",{'catogery':category.objects.all(),'total':total,'tax':tax,'grandtotal':grandtotal,'orderaddr':orderaddr})

@login_required(login_url="login")
def order(request,total=0,tax=0,grandtotal=0):
    data=CartItem.objects.filter(user=request.user,is_ordered=True)
    orderaddr=OrderAddress.objects.filter(user=request.user).order_by("id")
    return render(request,"dashboard/order.html",{'catogery':category.objects.all(),'data':data})


@login_required(login_url="login")
def changepassword(request,total=0,tax=0,grandtotal=0):
    form=Cpassword()
    if request.method=="POST":
        form=Cpassword(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            cpassword=form.cleaned_data['cpassword']
            if password==cpassword:
                user=Account.objects.get(username=request.user.username)
                user.set_password(password)
                messages.success(request,"Password changes sucessfully")
            else:
                messages.error(request,"Password and Confirm Password doesnt match")



    return render(request,"dashboard/change.html",{'catogery':category.objects.all(),'form':form})

