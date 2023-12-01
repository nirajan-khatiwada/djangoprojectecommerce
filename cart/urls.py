from django.urls  import path
from . import views
urlpatterns = [
    path("",views.cart,name="cart"),
    path("<slug:product_slug>",views.add_to_cart,name="addtocart"),
    path("delete/<slug:product_slug>",views.remove_cart,name="delete"),
    path("remove/<slug:product_slug>",views.delete,name="remove"),
    path("placeorder/",views.placeorder,name="placeorder")
]
