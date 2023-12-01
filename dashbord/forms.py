from django import forms


class Cpassword(forms.Form):
    password=forms.CharField(min_length=8,required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    cpassword=forms.CharField(min_length=8,required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))