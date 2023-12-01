from django import forms
from .models import Variation
from product.models import Product

class ProductCustomSizeColor(forms.Form):
        def __init__(self, product_slug,*args, **kwargs):
            super().__init__(*args, **kwargs)


            size=[]
            color=[]
            variation = Variation.objects.filter(product__slug=product_slug)
            size=list(set([x.size for x in variation]))
            color=list(set([x.color for x in variation]))
            size=[[x,x] for x in size]
            color=[[x,x] for x in color]
           
            
            self.fields['color'] = forms.ChoiceField(
            required=True,
            choices=color,
            error_messages={'required': "This Field is Required"},
            widget=forms.RadioSelect(attrs={'name': 'radio_color'}),
            )
            self.fields['size'] = forms.ChoiceField(
            required=True,
            choices=size,
            error_messages={'required': "This Field is Required"},
            widget=forms.RadioSelect(attrs={'name': 'radio_size'}),
            )
            