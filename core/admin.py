from django.contrib import admin
from .models import CustomUser, BrandProfile, Product, WardrobeItem

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_brand')
    search_fields = ('username', 'email')
    list_filter = ('is_brand',)

@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price')
    search_fields = ('name', 'brand__name')
    list_filter = ('brand',)

@admin.register(WardrobeItem)
class WardrobeItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'product')
    search_fields = ('name', 'owner__username', 'product__name')
    list_filter = ('owner', 'product')
