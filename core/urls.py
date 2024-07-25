from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('brand/<int:pk>/', views.brand_detail, name='brand_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/brand/', views.brand_owner_profile, name='brand_owner_profile'),
    path('profile/normal/', views.normal_user_profile, name='normal_user_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('brand/add/', views.add_brand, name='add_brand'),
    path('product/add/', views.add_product, name='add_product'),
    path('brand/edit/<int:pk>/', views.edit_brand, name='edit_brand'),
    path('brand/delete/<int:pk>/', views.delete_brand, name='delete_brand'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('wardrobe/add/', views.add_wardrobe_item, name='add_wardrobe_item'),
    path('wardrobe/edit/<int:pk>/', views.edit_wardrobe_item, name='edit_wardrobe_item'),
    path('wardrobe/delete/<int:pk>/', views.delete_wardrobe_item, name='delete_wardrobe_item'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('explore/', views.explore, name='explore'),
]
