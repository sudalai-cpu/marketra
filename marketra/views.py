from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Product, Address, StyleProfile, Wishlist, Collection, ViewHistory
from django.contrib.auth.decorators import login_required
import random

from marketra.models import Collection

from django.shortcuts import render, get_object_or_404
from .recommender import get_hybrid_recommendations
from django.db.models import Q, Prefetch
 


def home(request):
    # 1. Featured products logic (AI Rank padi edukkurom)
    featured_products = Product.objects.all().order_by('ai_rank')[:4]
    
    # 2. Collection IDs check
    collection_ids = request.session.get('collection', [])
    if request.user.is_authenticated and hasattr(request.user, 'collection'):
        collection_ids = list(request.user.collection.products.values_list('id', flat=True))

    ai_product_objects = []
    ai_picks_text = ""

    if request.user.is_authenticated:
        # 3. Namma puthu Hybrid AI logic-ah call pandrom
        # Ithu automatic-ah database similarity-ah check pannum
        recommended_data = get_hybrid_recommendations(request.user, num_rec=4)
        
        if recommended_data:
            # recommended_data-la irunthu products-ah mattum extract pannuvom
            ai_product_objects = [item['product'] for item in recommended_data]
            ai_picks_text = "AI-Powered Curation: Based on your recent interests."
        else:
            ai_picks_text = "Explore our shop for personalized recommendations!"
            ai_product_objects = Product.objects.all().order_by('?')[:2]
    else:
        ai_picks_text = "Login to see AI-powered curation just for you."
        ai_product_objects = Product.objects.all().order_by('?')[:2]

    context = {
        'featured_products': featured_products,
        'collection_ids': collection_ids,
        'collection_count': len(collection_ids),
        'ai_recommendations_text': ai_picks_text,
        'ai_products': ai_product_objects, 
        # Frontend-la score venumna direct-ah 'recommended_data'-vum anuppalaam
    }
    
    return render(request, 'marketra/index.html', context)



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.user.is_authenticated:
        # Interaction Tracking for AI input
        ViewHistory.objects.create(
            user=request.user,
            product=product,
            product_name=product.name,
            category=product.category.name if product.category else "General",
            interaction_type='view',
            strength=1
        )

    context = {
        'product': product,
        'categories': Category.objects.all(),
        'in_collection': request.user.is_authenticated and hasattr(request.user, 'collection') and request.user.collection.products.filter(pk=pk).exists(),
        'in_wishlist': request.user.is_authenticated and hasattr(request.user, 'wishlist') and request.user.wishlist.products.filter(pk=pk).exists(),
    }
    return render(request, 'marketra/product_detail.html', context)

def toggle_collection(request, pk):
    print(f"DEBUG: toggle_collection called for pk={pk} user={request.user}")
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        status = None
        count = 0
        
        if request.user.is_authenticated:
            # Database logic for logged-in users
            product = get_object_or_404(Product, pk=pk)
            collection_obj, created = Collection.objects.get_or_create(user=request.user)
            
            if collection_obj.products.filter(pk=pk).exists():
                collection_obj.products.remove(product)
                status = 'removed'
            else:
                collection_obj.products.add(product)
                status = 'added'
            
            count = collection_obj.products.count()
            print(f"DEBUG: DB Collection updated. Status={status}, Count={count}")
            
        else:
            # Session logic for anonymous users
            collection = request.session.get('collection', [])
            print(f"DEBUG: Current session collection before: {collection}")
            
            if pk in collection:
                collection.remove(pk)
                status = 'removed'
            else:
                collection.append(pk)
                status = 'added'
            
            request.session['collection'] = collection
            request.session.modified = True
            count = len(collection)
            print(f"DEBUG: Session Collection updated. Status={status}, New collection: {collection}")

        if is_ajax:
            return JsonResponse({'status': 'success', 'action': status, 'count': count})
            
    return redirect('marketra:home')

def remove_from_collection(request, pk):
    if request.method == 'POST':
        count = 0
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=pk)
            collection_obj, created = Collection.objects.get_or_create(user=request.user)
            if collection_obj.products.filter(pk=pk).exists():
                collection_obj.products.remove(product)
            count = collection_obj.products.count()
        else:
            collection = request.session.get('collection', [])
            if pk in collection:
                collection.remove(pk)
                request.session['collection'] = collection
                request.session.modified = True
            count = len(collection)
            
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'count': count})
            
    return redirect('marketra:collection')

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
from .models import Product, Category, Section

def featured_view(request):
    # Fetch all sections with their categories prefetched for hierarchy, ordered by display_order
    sections = Section.objects.prefetch_related(
        Prefetch('categories', queryset=Category.objects.order_by('display_order'))
    ).order_by('display_order')
    
    # Fetch all featured products
    featured_products = Product.objects.filter(is_featured=True).order_by('ai_rank')
    # If none marked as featured, fallback to top 12 by AI rank
    if not featured_products.exists():
        featured_products = Product.objects.all().order_by('ai_rank')[:12]
    
    collection_ids = request.session.get('collection', [])
    
    # Fetch random products for discovery section
    random_products = Product.objects.all().order_by('?')[:8]
    
    context = {
        'sections': sections,
        'featured_products': featured_products,
        'collection_count': len(collection_ids),
        'collection_ids': collection_ids,
        'random_products': random_products,
    }
    return render(request, 'marketra/featured.html', context)

def category_products_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    section = category.section
    
    # Fetch all categories related to this section for the sidebar
    # If no section is assigned, just show the current category
    if section:
        categories = section.categories.all().order_by('display_order')
    else:
        categories = [category]
        
    sort_by = request.GET.get('sort', 'best_match') # Default to AI Rank
    
    products = Product.objects.filter(category=category)
    
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else: # best_match / ai_rank
        products = products.order_by('ai_rank')
        
    collection_ids = request.session.get('collection', [])
    if request.user.is_authenticated and hasattr(request.user, 'collection'):
        collection_ids = list(request.user.collection.products.values_list('id', flat=True))
        
    context = {
        'category': category,
        'section': section,
        'categories': categories,
        'products': products,
        'sort_by': sort_by,
        'collection_count': len(collection_ids),
        'collection_ids': collection_ids,
    }
    return render(request, 'marketra/category_products.html', context)

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
    collection_products = []
    collection_ids = []
    
    if request.user.is_authenticated:
        if hasattr(request.user, 'collection'):
            collection_products = request.user.collection.products.all()
            collection_ids = list(collection_products.values_list('id', flat=True))
    else:
        collection_ids = request.session.get('collection', [])
        collection_products = Product.objects.filter(id__in=collection_ids)
    
    context = {
        'collection_products': collection_products,
        'collection_count': len(collection_products),
        'collection_ids': collection_ids,
    }
    return render(request, 'marketra/collection.html', context)

@login_required
def recommendations(request):
    if not request.user.is_authenticated:
        return render(request, 'marketra/recommendations.html', {'is_ai_success': False})

    # AI Engine call pandrom
    recommended_data = get_hybrid_recommendations(request.user, num_rec=12)

    # Collection IDs for 'Add to Cart' buttons in recommendation page
    collection_ids = []
    if hasattr(request.user, 'collection'):
        collection_ids = list(request.user.collection.products.values_list('id', flat=True))

    context = {
        'recommended_data': recommended_data, # Contains {'product': p, 'score': s}
        'is_ai_success': True if recommended_data else False,
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
def toggle_wishlist(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        
        if wishlist.products.filter(pk=pk).exists():
            wishlist.products.remove(product)
            status = 'removed'
        else:
            wishlist.products.add(product)
            status = 'added'
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'action': status, 'message': f'Product {status}'})
            
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
