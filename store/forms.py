from django import forms
from store.models import User,Categorymodel,Productmodel


class User_reg_form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']

class Loginform(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class Category_form(forms.ModelForm):
    class Meta:
        model=Categorymodel
        fields="__all__"

class Product_form(forms.ModelForm):
    class Meta:
        model=Productmodel
        fields="__all__"

class orderform(forms.Form):
    address=forms.Textarea()