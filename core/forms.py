from django import forms
from .models import CustomUser, BrandProfile, Product, WardrobeItem

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'is_brand', 'profile_picture', 'bio']
class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = BrandProfile
        fields = ['name', 'description', 'logo']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'description']

class WardrobeItemForm(forms.ModelForm):
    class Meta:
        model = WardrobeItem
        fields = ['product', 'name', 'image']