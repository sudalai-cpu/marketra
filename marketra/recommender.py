from marketra.models import Product
from .models import Collection


def get_ai_recommendations(user):
    recommended = []

    user_collections = Collection.objects.filter(user=user)

    print("USER COLLECTION COUNT:", user_collections.count())

    owned_product_ids = user_collections.values_list(
        'products__id',
        flat=True
    )

    for product in Product.objects.exclude(id__in=owned_product_ids):
        print("RECOMMENDING:", product.id, product.category)
        recommended.append(product)

    if recommended:
        return recommended[:8], True

    return [], False
