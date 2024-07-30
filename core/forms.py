from django import forms # type: ignore
from .models import CustomUser, BrandProfile, Product, WardrobeItem, Category, BrandCategory
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'is_brand', 'profile_picture', 'bio']  # Include additional fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user
    
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_brand', 'profile_picture', 'bio']
    
class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = BrandProfile
        fields = ['name', 'description', 'logo', 'category']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'description']

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