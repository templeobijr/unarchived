from django import forms # type: ignore
from .models import CustomUser, BrandProfile, Product, WardrobeItem, Category, BrandCategory
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'is_brand', 'profile_picture', 'bio']

class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = BrandProfile
        fields = ['name', 'description', 'logo', Category]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'description', Category]

class WardrobeItemForm(forms.ModelForm):
    class Meta:
        model = WardrobeItem
        fields = ['product', 'name', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class BrandCategoryForm(forms.ModelForm):
    class Meta:
        model = BrandCategory
        fields = ['name', 'description']