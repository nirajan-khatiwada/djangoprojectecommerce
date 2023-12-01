from django.db import models

# Create your models here.
from django.db import models
from account.models import Account
from store.models import Product, Variation
from cart.models import CartItem


class OrderAddress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.address_line_1},{self.state}'
    


class Order(models.Model):
    STATUS = (
        ('Paid', 'Paid'),
        ('Deliverred', 'Delivered'),
        ('Cancaled',"Cancaled"),
        ("Ongoing",'Ongoing')
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order_number = models.AutoField(primary_key=True)
    Address=models.ForeignKey(OrderAddress,on_delete=models.CASCADE,null=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')

    
    def __str__(self):
        return str(self.user.first_name)


