from django.db import models
from category.models import category
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50,blank=True,editable=False)
    description=models.CharField(max_length=250)
    price=models.IntegerField()
    image=models.ImageField(upload_to="product/image")
    stock=models.IntegerField()
    is_available=models.BooleanField()
    catogery=models.ForeignKey(category,on_delete=models.CASCADE,related_name="product")
    created_date=models.DateField(auto_now=True)
    modefied_date=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.product_name
    def save(self,*args,**kwargs):
        self.slug=slugify(self.product_name)
        super().save(*args,**kwargs)
    

