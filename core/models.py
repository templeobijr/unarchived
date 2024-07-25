from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    is_brand = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Avoiding conflict with 'auth.User.groups'
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Avoiding conflict with 'auth.User.user_permissions'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class BrandProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='brands')
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

class WardrobeItem(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='wardrobe_items/')

    def __str__(self):
        return f'{self.product.name} - {self.owner.username}'