from django.shortcuts import render
from product.models import Product
from django.http import Http404,HttpResponse
from category.models import category
from .forms import ProductCustomSizeColor

# Create your views here.

def store(request):
    min=request.GET.get('min')
    max=request.GET.get('max')
    if(min and max):
        product=Product.objects.filter(is_available=True,price__lte=max,price__gte=min)
    else:
        product=Product.objects.filter(is_available=True)
    return render(request,"store/store.html",{'data':product,'len_product':len(product),'catogery':category.objects.all()})

def category_display(request,category_slug):
    try:
        product_category=category.objects.get(category_name=category_slug)
        category_product=product_category.product.filter(is_available=True)
        return render(request,"store/store.html",{'data':category_product,'len_product':len(category_product),'catogery':category.objects.all()})
    except:
        raise Http404()

def product_display(request,category_slug,product_slug):
    try:
        shapeandsize=ProductCustomSizeColor(product_slug)
        data=Product.objects.get(catogery__slug=category_slug,slug=product_slug)
        return render(request,"store/product-detail.html",{'catogery':category.objects.all(),'data':data,'form':shapeandsize})
    except:
        raise Http404()

