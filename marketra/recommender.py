from .models import Product

def rule_based_recommendations(product):
    same_category = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)

    similar_price = Product.objects.filter(
        price__gte=product.price - 500,
        price__lte=product.price + 500
    ).exclude(id=product.id)

    return (same_category | similar_price).distinct()[:6]
