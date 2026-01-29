from django.shortcuts import render, get_object_or_404
from .models import Product
import random

def home(request):
    # Featured products: top 4 by AI rank
    featured_products = Product.objects.all().order_by('ai_rank')[:4]
    
    # Recommended products: 4 random products
    recommended_products = Product.objects.all().order_by('?')[:4]
    
    context = {
        'featured_products': featured_products,
        'recommended_products': recommended_products,
    }
    return render(request, 'marketra/index.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Recommendations on detail page
    recommended_products = Product.objects.exclude(pk=pk).order_by('?')[:4]
    
    context = {
        'product': product,
        'recommended_products': recommended_products,
    }
    return render(request, 'marketra/product_detail.html', context)
