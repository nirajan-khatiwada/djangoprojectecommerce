from django.db import models
from product.models import Product
from store.models import Variation
from account.models import Account

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=50)
    date=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name="user",null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation=models.ForeignKey(Variation,on_delete=models.CASCADE,related_name="variation")
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="carts",null=True)
    quantity=models.IntegerField()
    is_ordered=models.BooleanField(default=False)

    def subtotal(self):
        return self.product.price*self.quantity

    def __str__(self):
        return self.product.product_name
    