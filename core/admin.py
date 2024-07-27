from django.contrib import admin
from .models import CustomUser, BrandProfile, WardrobeItem, Product, ProductImage

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')


class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)

class WardrobeItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')
    list_filter = ('created_at',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_profile', 'price', 'created_at')
    search_fields = ('name', 'brand_profile__name')
    list_filter = ('created_at', 'brand_profile')

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'created_at')
    search_fields = ('product__name',)
    list_filter = ('created_at',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BrandProfile, BrandProfileAdmin)
admin.site.register(WardrobeItem, WardrobeItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
