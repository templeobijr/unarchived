from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, BrandProfile, Product, WardrobeItem, Category, BrandCategory
from .forms import CustomUserCreationForm, CustomUserForm, BrandProfileForm, ProductForm, WardrobeItemForm
from django.db.models import Q

def home(request):
    brands = BrandProfile.objects.all()
    return render(request, 'core/home.html', {'brands': brands})

def brand_detail(request, pk):
    brand = get_object_or_404(BrandProfile, pk=pk)
    return render(request, 'core/brand_detail.html', {'brand': brand})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/product_detail.html', {'product': product})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'core/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all()
    return render(request, 'core/category_detail.html', {'category': category, 'products': products})

def brand_category_list(request):
    categories = BrandCategory.objects.all()
    return render(request, 'core/brand_category_list.html', {'categories': categories})

def brand_category_detail(request, pk):
    category = get_object_or_404(BrandCategory, pk=pk)
    brands = category.brands.all()
    return render(request, 'core/brand_category_detail.html', {'category': category, 'brands': brands})
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
@login_required
def profile(request):
    user = request.user
    if user.is_brand:
        return redirect('brand_owner_profile')
    else:
        return redirect('normal_user_profile')

@login_required
def brand_owner_profile(request):
    user = request.user
    brand_profiles = user.brands.all()
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, request.FILES, instance=user)
        brand_form = BrandProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and brand_form.is_valid():
            user_form.save()
            brand = brand_form.save(commit=False)
            brand.user = user
            brand.save()
            return redirect('brand_owner_profile')
    else:
        user_form = CustomUserForm(instance=user)
        brand_form = BrandProfileForm()
    return render(request, 'core/brand_owner_profile.html', {'user_form': user_form, 'brand_form': brand_form, 'brand_profiles': brand_profiles})

@login_required
def normal_user_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect('normal_user_profile')
    else:
        user_form = CustomUserCreationForm(instance=user)
    wardrobe_items = WardrobeItem.objects.filter(owner=user)
    return render(request, 'core/normal_user_profile.html', {'user_form': user_form, 'wardrobe_items': wardrobe_items})

@login_required
def dashboard(request):
    user = request.user
    if user.is_brand:
        brands = user.brands.all()
        brand_profile = user.brands.first()
        products = brand_profile.products.all() if brand_profile else []
        return render(request, 'core/dashboard.html', {'brands': brands, 'brand_profile': brand_profile, 'products': products})
    else:
        wardrobe_items = WardrobeItem.objects.filter(owner=user)
        return render(request, 'core/dashboard.html', {'wardrobe_items': wardrobe_items})

@login_required
def add_brand(request):
    if request.method == 'POST':
        form = BrandProfileForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.user = request.user
            brand.save()
            return redirect('dashboard')
    else:
        form = BrandProfileForm()
    return render(request, 'core/add_brand.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.brand = request.user.brands.first()
            product.save()
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})

@login_required
def add_wardrobe_item(request):
    if request.method == 'POST':
        form = WardrobeItemForm(request.POST, request.FILES)
        if form.is_valid():
            wardrobe_item = form.save(commit=False)
            wardrobe_item.owner = request.user
            wardrobe_item.save()
            return redirect('dashboard')
    else:
        form = WardrobeItemForm()
    return render(request, 'core/add_wardrobe_item.html', {'form': form})

@login_required
def edit_brand(request, pk):
    brand = get_object_or_404(BrandProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BrandProfileForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = BrandProfileForm(instance=brand)
    return render(request, 'core/edit_brand.html', {'form': form})

@login_required
def delete_brand(request, pk):
    brand = get_object_or_404(BrandProfile, pk=pk, user=request.user)
    if request.method == 'POST':
        brand.delete()
        return redirect('dashboard')
    return render(request, 'core/delete_brand.html', {'brand': brand})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, brand__user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/edit_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, brand__user=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard')
    return render(request, 'core/delete_product.html', {'product': product})

@login_required
def edit_wardrobe_item(request, pk):
    wardrobe_item = get_object_or_404(WardrobeItem, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = WardrobeItemForm(request.POST, request.FILES, instance=wardrobe_item)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = WardrobeItemForm(instance=wardrobe_item)
    return render(request, 'core/edit_wardrobe_item.html', {'form': form})

@login_required
def delete_wardrobe_item(request, pk):
    wardrobe_item = get_object_or_404(WardrobeItem, pk=pk, owner=request.user)
    if request.method == 'POST':
        wardrobe_item.delete()
        return redirect('dashboard')
    return render(request, 'core/delete_wardrobe_item.html', {'wardrobe_item': wardrobe_item})

def explore(request):
    new_drops = BrandProfile.objects.order_by('-created_at')[:10]
    top_brands = BrandProfile.objects.all()  # Customize this as per your logic for top brands
    context = {
        'new_drops': new_drops,
        'top_brands': top_brands
    }
    return render(request, 'core/explore.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        brand_results = BrandProfile.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        product_results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        brand_results = BrandProfile.objects.none()
        product_results = Product.objects.none()
    
    context = {
        'brand_results': brand_results,
        'product_results': product_results,
        'query': query,
    }
    return render(request, 'core/search_results.html', context)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'core/add_category.html', {'form': form})
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'core/settings.html', {'form': form})