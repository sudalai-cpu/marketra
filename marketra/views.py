from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Product, Address, StyleProfile, Wishlist
from django.contrib.auth.decorators import login_required
import random

def home(request):
    # Featured products: top 4 by AI rank
    featured_products = Product.objects.all().order_by('ai_rank')[:4]
    
    # Recommended products: 4 random products
    recommended_products = Product.objects.all().order_by('?')[:4]
    
    # Get collection from session
    collection_ids = request.session.get('collection', [])
    collection_products = Product.objects.filter(id__in=collection_ids)
    
    context = {
        'featured_products': featured_products,
        'recommended_products': recommended_products,
        'collection_products': collection_products,
        'collection_count': len(collection_ids),
        'collection_ids': collection_ids,
    }
    return render(request, 'marketra/index.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Recommendations on detail page
    recommended_products = Product.objects.exclude(pk=pk).order_by('?')[:4]
    
    collection_ids = request.session.get('collection', [])
    in_collection = pk in collection_ids
    
    context = {
        'product': product,
        'categories': Category.objects.all(),
        'recommended_products': recommended_products,
        'in_collection': in_collection,
        'collection_count': len(collection_ids),
        'collection_ids': collection_ids,
        'in_wishlist': request.user.is_authenticated and request.user.wishlist.products.filter(pk=pk).exists() if hasattr(request.user, 'wishlist') else False,
    }
    return render(request, 'marketra/product_detail.html', context)

def add_to_collection(request, pk):
    if request.method == 'POST':
        collection = request.session.get('collection', [])
        if pk not in collection:
            collection.append(pk)
            request.session['collection'] = collection
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'count': len(collection)})
            
    return redirect('marketra:home')

def remove_from_collection(request, pk):
    if request.method == 'POST':
        collection = request.session.get('collection', [])
        if pk in collection:
            collection.remove(pk)
            request.session['collection'] = collection
            
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'count': len(collection)})
            
    return redirect('marketra:home')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('marketra:home')
    else:
        form = UserCreationForm()
    return render(request, 'marketra/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('marketra:home')
    else:
        form = AuthenticationForm()
    return render(request, 'marketra/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('marketra:home')
from .models import Product, Category

def featured_view(request):
    # Fetch all categories
    categories = Category.objects.all()
    
    # Get selected category from query params
    selected_category_id = request.GET.get('category')
    selected_category = None
    
    if selected_category_id:
        selected_category = get_object_or_404(Category, id=selected_category_id)
        featured_products = Product.objects.filter(category=selected_category).order_by('ai_rank')
    else:
        # Fetch all featured products
        featured_products = Product.objects.filter(is_featured=True).order_by('ai_rank')
        # If none marked as featured, fallback to top 12 by AI rank
        if not featured_products.exists():
            featured_products = Product.objects.all().order_by('ai_rank')[:12]
    
    collection_ids = request.session.get('collection', [])
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'selected_category': selected_category,
        'collection_count': len(collection_ids),
        'collection_ids': collection_ids,
    }
    return render(request, 'marketra/featured.html', context)
from django.db.models import Q

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct().order_by('ai_rank')
    
    collection_ids = request.session.get('collection', [])
    
    context = {
        'query': query,
        'results': results,
        'collection_count': len(collection_ids),
        'collection_ids': collection_ids,
    }
    return render(request, 'marketra/search.html', context)

def collection_view(request):
    collection_ids = request.session.get('collection', [])
    collection_products = Product.objects.filter(id__in=collection_ids)
    
    context = {
        'collection_products': collection_products,
        'collection_count': len(collection_ids),
        'collection_ids': collection_ids,
    }
    return render(request, 'marketra/collection.html', context)

def recommendations_view(request):
    recommended_products = Product.objects.all().order_by('?')[:12]  # Show more on standalone page
    collection_ids = request.session.get('collection', [])
    
    context = {
        'recommended_products': recommended_products,
        'collection_count': len(collection_ids),
        'collection_ids': collection_ids,
    }
    return render(request, 'marketra/recommendations.html', context)

@login_required
def dashboard(request):
    return render(request, 'marketra/dashboard/overview.html')

@login_required
def profile_view(request):
    addresses = request.user.addresses.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        street = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        if name and street and city:
            Address.objects.create(
                user=request.user,
                name=name,
                street_address=street,
                city=city,
                state=state,
                zip_code=zip_code
            )
            messages.success(request, "Address added successfully.")
            return redirect('marketra:profile')
            
    return render(request, 'marketra/dashboard/profile.html', {'addresses': addresses})

@login_required
def orders_view(request):
    # Retrieve user's past orders (Placeholder if Order model not implemented yet)
    return render(request, 'marketra/dashboard/orders.html')

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'marketra/dashboard/wishlist.html', {'wishlist': wishlist})

@login_required
def style_profile_view(request):
    profile, created = StyleProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.favorite_colors = request.POST.get('favorite_colors', '')
        profile.fashion_goals = request.POST.get('fashion_goals', '')
        
        # Handle simple size inputs for now - expecting form data keys like 'size_top'
        sizes = profile.sizes or {}
        if 'size_top' in request.POST:
            sizes['top'] = request.POST['size_top']
        if 'size_shoe' in request.POST:
            sizes['shoe'] = request.POST['size_shoe']
        profile.sizes = sizes
        
        # Simple keyword parsing from a text input
        keywords_raw = request.POST.get('style_keywords', '')
        if keywords_raw:
            profile.style_keywords = [k.strip() for k in keywords_raw.split(',')]
            
        profile.save()
        messages.success(request, "Style profile updated.")
        return redirect('marketra:style_profile')
        
    return render(request, 'marketra/dashboard/ai_style.html', {'profile': profile})

@login_required
def add_to_wishlist(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Added to wishlist'})
            
    return redirect('marketra:product_detail', pk=pk)

@login_required
def remove_from_wishlist(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.remove(product)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Removed from wishlist'})
            
    return redirect('marketra:wishlist')
