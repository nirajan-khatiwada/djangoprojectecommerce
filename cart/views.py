from django.shortcuts import render
from category.models import category
from product.models import Product
from cart.models import Cart,CartItem
from django.urls import reverse
from store.models import Variation
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from order.forms import OrderForm


from django.http import Http404,HttpResponse
from store.forms import ProductCustomSizeColor

# Create your views here.
def remove_cart(request,product_slug):
    if request.method=="POST":
            customshapesizeform=ProductCustomSizeColor(product_slug,request.POST)
            if(not customshapesizeform.is_valid()):
                return redirect(reverse("cart"))
            if customshapesizeform.is_valid():
                try:
                    if request.user.is_authenticated:
                        delete=CartItem.objects.get(is_ordered=False,product__slug=product_slug,user=request.user,variation__size=customshapesizeform.cleaned_data.get('size'),variation__color=customshapesizeform.cleaned_data.get('color'))
                    else:
                        delete=CartItem.objects.get(is_ordered=False,product__slug=product_slug,cart__cart_id=request.session.session_key,variation__size=customshapesizeform.cleaned_data.get('size'),variation__color=customshapesizeform.cleaned_data.get('color'))
                    if(delete.quantity>1):
                        delete.quantity=delete.quantity-1
                        delete.save()
                    else:
                        delete.delete()
                    return redirect(reverse("cart"))
                except:
                    return redirect(reverse("cart"))

def delete(request,product_slug):
    if request.method=="POST":
            customshapesizeform=ProductCustomSizeColor(product_slug,request.POST)
            if(not customshapesizeform.is_valid()):
                return redirect(reverse("cart"))
            if customshapesizeform.is_valid():
                try:
                    if request.user.is_authenticated:
                        delete=CartItem.objects.get(is_ordered=False,product__slug=product_slug,user=request.user,variation__size=customshapesizeform.cleaned_data.get('size'),variation__color=customshapesizeform.cleaned_data.get('color'))
                    else:
                        delete=CartItem.objects.get(is_ordered=False,product__slug=product_slug,cart__cart_id=request.session.session_key,variation__size=customshapesizeform.cleaned_data.get('size'),variation__color=customshapesizeform.cleaned_data.get('color'))
                    delete.delete()
                    return redirect(reverse("cart"))
                except:
                    return redirect(reverse("cart"))
        

def add_to_cart(request,product_slug):
        if request.method=="POST":
            customshapesizeform=ProductCustomSizeColor(product_slug,request.POST)
            if(not customshapesizeform.is_valid()):
                return redirect(reverse("cart"))
            if customshapesizeform.is_valid():
                products=Product.objects.get(slug=product_slug)
                try:
                    if not(request.session.session_key):
                        request.session.create()
        
                    session=request.session.session_key

                    carts=Cart.objects.get(cart_id=session)
                except:
                    carts=Cart.objects.create(cart_id=session)
                try:
                    variations_data=Variation.objects.get(product=products,color=customshapesizeform.cleaned_data.get('color'),size=customshapesizeform.cleaned_data.get('size'))
                except:
                    variations_data=Variation.objects.create(product=products,color=customshapesizeform.cleaned_data.get('color'),size=customshapesizeform.cleaned_data.get('size'))



                
                try:
                    if request.user.is_authenticated:
                        cart_items=CartItem.objects.get(is_ordered=False,product=products,user=request.user,variation=variations_data)
                    else:
                        cart_items=CartItem.objects.get(is_ordered=False,product=products,cart=carts,variation=variations_data)
                    cart_items.quantity=cart_items.quantity+1
                    cart_items.save()
                except:
                    if request.user.is_authenticated:
                        cart_items=CartItem.objects.create(is_ordered=False,product=products,user=request.user,quantity=1,variation=variations_data)
                    else:

                        cart_items=CartItem.objects.create(is_ordered=False,product=products,cart=carts,quantity=1,variation=variations_data)
                return redirect(reverse("cart"))
            
        
    

def cart(request,total=0,quantity=0,cart_iteams=None):
    try:
        
        if(request.user.is_authenticated):
            data=CartItem.objects.filter(user=request.user,is_ordered=False)
          
        else:
            cart_items=Cart.objects.get(cart_id=request.session.session_key)
            data=CartItem.objects.filter(cart=cart_items,is_ordered=False)
        
        for carts in data:
            total=total+carts.subtotal()
            tax=13/100*total
        grandtotal=total+tax
        return render(request,"cart/cart.html",{'catogery':category.objects.all(),'data':data,'grandtotal':grandtotal,'tax':tax,'total':total})
    except:
        return render(request,"cart/cart.html",{'catogery':category.objects.all(),'data':None,'grandtotal':0,'tax':0,'total':0})

    
    
@login_required(login_url="login")
def placeorder(request,total=0,quantity=0,cart_iteams=None):
    data=CartItem.objects.filter(user=request.user,is_ordered=False)
    if(data.count()==0):
        return redirect(reverse("cart"))

    form=OrderForm()
    try:
        data=CartItem.objects.filter(user=request.user,is_ordered=False) 
        for carts in data:
            total=total+carts.subtotal()
            tax=13/100*total
        grandtotal=total+tax
        return render(request,"cart/place-order.html",{'catogery':category.objects.all(),'data':data,'grandtotal':grandtotal,'tax':tax,'total':total,'form':form})
    except:
        return render(request,"cart/place-order.html",{'catogery':category.objects.all(),'data':None,'grandtotal':0,'tax':0,'total':0,'form':form})