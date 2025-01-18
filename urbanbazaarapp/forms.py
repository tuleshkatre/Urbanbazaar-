from django import forms
from .models import User , Profile , Product
from django.contrib.auth.forms import UserCreationForm  


class SignupForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICE, required=True)
    password2 = forms.CharField(label="Confirm Password (again)", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity' , 'category' , 'image']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity' , 'image']


class User_update_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']








