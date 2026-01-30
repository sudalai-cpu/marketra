from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Product
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
    }
    return render(request, 'marketra/search.html', context)
