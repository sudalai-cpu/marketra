from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
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
