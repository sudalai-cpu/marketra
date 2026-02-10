from .models import Product

def ai_score(candidate, viewed_product):
    score = 0

    if candidate.category == viewed_product.category:
        score += 5

    price_diff = abs(candidate.price - viewed_product.price)
    if price_diff <= 500:
        score += 3
    elif price_diff <= 1000:
        score += 1

    if candidate.is_featured:
        score += 2

    return score


def rule_based_recommendations(viewed_product):
    candidates = Product.objects.exclude(id=viewed_product.id)

    scored_products = []

    for product in candidates:
        score = ai_score(product, viewed_product)
        if score > 0:
            scored_products.append((score, product))

    scored_products.sort(reverse=True, key=lambda x: x[0])

    return [p for score, p in scored_products][:6]
