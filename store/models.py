from django.db import models
from product.models import Product

# Create your models here.
class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_varation")
    size=models.CharField(max_length=50,null=True)
    color=models.CharField(max_length=50,null=True)

    
    def __str__(self):
        return f'{self.product} of size {self.size} and color {self.color}'
