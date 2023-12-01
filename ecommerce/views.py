from django.shortcuts import render
from product.models import Product
from category.models import category
def homepage(request):
    product=Product.objects.filter(is_available=True)
    return render(request,"index.html",{'data':product,'catogery':category.objects.all()})